#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 18:54:09 2020

@author: ordovas
"""
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
import time


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
    
def todollar(value): 
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

def create_db(client):
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



def filtering(client):
    db = client.get_database("companies")
    #Alias to not to write a lot
    

    offices =db.offices
    res = list(offices.find({},{"category_code":1,"total_money_raised":1,"offices.city":1,
                  "name":1,"offices.latitude":1,"offices.longitude":1,"category_code":1}))
    

    df=pd.DataFrame(res)
    df["cat_1m"] = df["total_money_raised"].apply(obtain_1m)
    df["cat_design"] = df["category_code"].apply(isfashion)
    df["cat_tech"] = df["category_code"].apply(istech)
    
    df["cat_tech"]=df["cat_tech"] & df["cat_1m"] 
    
    df=df[df["cat_design"] | df["cat_tech"]]
    df=pd.concat([df, df["offices"].apply(pd.Series)], axis=1, sort=False).drop(["offices"], axis=1)
    
    df=df[["_id","longitude","latitude","name","city","cat_tech","cat_design"]]
    df=df.reset_index()
    return df


def obtain_list(client,closest):
    db = client.get_database("companies")
    offices =db.offices
    nearest = []
    for lon, lat,idn,name_near in zip(closest["longitude"],closest["latitude"],closest["_id"],closest["name"]):
        point = {"type":"Point","coordinates":[lon,lat]}
        
        query ={
            "coord":{
                "$near":{
                    "$geometry":point,
                    "$maxDistance":1000,
                    "$minDistance":50
                }
            }
        }
        res = list(offices.find(query,{"offices.address1":1,"offices.address2":1,"offices.city":1,
                           "offices.latitude":1,"offices.longitude":1,"category_code":1}))
        
        #Add info for each entry of which is its neighbour
        for i in range(len(res)):
            res[i]["id_near"] = idn
            res[i]["name_near"] = name_near
        
        nearest.append(res)
        
    
    closest['nearest_list'] = nearest
    len_list=[]
    for a in nearest:
        len_list.append(len(a))
    
    closest['nearest_count'] = len_list
    
    df_candidates=pd.DataFrame(nearest[0])
    for element in nearest[1:]:
        df_temp=pd.DataFrame(element)
        df_candidates=df_candidates.append(df_temp, ignore_index=True)
    
    
    df_candidates=pd.concat([df_candidates, df_candidates["offices"].apply(pd.Series)], axis=1, sort=False)
    df_candidates=df_candidates.drop(['offices'], axis=1)
    
    df_candidates=df_candidates.reset_index()
    df_candidates=drop_repeated_coords(df_candidates)
    return df_candidates

def drop_repeated_coords(res):
    group_coords = lambda x: (x["longitude"] , x["latitude"])
    res["coords"] = res.apply(group_coords, axis=1)
    res = res.drop_duplicates(subset='coords', keep="first").reset_index()
    return res

