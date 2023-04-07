from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import pipeline
import html

def obtainLabels(cur, product_id, label):
    """check if the labels match the review and insert the result into the database"""
    device = "cuda:0"
    model = AutoModelForSequenceClassification.from_pretrained("sileod/deberta-v3-base-tasksource-nli") #zero-shot classifier
    tokenizer = AutoTokenizer.from_pretrained("sileod/deberta-v3-base-tasksource-nli", model_max_length=1000)
    pipe = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer, device=device)
    
    matches = dict() #stores the result in a dict
    cur.execute(f"SELECT * FROM reviews WHERE product_id = '{product_id}'") #gets all reviews from the prodcut
    rows = cur.fetchall()
    products = [(html.unescape(i[2][:511]), i[0]) for i in rows] #get the review text and review ID from each entry from the query
    results = pipe([i[0] for i in products], label) #pass in the text and the label
    for text, score in zip(products, results): #iterate through each test and its corresponding score
        if score["scores"][0] >= 0.8: #if the score is above 80%, it matches the review
            matches[text[1]] = 1
        else: #if it is below, it does not match
            matches[text[1]] = 0
    #add both 0 and 1 because, all reviews of one product might not match the label, so adding both indicates that the classification has already been made
    cur.execute('INSERT INTO labels (label, target) VALUES \
            ("{}", "{}")'.format(label, 0))
    negative = cur.lastrowid #store the label ID for the reviews_labels query
    cur.execute('INSERT INTO labels (label, target) VALUES \
            ("{}", "{}")'.format(label, 1))
    positive = cur.lastrowid #this ID as well
    for review_id, target in matches.items(): #now iterate through each result and add the review ID and label ID into the reviews_labels table
        if target == 0:
            cur.execute('INSERT INTO reviews_labels (review_id, label_id) VALUES \
                ("{}", "{}")'.format(review_id, negative))
        else:
            cur.execute('INSERT INTO reviews_labels (review_id, label_id) VALUES \
                ("{}", "{}")'.format(review_id, positive))
    cur.connection.commit() #only if everything succeedes, commit the changes to the database
def prepareLabels(cur, product_id, label):
    """checks if the reviews were already classfied based on this label. If not, perform the classifciation"""
    query = f"SELECT * FROM reviews r JOIN reviews_labels rl ON r.id = rl.review_id JOIN labels l ON l.id = rl.label_id \
        WHERE r.product_id = '{product_id}' AND l.label = '{label}'" 
    cur.execute(query)
    results = cur.fetchall()
    if len(results) == 0: #if the label cannot be found in the database, make the classification
        obtainLabels(cur, product_id, label)