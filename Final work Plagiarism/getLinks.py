# -*- coding: utf-8 -*-
"""
Created on Fri May 17 17:47:42 2019

@author: rohaa
"""
import requests 
from bs4 import BeautifulSoup 

def GetLinks(url): 
    unvisitedLinks = []
  
    # the website fetched from our web-crawler 
    source_code = requests.get(url).text 
  
    # BeautifulSoup object which will 
    soup = BeautifulSoup(source_code, 'html.parser') 
    print("html fetched")
    
    
    for link in soup.findAll('a'):
        tempLink = str(link.get('href'))
        if(tempLink.startswith('https://en.') or tempLink.startswith('/')):
            if(tempLink.startswith('https://')):
                #print(tempLink)
                #print("\n")
                unvisitedLinks.append(tempLink)
                
            elif(tempLink.startswith('//')):
                pass
                
            else:
                #print(tempLink)
                #print("\n")
                base_url = "https://en.wikipedia.org"
                tempLink = base_url+tempLink
                unvisitedLinks.append(tempLink)

    return unvisitedLinks

