from database import connectToDatabase
from product import getProduct
from review import *
from label import prepareLabels
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import json
import html

app = Flask(__name__)
cur = connectToDatabase() #create a universal cursor (used by all methods) for the database


def returnResult(**kwargs):
    """returns the data obtained from the database query and formats it into JSON"""
    response = jsonify(kwargs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/scraping', methods=['POST', "GET"])
def crawl():
    """Crawls Amazon products and stores the result in a database"""
    url = request.form['key'] #get the URL from the AJAX call
    try:
        cap = [i for i, c in enumerate(url) if c == "/"][2] #checks for the second occurence of "/" to find the cap that separates the domain from the rest of the URL
        if url[:cap] != 'https://www.amazon.com': #if it is not an Amazon.com link, return an error
            return returnResult(result="InvalidURL")
    except IndexError: #if it does not resemble the amazon domain, also return an error
         return returnResult(result="InvalidURL")
    pageSource = getHTML(url) #get the HTML code of the page
    bs = BeautifulSoup(pageSource, 'html.parser') #and create a BS object for parsing
    if cur == 0: #if the connection to the database failed, return an error
        return returnResult(result="InvalidDatabaseConnection")
    product = getProduct(bs, cur) #get the product information
    if type(product) == str: #if it is a duplicate, product name is returned since no product was stored in the database. Also, no reviews are scraped (already stored in the database)
        cur.execute(f"SELECT * FROM products WHERE product_name = '{product}'")
        product = cur.fetchall()[0][0] #get the id of the product and return it for results.php since it must be put into the query string
        return returnResult(result="IntegrityError", product_id=product)
    else: #else, scrape the reviews of the prodcut
        for i in range(1, 6): #go through each star-review (i.e., 1 star reviews, 2 stars reviews, etc.)
            getReviews(bs, cur, product, 1, i) #store the reviews in the database
    return returnResult(result="Success", product_id=product)

@app.route('/filter', methods=['POST', "GET"])
def applyFilter():
    """use the filter values and return the reviews that match the description"""
    product_id = request.form['product_id']
    label = html.escape(request.form['target']) #escape the characters 
    if label != "0": #if a label was passed into the AJAX call, the reviews table must be joined with the reviews_labels and labels, since they hold the information on which review has which label
        query_string = f"SELECT * FROM reviews r LEFT JOIN reviews_labels rl ON r.id = rl.review_id LEFT JOIN labels l ON rl.label_id = l.id WHERE r.product_id = '{product_id}'"
        query_string += f" AND l.label = '{label}' AND l.target = '1'"  
        prepareLabels(cur, product_id, label) 
    else: #if no label was passed, the reviews table is sufficient
        query_string = f"SELECT * FROM reviews r WHERE r.product_id = '{product_id}'"
    stars = json.loads(request.form['star'])
    if len(stars) != 0: #iterate through each star and add its condition to the query string
        star_filter = " AND ("
        for i in stars:
            star_filter += f"r.stars = '{i}' OR " #OR because its not exclusive
        query_string += star_filter[:-4]+")" #remove the last OR that was added and close the parenthesis
    start_date = request.form['start']
    if start_date != "0":
        query_string += f" AND r.published >= '{start_date}'"
    end_date = request.form['end']
    if end_date != "0":
        query_string += f" AND r.published <= '{end_date}'"
    cur.execute(query_string) #execute the query 
    results = cur.fetchall() #and gather the results
    cur.execute(f"SELECT * FROM products WHERE id = '{product_id}'") #also, the webpage displays information about the prodcut, so return this as well
    product = cur.fetchall()[0]
    if len(results) == 0: #if no reviews match the filter, just return the product information
        return returnResult(result="EmptyResults", name=product[1], brand=product[2], price=product[3], product_stars=product[4], num_reviews=product[5])
    else: #if reviews match it, return both
        return returnResult(result="Success", stars=[i[1] for i in results], content=[html.unescape(i[2]) for i in results], published=[i[3] for i in results], \
            name=product[1], brand=product[2], price=product[3], product_stars=product[4], num_reviews=product[5])


