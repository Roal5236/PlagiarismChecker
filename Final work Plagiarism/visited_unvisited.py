# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:40:05 2019

@author: rohaa
"""
import InvertedIndex as ii
import documentCrawler as dc
import getLinks as gl
import pymongo
import time
import hashlib 


myclient = pymongo.MongoClient("mongodb://localhost/27017")
 
def visited_unvisited():
    
    linkdb = myclient["Links"]
    unvisited = linkdb["unvisited"]
    visited = linkdb["visited"]
    
    unvisited.create_index([('encoded_link', pymongo.ASCENDING)])
    visited.create_index([('encoded_link', pymongo.ASCENDING)])


    
    if(unvisited.find({}).count()<=0):
        startz = "https://en.wikipedia.org/wiki/Main_Page"
        Links = gl.GetLinks(startz)
        
        for link in Links:
            result = str(hashlib.md5(link.encode()).hexdigest())
            if(visited.find({"encoded_link": result}).count()<=0 and unvisited.find({"encoded_link": result}).count()<=0):
                LinkDict  = {"Link": link, "encoded_link": result}
                unvisited.insert_one(LinkDict)
        
    i=1
    for linkDict in unvisited.find({}):
        
        if(visited.find({"encoded_link": linkDict["encoded_link"]}).count()<=0 and i<=10):
            print("\n\n")
            print(i)

            
            #Add the keywords to database
            dc.start(linkDict["Link"])
            
            #Add the new Links to the unvisited List
            Links = gl.GetLinks(linkDict["Link"])
            for link in Links:
                result = str(hashlib.md5(link.encode()).hexdigest())
                if(visited.find({"encoded_link": result}).count()<=0 and unvisited.find({"encoded_link": result}).count()<=0):
                    LinkDict  = {"Link": link, "encoded_link": result}
                    unvisited.insert_one(LinkDict)
            
            #Add to Visited Links
            LinkDict  = {"Link": link, "encoded_link": result}
            visited.insert_one(LinkDict)
            
            #Remove from Unvisited Links
            myquery = {"Link": link, "encoded_link": result}
            unvisited.delete_one(myquery) 
        
        i+=1
        
def reset_last():
    
    mydb = myclient["DataA"]
    mycol = mydb["keywords"]
    
    if(mycol.find({}).count()<=0):

        LastEleCol = myclient["last_db"]
        myLastElements = LastEleCol["LastElements"]
        
        
        #Get the last value added to the database
        GetLastElements = myLastElements.find({})
        keywordsValue = GetLastElements[0]["keywords"]
        postingValue = GetLastElements[0]["posting"]

        #Reset the last Value of the keywords 
        myquery = { "keywords": keywordsValue, "posting": postingValue }
        newvalues = { "$set": { "keywords": 1, "posting": 1 } }
        myLastElements.update_one(myquery, newvalues)
        
    
def remove_dataBases():
    myclient.drop_database('Links')  
    myclient.drop_database('DataA')    

    

start = time.time()

remove_dataBases()

reset_last()

visited_unvisited()

ii.InvertedIndex()  

end = time.time()
print(end - start)
