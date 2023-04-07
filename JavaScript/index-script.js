export function displayMessage(parent, message, color, icon, screen=660){ //is called to display a message such as error, or waiting for data to be gathered
    $(".messages").empty() //remove previous message
    var container = $("<div/>", {"class": "error centered-row", css: {"background-color": color}}).appendTo(parent)
    $("<i/>", {"class": icon, css: {"margin": "0px 5px"}}).appendTo(container)
    if (screen >= 660){ //only when the screen is smaller than 660px, it should display a message. Otherwise it gets crowded
        $("<p/>", {html: message}).appendTo(container)
    }

}

export function loadReviews(url, screen=660){
    $.ajax({ //call to scrape the product info and reviews
        url: "http://localhost:5000/scraping", 
        data: {key: url},
        type: "POST",
        dataType: "json", 
        success: function(data) { 
            if (data.result == "IntegrityError" || data.result == "Success"){ //product seems to be in database already or it was successfully scraped, so go to results.php 
                window.location = "http://localhost:3000/results.php?product="+data.product_id
                }  
            else if (data.result == "InvalidURL"){
                displayMessage($(".messages"), "Please enter a valid URL", "rgb(139, 23, 23)", "fa-solid fa-triangle-exclamation", screen)
            }
            else if (data.result == "InvalidDatabaseConnection"){
                displayMessage($(".messages"), "Failed to establish a connection to the database", "rgb(139, 23, 23)", "fa-solid fa-triangle-exclamation", screen)
            }
        },
        error: function(error) {
            displayMessage($(".messages"), "Some internal error occured", "rgb(139, 23, 23)", "fa-solid fa-triangle-exclamation", screen)
        }
    });
}

$(document).ready(function(){
//when either the enter key or the search button was clicked, get the url, send the waiting message and load the review
    $("#button-index").click(function(){ 
        var url = $("#input-field-index").val()
        displayMessage($(".messages"), "Please wait while the data is being gathered", "green", "fa-solid fa-spinner fa-spin")
        loadReviews(url)
    })
    $("#input-field-index").keypress(function(e){
        if (e.which == 13){ //when the key pressed was enter
            var url = $("#input-field-index").val()
            displayMessage($(".messages"), "Please wait while the data is being gathered", "green", "fa-solid fa-spinner fa-spin")
            loadReviews(url)
        }
    })
})