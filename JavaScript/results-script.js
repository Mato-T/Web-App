import { displayMessage, loadReviews } from "./index-script.js"

function displayResults(parent, content, published, stars){ //is called when the filters where applied and the results come back from the database
    for (var i = 0; i < content.length; i++){ //iterates through each review and adds it to the webpage
        var container = $("<div/>", {"class": "review-container"}).appendTo(parent)
        $("<p/>", {"class": "format", html:published[i].slice(0, -13)}).appendTo(container)
        $("<p/>", {"class": "format", html: '"'+content[i]+'"'}).appendTo(container)
        var stars_container = $("<div/>", {"class": "format"}).appendTo(container) //fills out the number of appropriate stars
        for (var j = 0; j < stars[i]; j++){
            $("<i/>", {"class": "fa fa-star"}).appendTo(stars_container)
        }
        for (var j = 0; j < 5-stars[i]; j++){ //and adds the missing, empty ones to count up to 5
            $("<i/>", {"class": "fa-regular fa-star"}).appendTo(stars_container)
        }
    }
}

function displayProduct(name, brand, price, stars, num_reviews, screen){ //is called when the results come back from the database to display the product info
    if (screen >= 660){ //only when the screen is larger than 660px, should the product info line up with the reviews (vertically). With smaller sizes, it fills out the entire area
        var distanceFromLeft = $("#search-results").offset().left
        var distanceFromRight = $(window).width() - (distanceFromLeft + $("#search-results").outerWidth());
        $("#product-info").css({
            "padding-left": distanceFromLeft,
            "padding-right": distanceFromRight,
        })
    }
    //append all product details to the container
    $("<h3/>", {html: "Product"}).appendTo($("#product-info"))
    $("<p/>", {html: name, css:{"text-align": "center"}}).appendTo($("#product-info"))
    $("<p/>", {html: "Sold for "+price+"$ by "+brand}).appendTo($("#product-info"))
    var stars_container = $("<div/>", {"class": "format centered-row"}).appendTo($("#product-info"))
    for (var j = 0; j < Math.round(stars); j++){
        $("<i/>", {"class": "fa fa-star"}).appendTo(stars_container)
    }
    for (var j = 0; j < 5-Math.round(stars); j++){
        $("<i/>", {"class": "fa-regular fa-star"}).appendTo(stars_container)
    }
    $("<p/>", {html: "("+stars+")  from "+ num_reviews+" total reviews"}).appendTo(stars_container)
}

function prepareResults(){ //is called before the new reviews come in so that old ones (from old filtering) are cleared out
    $("#search-results").empty()
    $("<h3/>", {html: "Reviews"}).appendTo($("#search-results"))
}

function isValidDate(dateString) { //is called to check if the date inside the input field is valid
    var d = new Date(dateString);
    return !isNaN(d.getTime());
  }

