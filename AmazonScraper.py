# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:14:06 2019

@author: Umaima
"""

import requests
from bs4 import BeautifulSoup
import json

def AmazonScraper(url):
    
    res = requests.get(url)
    #print(res.status_code)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    
    NAME = soup.find('h1').get_text().strip()
    #print(NAME)
    
    AVAILABILITY = soup.find(id = 'availability').get_text().strip().split("  ")[0].strip()
    #print(AVAILABILITY)
    
    if AVAILABILITY != 'Currently unavailable.':
        RAW_SALE_PRICE = soup.find(id = 'priceblock_ourprice')
        SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE.get_text()).split()).strip().replace('₹ ', '') if RAW_SALE_PRICE else None
        #print(SALE_PRICE) 
        RAW_ORIGINAL_PRICE = soup.find(class_ = 'priceBlockStrikePriceString a-text-strike').get_text().strip()
        ORIGINAL_PRICE = ' '.join(''.join(RAW_ORIGINAL_PRICE).split()).strip().replace('₹ ', '')
        #print(ORIGINAL_PRICE)
        CATEGORY_S = soup.find(class_ = 'a-list-item')
        CATEGORY = CATEGORY_S.find(class_ = 'a-link-normal a-color-tertiary').get_text().strip()
        #print(CATEGORY)
    else:
        SALE_PRICE = 'NA'
        ORIGINAL_PRICE = 'NA'
        CATEGORY = 'NA'
       
    data = {
                'NAME':NAME,
                'SALE_PRICE':SALE_PRICE,
                'CATEGORY':CATEGORY,
                'ORIGINAL_PRICE':ORIGINAL_PRICE,
                'AVAILABILITY':AVAILABILITY,
                'URL':url,
                }
    
    return data

def ReadProducts():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    ProductList = ['B00PFJ00U6',
                   'B07D5V12Y8',
                   'B010D771GK',
                   'B01LQQHI8I',
                   'B077RV8CCY']
    
    extracted_data = []
    for i in ProductList:
        url = "https://www.amazon.in/dp/"+i
        print("Processing: "+url)
        extracted_data.append(AmazonScraper(url))
        #time.sleep(5)
        
    f=open('amazondata.json','w')
    json.dump(extracted_data,f,indent=4)


if __name__ == "__main__":
    ReadProducts()