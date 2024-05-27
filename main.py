from flask import Flask, request as f_req
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
import certifi
import ssl

app = Flask(__name__)

MODEL = "gpt-3.5-turbo"
OPENAI_SECRET_KEY = open("api.key", "r").read()

prompt = "Prüfe, ob Titel und Beschreibung eines Produkts, das der Benutzer angibt, mit folgender Beschreibung" \
         " übereinstimmt:\n\n$goal_cond\n\nAntworte mit ja oder nein. Antworte nur mit einem Wort. Das Produkt:\n\n"


async def product_async(session, goal_condition, link):
    title, price, desc, condition, imgs = "", "", "", ["", ""], []
    async with session.get(link) as resp:
        soup = BeautifulSoup(await resp.read(), features="html.parser")

    title = soup.find(class_="ux-textspans ux-textspans--BOLD").get_text()
    price = soup.find(class_="x-price-primary").find('span').get_text()
    desc = soup.find(id="desc_ifr")["src"]
    imgs = soup.find_all(class_="ux-image-magnify__image--original")

    if not imgs:
        imgs = soup.find_all(class_="img-scale-down")
    for i in range(len(imgs)):
        try:
            imgs[i] = imgs[i]["src"]
        except:
            try:
                imgs[i] = imgs[i]["data-src"]
            except:
                ...
    condition[0] = soup.find(class_="x-item-condition-text").find('div') \
        .find('span').find('span').find('span').get_text()

    try:
        async with session.get(soup.find(id="desc_ifr")["src"]) as resp:
            desc_short = BeautifulSoup(
                await resp.read(),
                features="html.parser"
            ).find(class_="x-item-description-child").text
    except:
        desc_short = "Unavailable"

    payload = {
        'model': MODEL,
        'messages': [
            {"role": "system", "content": prompt.replace("$goal_cond", goal_condition)},
            {"role": "user", "content": f"{title};{desc_short}"}
        ]
    }
    try:
        async with session.post(
                url='https://api.openai.com/v1/chat/completions',
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_SECRET_KEY}"},
                json=payload,
                ssl=ssl.create_default_context(cafile=certifi.where())
        ) as response:
            response = await response.json()
        if "error" in response:
            print(f"OpenAI request failed with error {response['error']}")
        condition[1] = response['choices'][0]['message']['content'].upper().strip().strip(".")
    except Exception as e:
        print("Request failed:", e)

    return link, title, price, desc, condition, imgs


async def call_product_bulk(goal_condition, product_links):
    async with aiohttp.ClientSession() as session, asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(product_async(session, goal_condition, product_link)) for product_link in product_links]
    return await asyncio.gather(*tasks)


def get_item_links(query):
    soup = BeautifulSoup(requests.get(query).text, features="html.parser")
    links = [link["href"] for link in soup.find_all(class_="s-item__link")]
    return [link.split('?')[0] for link in links[1:]]


def search_store(goal_condition: str, query: str):
    return asyncio.run(call_product_bulk(goal_condition, get_item_links(query)))


@app.route("/")
def index():
    return open("index.html", "r").read()


@app.route("/search", methods=["POST"])
def search():
    html = open("product.html", "r").read()
    if not last_search[0] == f_req.json:
        last_search[0] = f_req.json
        last_search[1] = search_store(**f_req.json)
    return "".join(html
                   .replace("_$img_", imgs[0])
                   .replace("_$link_", link)
                   .replace("_$title_", title)
                   .replace("_$condition[0]_", condition[0])
                   .replace("_$condition[1]_", condition[1].upper())
                   .replace("_$price_", price)
                   .replace("_$desc_", desc)
                   for link, title, price, desc, condition, imgs in last_search[1])


last_search = ["", "", ""]
app.run("localhost", 8070)
