from bs4 import BeautifulSoup
from twilio.rest import Client
import requests

# Amazon Price Tracker
#This software aims to check the price of a given product and compare with a pre-determined price set by me
#In case the price offered is ideal, it'll send me an SMS message with the price and link for me to buy it
#I am of course removing all sensitive information from it
URL_target = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
desired_price = 100.00
my_phone_number = "insertyourNUMBER"
account_sid = 'insertyourSID'
auth_token = 'insertyourTOKEN'

response = requests.get(url=URL_target, headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})

soup = BeautifulSoup(response.text, 'html.parser')
#Scraping the Amazon website for the price
price = soup.find(class_="aok-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)
#Scraping the Amazon website for the product name
product_Title = soup.find(id="productTitle").get_text()
print(product_Title)
#Sending an SMS to myself using twilio
#Through a message to my cellphone in case the price is lower
if price_as_float < desired_price:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='+19546377166',
        body=f'Your product is for sale, please buy now {product_Title} at {URL_target} for only {price_as_float}',
        to= my_phone_number
    )
    print(message.status)
print(soup.prettify())
