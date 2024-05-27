<?php
function getElementsByClass(&$parentNode, $tagName, $className) {
    $nodes=array();

    $childNodeList = $parentNode->getElementsByTagName($tagName);
    for ($i = 0; $i < $childNodeList->length; $i++) {
        $temp = $childNodeList->item($i);
        if (stripos($temp->getAttribute('class'), $className) !== false) {
            $nodes[]=$temp;
        }
    }

    return $nodes;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the search query and desired condition from the form
    $query = $_POST['query'];
    $condition = $_POST['condition'];

    $searchUrl = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' . urlencode($query) . '&_sacat=0&LH_ItemCondition=' . $condition;
    $htmlContent = file_get_contents($searchUrl);

    if ($htmlContent === false) {
        die("Error fetching the webpage.");
    }

    $dom = new DOMDocument();
    @$dom->loadHTML($htmlContent);

    $elements = getElementsByClass($dom, 'div', '');
    $elementsCount = count($elements);

    for ($i = 0; $i < $elementsCount; $i++) {
    $element = $elements->item($i);
    if ($element->hasAttribute('class') && $element->getAttribute('class') === 'abc') {
        echo $element->nodeValue . "\n";
    }
    }

    // Extract product links from the search results page
    $productLinks = $crawler->filter('.s-item__link')->each(function ($node) {
        return $node->attr('href');
    });

    // Create an empty array to store the product details
    $products = [];

    // Loop through each product link and scrape its details
    foreach ($productLinks as $productLink) {
        // Use Goutte to scrape the product page
        $productCrawler = $client->request('GET', $productLink);

        // Extract the product title, price, description, condition, and images
        $title = $productCrawler->filter('.ux-textspans.ux-textspans--BOLD')->text();
        $price = $productCrawler->filter('.x-price-primary span')->text();
        $desc = $productCrawler->filter('#desc_ifr')->attr('src');
        $condition = $productCrawler->filter('.x-item-condition-text .x-item-condition-text__condition span span span')->text();
        $images = $productCrawler->filter('.ux-image-magnify__image--original')->each(function ($node) {
            return $node->attr('src');
        });

        // Add the product details to the array
        $products[] = [
            'link' => $productLink,
            'title' => $title,
            'price' => $price,
            'desc' => $desc,
            'condition' => $condition,
            'images' => $images
        ];
    }

    // Generate the HTML for the search results
    $html = '';
    foreach ($products as $product) {
        // Get the first image URL
        $imageUrl = isset($product['images'][0]) ? $product['images'][0] : '';

        $html .= '<div style="overflow: hidden; width: 75%; height: 480px; border: 1px solid rgb(220, 220, 220); padding: 20px;">';
        $html .= '<img src="' . $imageUrl . '" style="float: left; padding-right: 20px; height: 180px;"></img>';
        $html .= '<a href="' . $product['link'] . '"><h2>' . $product['title'] . '</h2></a>';
        $html .= '<h2>Zustand: ' . $product['condition'] . ', gewünschter Zustand: ' . $condition . '</h2>';
        $html .= '<h2>Preis: ' . $product['price'] . ' €</h2><br>';
        $html .= '<iframe width="100%" height="260px" src="' . $product['desc'] . '"></iframe><br>';
        $html .= '</div>';
    }

    // Send the HTML to the client
    echo $html;
}
?>
