<!DOCTYPE html>
<html>
    <head>
    <title>ReviewReview</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://code.jquery.com/jquery-3.6.3.js" type="text/javascript"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer">
    <link rel="stylesheet" href="CSS/shared-stylesheet.css">
    <link rel="stylesheet" href="CSS/results-stylesheet.css">
    <script src="JavaScript/results-script.js" type="module"></script>
  </head>
  <body>
    <div class="search-bar centered-row" id="nav-bar">
        <p id="co">The ReviewReview</p>
        <div class="search centered-row">
            <input class="text-input" type="text" name="search" placeholder="enter an amazon.com URL" id="input-field-results" aria-label="input for the product URL">
            <button class="search-button centered-row" id="button-results"><i class="fa fa-search"></i></button> 
        </div>
        <div class="messages">

        </div>  
    </div>
    <div id="product-info"></div>
    <div class="content">
      <div id="filter">
          <div class="filter-item" id="stars">
            <h3>Stars</h3>
            <div class="wrapper centered-row checkbox-wrapper">
              <label>
                <input type="checkbox" value=1>1 Star
              </label>
            </div>
            <div class="wrapper centered-row checkbox-wrapper">
              <label>
                <input type="checkbox" value=2>2 Stars
              </label>
            </div>
            <div class="wrapper centered-row checkbox-wrapper">
              <label>
                <input type="checkbox" value=3>3 Stars
              </label>
            </div>
            <div class="wrapper centered-row checkbox-wrapper">
              <label>
                <input type="checkbox" value=4>4 Stars
              </label>
            </div>
            <div class="wrapper centered-row checkbox-wrapper">
              <label>
                <input type="checkbox" value=5>5 Stars
              </label>
            </div>
          </div>
          <div class="filter-item">
            <h3>Date</h3>
            <div class="wrapper centered-row text-wrapper">
              <label>
                <input class="input-bar" type="text" placeholder="YYYY-MM-DD" id="start-date" aria-label="input for the starting date"> Starting Date
                <div class="fail-msg"></div>
              </label>
              
            </div>
            <div class="wrapper centered-row text-wrapper">
              <label>
                <input class="input-bar" type="text" placeholder="YYYY-MM-DD" id="end-date" aria-label="input for the ending date">Ending Date
                <div class="fail-msg"></div>
              </label>
              
            </div>
          </div>
          <div class="filter-item">
            <h3>Label</h3>
            <div class="wrapper text-wrapper" style="display:inline-block"> <!-- required for the spinning symbol -->
                <input class="input-bar" type="text" placeholder="e.g. quality" id="label" maxlength="15" aria-label="input for the classification label">
            </div>
          </div>
      </div>
      <div id="search-results">
        <h3>Reviews</h3>
      </div>
    </div>
  </body>
</html>