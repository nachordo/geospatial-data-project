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
        # Obtaining the number in dollars
        number=todollar(value)
        #Define if it is in M or k and multiply it
        if value[-1] == "M":
            number*=1e6
        else:
            number*=1e3
        #If it is higher than 1M return true
        if number > 1e6:
            return True
        else:
            return False
    # If the money isnt marked with M or k return false    
    else:
        return False
    
def isfashion(value):
    # Returns True when the category is design related
    return (value == "fashion") or (value == "design")

def istech(value):
    # Returns True when the category is tech related
    tech = (value == "web") or (value == "software") or  (value == "games_video") or (value == "mobile") or (value == "network_hosting") or (value == "ecommerce") or (value == "nanotech")     
    return tech
    
def todollar(value): 
    # Converts the currency to US dollars
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
    # Alias to not to write a lot
    comp = db.companies
    # We need to get the info of each diffetent office to crossmatch
    # the different conditions that we need in this exercise.
    
    # To do so, we unfold the companies that have several offices and save it 
    # in a new MongoDB collection. We exclude those documents that there
    # is not office coordinates available

    comp_agg = comp.aggregate([ {"$unwind":"$offices" },
                               {"$match":{"offices.latitude":{"$ne":None}}}, 
                               {"$match":{"offices.longitude":{"$ne":None}}}, 
                               {"$match":{"offices.city":{"$ne":None}}}, 
                               {"$project":{"_id":0}} ])
    
    
    # Storing this new database in "offices" inside "companies"
    
    db.offices.insert_many(comp_agg)
    offices =db.offices
    res = list(offices.find({},{"category_code":1,"total_money_raised":1,"offices.city":1,
                           "offices.latitude":1,"offices.longitude":1,"category_code":1}))
      
    # Adding point coordinates
    for c in res:
        filt = {"_id":c["_id"]}
        coord = {
                  "type": "Point",
                  "coordinates": [c["offices"]["longitude"], c["offices"]["latitude"]]
                }
        update = {"$set":{"coord":coord}}
        offices.update_one(filt,update)



def filtering(client):
    # Load the companies dataset
    db = client.get_database("companies")
    # Define an alias for the offices dataset
    offices =db.offices
    # Obtain only the desired info for each office
    res = list(offices.find({},{"category_code":1,"total_money_raised":1,"offices.city":1,
                  "name":1,"offices.latitude":1,"offices.longitude":1,"category_code":1}))
    
    # Converting to DataFrame to apply sonme filters
    df=pd.DataFrame(res)
    # Adding a boolean column for companies that make >1M$
    df["cat_1m"] = df["total_money_raised"].apply(obtain_1m)
    # Boolean column to mark the design related companies
    df["cat_design"] = df["category_code"].apply(isfashion)
    # Boolean column to mark the tech related companies
    df["cat_tech"] = df["category_code"].apply(istech)
    # Combine the >1M$ and tech conditions
    df["cat_tech"]=df["cat_tech"] & df["cat_1m"] 
    
    # Trim the DataFrame to only the values where at least one condition is met
    df=df[df["cat_design"] | df["cat_tech"]]
    # Extract the keys inside "offices" to create conlumns for each one
    df=pd.concat([df, df["offices"].apply(pd.Series)], axis=1, sort=False).drop(["offices"], axis=1)
    
    # Return only the DataFrame with the desired info and its index reseted
    df=df[["_id","longitude","latitude","name","city","cat_tech","cat_design"]]
    df=df.reset_index()
    return df


    
def obtain_list(client,closest):
    # Load the companies collection
    db = client.get_database("companies")
    # Define an alias for the offices dataset
    offices =db.offices
    # Creating a list of the nearest locations info
    nearest = []
    for lon, lat,idn,name_near in zip(closest["longitude"],closest["latitude"],closest["_id"],closest["name"]):
        # Dict with the point coordinates
        point = {"type":"Point","coordinates":[lon,lat]}
        
        # Define query dictionary to search within a 1km radius
        # excluding a 50m inner radius
        query ={
            "coord":{
                "$near":{
                    "$geometry":point,
                    "$maxDistance":1000,
                    "$minDistance":50
                }
            }
        }

        # Query the rearest locations
        res = list(offices.find(query,{"offices.address1":1,"offices.address2":1,"offices.city":1,
                           "offices.latitude":1,"offices.longitude":1,"category_code":1}))
        
        # Add info for each entry of which is its neighbour
        for i in range(len(res)):
            res[i]["id_near"] = idn
            res[i]["name_near"] = name_near
        
        # Store the query
        nearest.append(res)
        
    # Add a column with the nearest
    closest['nearest_list'] = nearest
    len_list=[]
    for a in nearest:
        len_list.append(len(a))
    
    # Add a column with the count
    closest['nearest_count'] = len_list
    
    # Append all the locations near each neighbouring company
    # to obtain a DataFrame with all the location candidates wiht
    # a company that meets one of the conditions
    df_candidates=pd.DataFrame(nearest[0])
    for element in nearest[1:]:
        df_temp=pd.DataFrame(element)
        df_candidates=df_candidates.append(df_temp, ignore_index=True)
    
    # Convert the dictionary elements in offices into new columns
    df_candidates=pd.concat([df_candidates, df_candidates["offices"].apply(pd.Series)], axis=1, sort=False)
    df_candidates=df_candidates.drop(['offices'], axis=1)
    
    # Reseting the index and calling a function to delete locations
    # with the same coordinates
    df_candidates=df_candidates.reset_index()
    df_candidates=drop_repeated_coords(df_candidates)
    return df_candidates

def drop_repeated_coords(res):
    # Creating a function to create a new column with a coordinate tuple
    group_coords = lambda x: (x["longitude"] , x["latitude"])
    res["coords"] = res.apply(group_coords, axis=1)
    # Remove the duplicated coordinates to obtain only a DataFrame
    # with non repeated coordinates for the desired location
    res = res.drop_duplicates(subset='coords', keep="first").reset_index()
    return res

