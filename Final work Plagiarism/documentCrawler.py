# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:42:54 2019

@author: rohaa
"""
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from nltk.corpus import stopwords
import collections
import pymongo
import operator 
import getLinks as gl
import webcrawler as wc



def start(url): 
    
    #Get the words from the website
    word_list = wc.start(url)
    
    #Remove stop words and Unnecessary Symbols
    removed_words = remove_unnecessary(word_list)
    
    #lemmatizatoin of the words
    Lemma_list = lemma_wordlist(removed_words)
    
    #Creates a dictionary with word and Word Frequency
    create_dict = create_dictionary(Lemma_list) 
    
    #remove Irrelevant words(words with frequency less than 5)
    RemoveIWords = remove_Irrelevant_Words(create_dict)
    
    #Add the dictionary to the database
    add_database(RemoveIWords, url)
    
    
def add_database(word_dict, url):
    
    #Database Info(Collection Name)
    myclient = pymongo.MongoClient("mongodb://localhost/27017")
    mydb = myclient["DataA"]
    mycol = mydb["keywords"]
    myDocs = mydb['myDocs']
    
    LastEleCol = myclient["last_db"]
    myLastElements = LastEleCol["LastElements"]

    
    
    #Get the id of the Last Element Added
    last=mycol.find({}).sort([("_id",-1)]).limit(1)
    
    
    #Get the last value added to the database
    if(last.count()>0):
        k = last[0]["_id"]+1
    else:
        k=1
    word_dict["_id"]=k
    
    #insert Into Database
    mycol.insert_one(word_dict)
    TempDocDict = {"_id": k, "url": url}
    myDocs.insert_one(TempDocDict)
    print("Row Added")
    
    #Append the last Value of the keywords 
    myquery = { "keywords": k }
    newvalues = { "$set": { "keywords": k+1 } }
    myLastElements.update_one(myquery, newvalues)
    
    

def remove_unnecessary(word_list):
    
    removed_symbols = []
    
    #List of stopwords from nltk
    stop_words = set(stopwords.words('english'))
    stop_words.add('')
    stop_words.add('/')
    
    unnecessary_words = [w for w in word_list if not w in stop_words]

    #Removing Unnecessary Symbols
    for word in unnecessary_words: 
        symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/.,¿`•\''
          
        for i in range (0, len(symbols)): 
            word = word.replace(symbols[i], ' ')
        
        if(' ' in word):
            tempWordSplit = word.split(' ')
            word = word.strip()
            for tempWords in tempWordSplit:
                removed_symbols.append(tempWords)  

        if len(word) > 1: 
            removed_symbols.append(word)  
        
    print('Symbols Removed')
    return removed_symbols




def create_dictionary(word_list): 
    word_count = {} 
      
    for word in word_list: 
        if word in word_count: 
            word_count[word] += 1
        else: 
            word_count[word] = 1
        
            
    print('Dictionary Created')
    sorted_x = sorted(word_count.items(), key=operator.itemgetter(1))
    sorted_dict = collections.OrderedDict(sorted_x)
    return sorted_dict        


def remove_Irrelevant_Words(word_list):
    final_word_count={}
    for word in word_list:
        temp = word_list[word]
        if(temp>0):
            final_word_count[word]=temp

    return final_word_count


def lemma_wordlist(word_list):
    lemmatizer = lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    Lemma_list = []
    
    for word in word_list:
        lWord = lemmatizer(word, u"NOUN")
        Lemma_list.append(lWord[0])
        
    return Lemma_list
    

