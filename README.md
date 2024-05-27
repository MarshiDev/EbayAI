# EbayAI
## What is this?
EbayAI is a tool for helping you search ebay for products. It uses a flask webserver to provide a nicer frontend for the user and ChatGPT in the backend for advanced text interpretation.

## Installation
Clone the project to your computer using git clone or by downloading it as a zip file. Make sure to install all the required python packages using ```pip install -r requirements.txt```. Additionally, after installing, you will need to provide an OpenAI-API-key
in the 'api.key' file.

## Usage
In your terminal, run the command ```python3 main.py``` to start the flask webserver. You should now be able to open the address 'localhost:8070'. You will be greeted with a menu that looks like this:
<img width="80%" alt="EbayAI" src="https://github.com/MarshiDev/EbayAI/assets/97107764/04f9381b-d1cf-4f21-8bb7-1ccb262ded59"><br><br>
If you do not speak german, I recommend you use google auto-translate or similar on this website for a better experience with this tool.
Now, open ebay.com (or the respective website for your country, i.e. ebay.de) and search for the product you want to search for. I recommend to filter for 'Buy It Now' and sort by 'Price + Shipping: lowest first' to achieve the best results.
Then copy and paste the link from the search bar into the Ebay-link field. Then in the 'gewünschter Zustand' field (this is german for target condition) try to accurately and precisely describe the condition you want the products to be in.
Now hit the 'Suchen' (german for search) button to start the search. Next to every Product, you will see 'gewünschter Zustand' with a 'Ja' (yes) or 'Nein' (no). This describes if the product matches the target condition. Now if you hit the
'Unpassende entfernen' (remove non-matching) button, only results where the condition actually matches the target condition will be shown.
