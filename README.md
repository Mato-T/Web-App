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
- To get the features across of an interactive website is quite a challenge, so I decided to make a quick video. However, in a nutshell, the user enters a URL of an Amazon product into the text field, waits until the results have been loaded up and then provides a label to filter the displayed reviews. For a more detailed display of the wepage, check out the features.mp4 file in this repository.

# Technologies
- I used several technologies building this application. First, I hosted a database using MariaDB that will store the information that resulted from crawling the Amazon webpages. Of course, I also used the most popular front-end technologies like HTML, CSS, and JavaScript. Most of the webpage is acutally dynamically generated, meaning that the actual content of the wep page is based on the queries made to the database.
- When it comes to backend technology, I set up a Flask app to handle the connection made to the query and initiate the crawling process. Furthermore, the Flask app directs the texts from the reviews to the Transformer model.
- As mentioned earlier, an important part of this application is classifying the reviews. Since no labels are available, a zero-shot classifier is used. Zero-shot classifiers are typically trained using a pre-trained language model, such as BERT or GPT. The model uses its pre-trained knowledge of language and concepts to make a prediction about the class of the input data by contrasting the input text and the label. The label, for example, might be a prompt like: "this text is about customer service".
- Hugging Face is a useful platform that provides an enormous amount of different Transformer models. I decided to go with DeBERTa-v3-base (https://huggingface.co/sileod/deberta-v3-base-tasksource-nli) that was fine-tuned on 520 tasks, including a number of datasets that I deemed relevant for my purpose (e.g., https://huggingface.co/datasets/app_reviews and https://huggingface.co/datasets/amazon_polarity).
- When it comes to scraping Amazon webpages, I used to essential technologies. First, I used Selenium's webdriver, an API that provides an interface for controlling the behaviour of web browsers. A headless webdriver provides the browser functionality without any visible UI. The advantage of such a web browser is that it executes JavaScript and stores cookies to appear more human like. This will prevent Amazon to prompt CAPTCHA challenges.
- Using Selenium, I am able to obtain the HTML code of the Amazon webpage (it will take more time, however, than using the Requests library). I feel most comfortable using Beautiful Soup for parsing HTML documents, so I used this library to extract the information required.

# Limitations
- This web applications has several limitations. First, as shown in the demo video, it takes considerable time to crawl the information from the Amazon web page. Note that, for demonstration purposes, I only crawled the first 10 reviews from each star (i.e., 10 one-star reviews, 10 two-star reviews, etc.). In many cases, there are thousands of reviews that can be scraped, taking even more time to obtain.
- Second, I tried but did not succeed in fine-tuning this model even further. This is because of the limited computation resources I have. In my case, I was constantly running out of CUDA memory, since the model has millions of parameters. I tried truncating the text input, using a batch size of 1 with gradient accumulation, etc., but nothing seemed to work. For this reason, the model might be inaccurate from time to time. This is especially true when the text has 30 characters or less.
- Another major limitation is that this web page does not work with all Amazon products. It works fine with tangible things, like hardware, household items, etc., but it does not work with e-Books, movies, or similar. This is because Amazon does not structure all of their products the same, and it would require additional coding for these products
- Deep learning is dominated by English, meaning that the DeBERTa-v3-base is primarily designed for the English language so I decided to accept products from the Amazon.com website only.

# Conclusion and Future Development


