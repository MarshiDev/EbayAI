<!DOCTYPE html>
<html>
<head>
    <title>Ebay Product Search</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
</head>
<body>
    <h1>Ebay Product Search</h1>

    <form id="searchForm">
        <label for="query">Suchbegriff:</label>
        <input type="text" id="query" name="query"><br><br>

        <label for="condition">Gewünschter Zustand:</label>
        <select id="condition" name="condition">
            <option value="neu">Neu</option>
            <option value="gebraucht">Gebraucht</option>
        </select><br><br>

        <button type="submit">Suchen</button>
    </form>

    <div id="results">
        </div>

    <script>
        $(document).ready(function() {
            $("#searchForm").submit(function(event) {
                event.preventDefault();

                // Get the search query and desired condition from the form
                var query = $("#query").val();
                var condition = $("#condition").val();

                // Send AJAX request to the PHP server
                $.ajax({
                    url: "search.php",
                    type: "POST",
                    data: {
                        query: query,
                        condition: condition
                    },
                    success: function(response) {
                        // Process the HTML response on the client side
                        processHtml(response, condition);
                    },
                    error: function(error) {
                        console.error(error);
                    }
                });
            });

            // Function to process the HTML response and display results
            function processHtml(html, condition) {
                // Parse the HTML string into a DOM object
                var parser = new DOMParser();
                var doc = parser.parseFromString(html, "text/html");

                // Find all product divs
                var productDivs = doc.querySelectorAll("div");

                // Array to store the product data
                var products = [];

                // Loop through each product div
                for (var i = 0; i < productDivs.length; i++) {
                    var productDiv = productDivs[i];

                    // Extract product data
                    var link = productDiv.querySelector("a").href;
                    var title = productDiv.querySelector("h2").textContent;
                    var price = productDiv.querySelector("h2:nth-of-type(3)").textContent;
                    var conditionText = productDiv.querySelector("h2:nth-of-type(2)").textContent;
                    var imageSrc = productDiv.querySelector("img").src;
                    var description = productDiv.querySelector("iframe").src;

                    // Create product object and add to array
                    var product = {
                        link: link,
                        title: title,
                        price: price,
                        condition: conditionText,
                        image: imageSrc,
                        description: description
                    };
                    products.push(product);
                }

                // Sort the products array based on price
                products.sort(function(a, b) {
                    return parseFloat(a.price.replace(',', '.')) - parseFloat(b.price.replace(',', '.'));
                });

                // Generate the HTML for the search results
                var htmlResults = '';
                for (var i = 0; i < products.length; i++) {
                    var product = products[i];

                    htmlResults += '<div style="overflow: hidden; width: 75%; height: 480px; border: 1px solid rgb(220, 220, 220); padding: 20px;">';
                    htmlResults += '<img src="' + product.image + '" style="float: left; padding-right: 20px; height: 180px;"></img>';
                    htmlResults += '<a href="' + product.link + '"><h2>' + product.title + '</h2></a>';
                    htmlResults += '<h2>Zustand: ' + product.condition + ', gewünschter Zustand: ' + condition + '</h2>';
                    htmlResults += '<h2>Preis: ' + product.price + ' €</h2><br>';
                    htmlResults += '<iframe width="100%" height="260px" src="' + product.description + '"></iframe><br>';
                    htmlResults += '</div>';
                }

                // Update the results div with the generated HTML
                $("#results").html(htmlResults);
            }
        });
    </script>
</body>
</html>
