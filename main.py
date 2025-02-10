from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# headers= {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6,mr;q=0.5",
#     "Priority": "u=0, i",
#     "Sec-Ch-Ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "\"Windows\"",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "cross-site",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    
#   }

headers = {
    
    "aws-ubid-main" : "763-3631235-3422301",
    
}

response = requests.get(url="https://www.amazon.in/dp/B0DSBTKP5Q",headers=headers)
amazon_web_page = response.text

soup = BeautifulSoup(amazon_web_page,"html.parser")
list_of_price = soup.find_all(name="span",class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")

# for i in list_of_price:
#     price = i.getText()
# print(price)
        # Or
price = list_of_price[0].getText()

price_without_symbol = price.split("₹")[1]
price_without_comma = "".join(price_without_symbol.split(","))
current_price = int(price_without_comma)




MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")

# Create email message with UTF-8 encoding
html_content = f"""<p>"Samsung Galaxy S25 Ultra 5G AI Smartphone (Titanium Silverblue, 12GB RAM, 512GB Storage), 200MP Camera, S Pen Included, Long Battery Life of price : \n {current_price } ₹"
<a href= "https://www.amazon.in/dp/B0DSBTKP5Q" >here is the link </a> </p>"""

message = MIMEText(
    
    html_content,
    "html", 
    "utf-8"
)
message["Subject"] = "Amazon price traker"


if current_price < 150000:
    with smtplib.SMTP(SMTP_ADDRESS, 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL,password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,to_addrs="josephtelang30@Yahoo.com",msg=message.as_string())

