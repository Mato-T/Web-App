import mariadb
import html

def getProduct(bs, cur):
    """extracts the information about a product ans stores in in the database"""
    product_name = html.escape(bs.find("span", {"id": "productTitle"}).text.strip())
    try: #might be out of stock or something
        price = bs.find("span", {"class": "a-price-whole"}).text+bs.find("span", {"class": "a-price-fraction"}).text        
    except AttributeError:
        try: #Amazon has different ways of displaying the price (or none at all)
            price = bs.find("span", {"class", "a-offscreen"}).text[1:]
        except AttributeError:
            price = 0
    if bs.find("a", {"id": "bylineInfo"}).text[0] == "V": #Visit the x Store
        brand = bs.find("a", {"id": "bylineInfo"}).text[10:-6]
    elif bs.find("a", {"id": "bylineInfo"}).text[0] == "B": #Brand: x
        brand = bs.find("a", {"id": "bylineInfo"}).text[7:]
    else:
        brand = "Not Found" 
    stars = bs.findAll("i", {"class": "a-icon-star"})[0].text[:3] #different way of storing the stars
    if stars == "":
        stars = bs.findAll("i", {"class": "a-icon-star"})[1].text[:3]
    num_reviews = bs.find("span", {"id": "acrCustomerReviewText"}).text[:-8].replace(",", "")
    try: #tries to insert the information found into the database
        cur.execute('INSERT INTO products (product_name, price, brand, stars, num_reviews) VALUES  \
            ("{}", "{}", "{}", "{}", "{}")'.format(product_name, price, brand, stars, num_reviews))
        return cur.lastrowid #retunrs the product ID for the processing of the reviews for that prodcut
    except mariadb.IntegrityError: #since no ID is available, simply returns the product name if it is a duplicate
        return product_name
    