function applyFilter(query){ //this is the function that reads the values of the filter and passes them to the Python script
    $(".fail-msg").empty()  
    var start_date = 0; end_date = 0; label = 0;
    var stars = []
    for (const i of $("input[type=checkbox]")){ //iterate through each checkbox and add those that are checked to the list
        if($(i).prop("checked") == true){
            stars.push($(i).val())
        }
    }
    if ($("#start-date").val().length > 0 && isValidDate($("#start-date").val())){ //if the input field has a valid date, add it to the items that are passed to the Python script
        var start_date = $("#start-date").val()
    }else if (isValidDate($("#start-date").val()) == false && $("#start-date").val().length > 0){//if it is not a valid date (but has content in it) print an alert statement
        $("<i/>", {"class": "fa-solid fa-triangle-exclamation", css: {"color": "rgb(139, 23, 23)"}}).appendTo($("#start-date").siblings()[0])
    } //same procedure for the other date
    if ($("#end-date").val().length > 0 && isValidDate($("#end-date").val())){ 
        var end_date = $("#end-date").val()
    }else if (isValidDate($("#end-date").val()) == false && $("#end-date").val().length > 0){
        $("<i/>", {"class": "fa-solid fa-triangle-exclamation", css: {"color": "rgb(139, 23, 23)"}}).appendTo($("#end-date").siblings()[0])
    }
    if ($("#label").val().length > 0){ //read out the classification label
        var label = $("#label").val()
    }
    $.ajax({ //call to pass the information of the filters to the Python script
        url: "http://localhost:5000/filter", 
        data: {product_id: query, star: JSON.stringify(stars), start: start_date, end: end_date, target: label},
        type: "POST",
        dataType: "json", 
        success: function(data) { 
            $("#spinner").remove() //remove the spinner that is used to indicate that the Transformer model is working on the classification (or if the process was initiated)
            $("#product-info").empty() //remove previous product_info
            prepareResults()
            displayProduct(data.name, data.brand, data.price, data.product_stars, data.num_reviews, window.screen.width) //display the new product info
            if (data.result == "Success"){ //if a success, display the reviews
                displayResults($('#search-results'), data.content, data.published, data.stars)
            }else if (data.result == "EmptyResults"){ //if nothing matched the filter requirements, print a small warning signal
                var container = $("<div/>", {"class" : "centered-row", css: {"color": "grey", "margin-top": "10%"}}).appendTo($("#search-results"))
                $("<i/>", {"class": "fa-solid fa-triangle-exclamation", css: {"margin-right": "10px"}}).appendTo(container)
                $("<p/>", {html: "Your query did not yield any results"}).appendTo(container)
            }
        },
        error: function(error) { //in case of an error, remove previous results and the spinner
            prepareResults()
            $("#spinner").remove() 
            
        }
    });
}


$(document).ready(function(){
    var queryString = window.location.search
    var urlParams = new URLSearchParams(queryString) 
    var query = urlParams.get("product") //read out the query string of the URL
    if (query){ //if there was a query (e.g., due to using the search bar)
        applyFilter(query) //make the call to the script to get each review that matches the filter
        //also, the change event and keypress event can trigger the same process
        $("input[type=checkbox]").change(function(){ 
            applyFilter(query)
        })
        $(".input-bar").keypress(function(e){
            if (e.which == 13){
                if (e.target.id == "label"){ //display a small spinner that spins as long as the model is classifying or the database returns reviews with already existing labels
                    $("<i/>", {"class": "fa-solid fa-spinner fa-spin", id: "spinner"}).appendTo($(e.target).parent())
                }
                applyFilter(query) 
            }
        })
    }
    else { //if the query is empty (e.g., a user opened this page on purpose, i.e., not being transferred)
        //since the product info is missing, the filter and reviews boxes must have a margin to not overlap with the nav-bar
        //also, display a small warning that nothing has been selected
        $("#filter").css({"margin-top": "50px"}) 
        $("#search-results").css({"margin-top": "50px"})
        var container = $("<div/>", {"class" : "centered-row", css: {"color": "grey", "margin-top": "10%"}}).appendTo($("#search-results"))
        $("<i/>", {"class": "fa-solid fa-triangle-exclamation", css: {"margin-right": "10px"}}).appendTo(container)
        $("<p/>", {html: "No product selected yet. Please enter a URL into the search bar"}).appendTo(container)
    }
    //on the nav-bar, clicking the button and pressing enter on the input field triggers the process of scraping and loading this page with a new query string
    $("#button-results").click(function(){
        var url = $("#input-field-results").val()
        displayMessage($(".messages"), "Please wait while the data is being gathered", "green", "fa-solid fa-spinner fa-spin", window.screen.width )
        loadReviews(url, window.screen.width )
    })
    $("#input-field-results").keypress(function(e){
        if (e.which == 13){
            var url = $("#input-field-results").val()
            displayMessage($(".messages"), "Please wait while the data is being gathered", "green", "fa-solid fa-spinner fa-spin", window.screen.width )
            loadReviews(url, window.screen.width )
        }
    })
})