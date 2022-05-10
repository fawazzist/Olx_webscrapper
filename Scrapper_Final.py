#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv


# In[4]:


#if not deleted before running an error occurs already exists
import sys     
if "twisted.internet.reactor" in sys.modules: del sys.modules["twisted.internet.reactor"]


# In[5]:


class olx(scrapy.Spider):
    name = 'olx'
    
    url = 'https://www.olx.in/api/relevance/v2/search?category=1723&facet_limit=100&lang=en-IN&location=4058877&location_facet_limit=20&platform=web-desktop&size=40'
    
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        #'user-agent':'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620'
        }
    
    def __init__(self):
        with open('results.csv','w') as csv_file:
            csv_file.write('Property_Name,Property_Id,BreadCrumbs,Price,Location,Image_url,Description,Property_Type,Bathrooms,Bedrooms\n')
    
    def start_requests(self):
        for page in range(0,500):
            yield scrapy.Request(url = self.url + '&page=' + str(page), headers = self.headers, callback = self.parse)
        
    def parse(self, res):
        data = res.text
        #print(res)
        data = json.loads(data)
        
        
        for i in data['data']: # taking from the html key data
            items = {
                'Property_Name':i['title'],
                'Property_Id':i['id'],
                'BreadCrumbs': i['parameters'],
                'Price':{i['price']['value']['currency']['iso_4217']:i['price']['value']['display']},
                'Location': i['locations_resolved']['SUBLOCALITY_LEVEL_1_name'] + ', ' 
                + i['locations_resolved']['ADMIN_LEVEL_3_name'] + ', ' 
                + i['locations_resolved']['ADMIN_LEVEL_1_name'],              
                'Image_url':i['images'][0]['url'],
                'Description': i['description'].strip().replace('\n',' '),
                'Property_Type': i['parameters'][0]['value_name'],
                'Bathrooms': i['main_info'].split()[3],
                'Bedrooms': i['main_info'].split()[0]
                
                
            }
            
            with open('results.csv','a',encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames = items.keys())
                writer.writerow(items)
            

process = CrawlerProcess()
process.crawl(olx)
process.start() 


# In[6]:


import pandas as pd
df = pd.read_csv('results.csv')


# In[9]:


df2 =df


# In[11]:


df2['Bathrooms'] = df2['Bathrooms'].str.replace('4+','4',regex = False)
#df2['Bathrooms'].unique()
df2['Bedrooms'] = df2['Bathrooms'].str.replace('4+','4',regex = False)
#df2['Bedrooms'].unique()


# In[12]:


df['Bathrooms'] = df['Bathrooms'].str.replace('4+','4',regex = False)
df['Bedrooms'] = df['Bedrooms'].str.replace('4+','4',regex = False)


# In[13]:


df['Bathrooms'] = pd.to_numeric(df['Bathrooms'])
df['Bedrooms'] = pd.to_numeric(df['Bedrooms'])


# In[75]:


df.to_csv(r'results.csv', index=False)


# In[ ]:




