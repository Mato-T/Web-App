import datetime as dt
from bs4 import BeautifulSoup
import re
import mariadb
from selenium import webdriver
import html

def returnDate(date):
    """returns a formated date string"""
    date = dt.datetime.strptime(date, "%B %d, %Y")
    return f"{date.year}-{date.month}-{date.day}"
def createEntry(parent, cur, star, product_id):
    """takes the review information and inserts them into the database"""
    review_text = html.escape(parent.find("span", {"class": "review-text"}).text[:900].replace("\n", ""))#finds the review text, escapes its characters and truncates them at 900
    if len(review_text) > 10: #the review must be longer than 10 characters to be inserted into the database
        review_info = parent.find("span", {"class": "review-date"}).text
        country = review_info[12:review_info.find("on")-1] #cuts out the country from the review information
        country = re.sub(r'[^a-zA-Z\ ]', '', country).strip() #sometimes, a flag is included, but only the country will be stored
        date = returnDate(review_info[review_info.find("on")+3:]) #returns a formatted date string
        try: #tries to insert the values
            cur.execute('INSERT INTO reviews (stars, content, published, country, product_id) VALUES  \
                ("{}", "{}", "{}", "{}", "{}")'.format(star, review_text, date, country, product_id))
        except mariadb.IntegrityError: #if it already exist, simply continue
            pass

def getHTML(url):
    """returns the HTML code from an URL"""
    #Scraping Amazon can be quite challenging so I decided to use a headless browser, which is slower but more human like since it stores all cookies and executes JS
    headOption = webdriver.FirefoxOptions()
    headOption.add_argument('-headless')
    driver = webdriver.Firefox(options=headOption)
    driver.get(url)
    pageSource = driver.page_source
    driver.close()
    return pageSource

def getReviews(bs, cur, product_id, pages, star):
    """stores the reviews from a product inside the database"""
    # Amazon has an <a> tag for the webpages of each star. In my case, I am only scraping the reviews on the first page; i.e., 10 reviews per star
    link = bs.findAll("a", {"class": "a-link-normal", "title":re.compile(f"^({star} stars represent)")})[0].attrs["href"]
    for i in range(pages):
        pageSource = getHTML('https://www.amazon.com'+link) 
        bs = BeautifulSoup(pageSource, 'html.parser')
        for j in bs.findAll("div", {"class": "review"}): #iterates through each review
            createEntry(j, cur, star, product_id)
        link = link[:46]+"&pageNumber="+str(i) #would update the link to the next page
    cur.connection.commit() #commit all changes made to the database