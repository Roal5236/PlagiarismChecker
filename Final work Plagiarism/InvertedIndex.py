# -*- coding: utf-8 -*-
"""
Created on Tue May 21 21:25:38 2019

@author: rohaa
"""

import pymongo

def InvertedIndex():
    
    print("Building InvertedIndex")
    myclient = pymongo.MongoClient("mongodb://localhost/27017")
    mydb = myclient["DataA"]
    mycol = mydb["keywords"]
    Diction = mydb["Diction"]
    Posting = mydb["Posting"]
    
    Diction.create_index([('Term', pymongo.ASCENDING)])

    
    LastEleCol = myclient["last_db"]
    LastElements = LastEleCol["LastElements"]

    last=LastElements.find({}).limit(1)
    
    if(last.count()>0):
        last_posting_index = last[0]["posting"]
    else:
        last_posting_index=1
        
    
    TotalNumDocumnets = mycol.find({"_id" : { "$gte": last_posting_index }})
    
    
    k=0
    for word_dict in TotalNumDocumnets:
        for word, freq in word_dict.items():
            i=0
            j=0
            TempF = {}
            for n in mycol.find({}, {word : 1}):
                if(len(n)>1):
                    i+=1
                    j+=n[word]
            TempF["Term"]=word
            TempF["Docs"]=i
            TempF["Total"]=j
            if(i>0 and j>0 and i/j<0.2):
                Diction.insert_one(TempF)
                
            TempPosting = {}
            TempPosting["Term"] = word
            TempPosting["DocId"] = last_posting_index
            Posting.insert_one(TempPosting)    

            k+=1
            print(k)
        last_posting_index+=1
        
    myquery = { "posting": last[0]["posting"] }
    newvalues = { "$set": { "posting": last_posting_index } }

    LastElements.update_one(myquery, newvalues)


    
