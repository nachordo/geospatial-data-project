#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 18:54:09 2020

@author: ordovas
"""
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId


def obtain_1m(value):
    
    if (value[-1] == "M") or (value[-1] == "k"):
        number=todollar(value)
        if value[-1] == "M":
            number*=1e6
        else:
            number*=1e3
        if number > 1e6:
            return True
        else:
            return False
        
    else:
        return False
    
def isfashion(value):
    return (value == "fashion") or (value == "design")

def istech(value):
    tech = (value == "web") or (value == "software") or  (value == "games_video") or (value == "mobile") or (value == "network_hosting") or (value == "ecommerce") or (value == "nanotech")     
    return tech
    
def todollar(value):  #0.12 kr
    if value[0] == "$":
        return float(value[1:-1])
    elif value[0] == "€":
        return float(value[1:-1]) * 1.18
    elif value[0] == "£":
        return float(value[1:-1]) * 1.32
    elif value[0] == "C":
        return float(value[2:-1]) * 0.76
    elif value[0] == "k":
        return float(value[2:-1]) * 0.12
    else:
        return 0

def filtering(client):
    db = client.get_database("companies")
    #Alias to not to write a lot
    comp = db.companies
    
    #We need to get the info of each diffetent office to crossmatch
    #the different conditions that we need in this exercise.
    
    #To do so, we unfold the companies that have several offices and save it 
    #in a new MongoDB collection. We exclude those documents that there
    #is not office coordinates available
    
    comp_agg = comp.aggregate([ {"$unwind":"$offices" },
                               {"$match":{"offices.latitude":{"$ne":None}}}, 
                               {"$match":{"offices.longitude":{"$ne":None}}}, 
                               {"$match":{"offices.city":{"$ne":None}}}, 
                               {"$project":{"_id":0}} ])
    
    
    #Storing this new database in "offices" inside "companies"
    
    db.offices.insert_many(comp_agg)
    offices =db.offices

    
    res = list(offices.find({},{"category_code":1,"total_money_raised":1,"offices.city":1,
                           "offices.latitude":1,"offices.longitude":1,"category_code":1}))
    
    #Adding point coordinates
    for c in res:
        filt = {"_id":c["_id"]}
        coord = {
                  "type": "Point",
                  "coordinates": [c["offices"]["longitude"], c["offices"]["latitude"]]
                }
        update = {"$set":{"coord":coord}}
        offices.update_one(filt,update)
        
    df=pd.DataFrame(res)
    df["cat_1m"] = df["total_money_raised"].apply(obtain_1m)
    df["cat_design"] = df["category_code"].apply(isfashion)
    df["cat_tech"] = df["category_code"].apply(istech)
    
    df["cat_tech"]=df["cat_tech"] & df["cat_1m"] 
    
    df=df[df["cat_design"] | df["cat_tech"]]
    df=pd.concat([df, df["offices"].apply(pd.Series)], axis=1, sort=False).drop(["offices"], axis=1)
    
    return df[["longitude","latitude","cat_tech","cat_design"]]

