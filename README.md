# Introduction
- I created this web app, dubbed the ReviewReview, as an exercise for me to get around all the data that is available on the Internet. There is unlimited amount of information present for everyone, so it is important to be able to make sense of it. This application crawls through Amazon products, extracts its information and stores the information in a database for faster access.
- The most relevant part of this applications is retrieving the reviews of such products and offering certain filtering options. The user is able to filter for certain star reviews can even provide a keyword that should be matched against the reviews.
- The target audience for this web app is the everyday-consumer who may wants to make a more educate purchase decision. If the durability is an important factor for the consumer decision, the user is able to filter for reviews that mention the durability in their review. This web page provides a much more comfortable interface for "review reviews" in comparison to the Amazon web page.

# Data Requirement
- The main purpose of this application is displaying the reviews in an ordered fashion, meaning that there is not much information needed neither from the product nor the reviews. For the product, I decided to include very basic information, such as the brand, the product name, and the price.
- The essential data requirement is the text of each review, since this provides all the information about the positive and negative aspects of the product. Also, it allows the review to be classified using the provided lable. I also included the the number of stars the review has, since it provides a basic feeling for the sentiment of that review.
- All this information is stored inside a database. This is because the scraping of web pages requires some time that the user might not like to wait for. Storing the results from the scraping task in a database makes the next request for this product a simple database query. The simple database structure can be depicted by the following:

  ![overview](https://user-images.githubusercontent.com/127037803/230575355-dab1e8d3-72b3-4e5b-8a2b-daeabf7d05d5.png) 
 - For more information, check out the SQL.txt file in this repository to look at the SQL queueries.
 
 # Features
- To get the features across of an interactive website is quite a challenge, so I decided to make a quick video. However, in a nutshell, the user enters a URL of an Amazon product into the text field, waits until the results have been loaded up and then provides a label to filter the displayed reviews. For a more detailed display of the wepage, check out this video:
