# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:39:26 2019

@author: rohaa
"""

import requests 
from bs4 import BeautifulSoup 
from collections import Counter 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymongo
import re


def start(url): 
    
    myclient = pymongo.MongoClient("mongodb://localhost/27017")
    mydb = myclient["DataA"]
    mycol = mydb["keywords"]
    
    
    #Get the id of the Last Element Added
    last=mycol.find({}).sort([("_id",-1)]).limit(1)
    
    
    #Get the last value added to the database
    doc_no=1
    
    if(last.count()>0):
        doc_no = last[0]["_id"]+1
        
  
    source_code = requests.get(url).text 
    soup = BeautifulSoup(source_code, 'html.parser') 
    print("html fetched")
    
    name = "X/"+str(doc_no)+".txt"
    
    File_object = open(name,"w+", encoding='utf8', errors='ignore')

    AllWords=[]
    Sentances = []

    text_returned=soup.findAll('p')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip())            
                   
    text_returned=soup.findAll('a')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h1')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h2')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h3')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h4')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h5')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h6')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip())  
                
    text_returned=soup.findAll('li')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip())  
       
    final_sent=''         
    for sent in Sentances:
        final_sent = final_sent+sent
        
    File_object.write(final_sent)
    
    File_object.close()
           
    return AllWords

# Driver code 
if __name__ == '__main__': 
        link = "https://en.wikipedia.org/wiki/Main_Page"
        start(link)