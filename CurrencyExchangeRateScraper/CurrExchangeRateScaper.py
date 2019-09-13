# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:13:44 2019

@author: Umaima
"""

import requests
from bs4 import BeautifulSoup
import json
import datetime

# Foriengn currency exchange rate against USD scraper 

def ExchangeRateAgainstUSD():
    
    print("In currency exchange Page");
    
    list_c = []
    list_r = []
    
    page = requests.get('https://transferwise.com/in/currency-converter/')
    soup = BeautifulSoup(page.content, 'lxml')
    
    table = soup.find('table', class_ = 'table table-condensed')
    
    tr_heading = table.find_all('tr')[0]
    tr_1 = tr_heading.find_all('th')
    
    
    for th in tr_1:
        data = th.find('span', class_ = "sr-only")
        if data != None:
            list_c.append(data.get_text())
    
    tr_rate = table.find_all('tr')[3]
    tr_2 = tr_rate.find_all('td')
    
    for td in tr_2:
        data1 = td.find('span')
        if data1 !=None:
            list_r.append(data1.get_text())
        else:
            
            data2 = td.find('a', class_ = "js-TopCurrenciesLink currency-table__link")
            if data2 != None:
                list_r.append(data2.get_text())
            
#    print(list_c)
#    print(list_r)
    
    res = []
    
    for i in range(0, len(list_c)):
      
        data = {
                    'ExchangeRate': list_r[i],
                    'CurrencyCode': list_c[i],
                }
        
        res.append(data)
    
    date = datetime.date.today().strftime('%d-%m-%Y')
    filename = 'ExchangeRateUSD-' + date + '.json'
    f=open(filename,'w')
    json.dump(res,f,indent=4)
    
    
if __name__ == "__main__":
    ExchangeRateAgainstUSD()
    