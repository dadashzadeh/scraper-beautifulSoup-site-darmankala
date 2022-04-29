import concurrent.futures
import pandas as pd
import requests
from bs4 import BeautifulSoup

def send_request(single_url):
    global done
    data = requests.get(single_url)
    soup2 = BeautifulSoup(data.text, "lxml")
    dit[single_url] = soup2.find("h1").text
    dis[single_url] = soup2.find('meta', attrs={"name": "description"})['content']  # متا دیسکریپشن
    description[single_url] = soup2.find('div',attrs={"id": "tab_description_tabbed_contents"})  # توضیحات
    brand[single_url] = soup2.select("#product_addtocart_form > div.row > div.product-shop.col-sm-6 > div:nth-child(2) > a")[0].text
    availability[single_url] = soup2.find('meta',attrs={"property": "product:availability"})['content']  # وضعیت موجودی
    imageurl[single_url] = soup2.find("meta", attrs={"property": "og:image"})['content']  # عکس
    price[single_url] = soup2.find("meta", attrs={"property": "product:price:amount"})['content']  # قیمت
    done += 1
    print(done)

dit = {}
dis = {}
description = {}
brand = {}
availability = {}
imageurl = {}
price = {}
done = 0

name = input("name file = ")
address = input("address cat url = ")
tedad = int(input("number page cat = "))

productlinks = []
for x in range(1, tedad + 1):
    url = address.strip() + '?limit=36&p={}'.format(x)
    k = requests.get(url=url).text
    soup = BeautifulSoup(k, 'html.parser')
    productlist = soup.find_all("span", {"class": "product-name"})
    productlinks.extend([product.find("a").get('href') for product in productlist])

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(send_request, list(set(productlinks)))

# داده های اکسل
sss = pd.DataFrame({"h1": dit, "meta-dic": dis, "description": description, "brand": brand, "price": price,"imageurl": imageurl, "availability": availability})
sss.to_excel(name + '.xlsx')
