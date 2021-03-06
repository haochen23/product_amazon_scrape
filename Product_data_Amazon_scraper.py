from lxml import html
import csv
import os
import json
import requests
from time import sleep


def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)

    while True:

        try:
            doc = html.fromstring(page.content, parser=html.HTMLParser(encoding="utf-8"))
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//div[@id="burjOneTimePrice"]//span[@id="priceblock_ourprice"]//text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            # XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            print(doc.xpath(XPATH_SALE_PRICE))
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            # RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            # AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code != 200:
                raise ValueError('captha')
            data = {
                'NAME': NAME,
                'SALE_PRICE': SALE_PRICE,
                'CATEGORY': CATEGORY,
                'ORIGINAL_PRICE': ORIGINAL_PRICE,
                # 'AVAILABILITY': AVAILABILITY,
                'URL': url,
            }

            return data
        except Exception as e:
            print(e)


# AsinList = ['B00NB3PAGW',
#             'B00NB3PAP8',
#             'B001UFE1KY',
#             'B000ZM34MO',
#             'B001ILKJJ2',
#             'B009NNM3UU',
#             'B00NB3PBFM',
#             'B0198EXKY6',
#             'B01AJU4RGS',
#             'B075CRX3Z2',
#             'B005DB94T4',
#             'B00Y0YZWUA',
#             'B00NB3PBPW',
#             'B009NNM3UU']
with open('ASIN_list.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    AsinList = list(reader)


extracted_data = []
for i in AsinList:
    url = "http://www.amazon.com/dp/" + i
    print("Processing: " + url)
    extracted_data.append(AmzonParser(url))
    # sleep(10)
f = open('product_data.csv', 'a+')
writer = csv.writer(f)
writer.writerow(extracted_data[0].keys())
for row in extracted_data:
    writer.writerow(row.values())
f.close()
