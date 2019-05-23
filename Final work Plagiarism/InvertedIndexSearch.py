# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:28:15 2019

@author: rohaa
"""

import pymongo
import documentCrawler as dc
from nltk.tokenize import word_tokenize
from collections import Counter 
import documentCrawler as dc

def InvertedIndexSearch():
    myclient = pymongo.MongoClient("mongodb://localhost/27017")
    mydb = myclient["DataA"]
    Posting = mydb["Posting"]
    Diction = mydb["Diction"]
    
    raw = open('Test_document.txt').read().lower()
    
    #Tokenizing the words
    tokens = word_tokenize(raw)
    words = [w.lower() for w in tokens]
    
    #Remove stop words and Unnecessary Symbols
    removed_words = dc.remove_unnecessary(words)
    
    #lemmatizatoin of the words
    Lemma_list = dc.lemma_wordlist(removed_words)
    
    #Creates a dictionary with word and Word Frequency
    create_dict = dc.create_dictionary(Lemma_list)     
    
    
    
    ArrayOfRelevantDocuments = []
    
    ArrayOfMinDocuments = []
    
    for word,freq in create_dict.items():
        diction_words = Diction.find({"Term": word})
        for row in diction_words:
            TempDict= {"Term":row['Term'], "Total":row["Total"]}
            ArrayOfMinDocuments.append(TempDict)

    SortedArrayMinDoc = sorted(ArrayOfMinDocuments, key = lambda i: i['Total'])

    
    
    for word in SortedArrayMinDoc:
        x = Posting.find({"Term": word["Term"]})
        for row in x:
            ArrayOfRelevantDocuments.append(row["DocId"])
    
    
    DocArrayDocRite = dc.create_dictionary(ArrayOfRelevantDocuments)
    print(DocArrayDocRite)
    
    finalDocArray = []
    for key, val in DocArrayDocRite.items():
        finalDocArray.append(key)
        
        
                
    return finalDocArray
    
   
    
 
