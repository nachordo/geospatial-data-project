#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:12:37 2020

@author: ordovas
"""

import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import numpy as np
from pymongo import MongoClient
from bson import ObjectId
import time

# Obtain the haversine distance between two places
def obtain_dist(c_a,c_b):
    # Convert angle to radians 
    ca_in_radians = [radians(_) for _ in c_a]
    cb_in_radians = [radians(_) for _ in c_b]
    # Obtain the haversine distance
    result = haversine_distances([ca_in_radians, cb_in_radians])
    return result[0][1] * 6371000
    
# Sigmoid function
def sigmoid(d,c1,c2):
    return 1./(1. + np.exp(-c1 * (c2 - d)))


# Obtain info about the neighbour
def obtain_closer_data(client,id_near):
    db = client.get_database("companies")
    #Alias to not to write a lot

    offices =db.offices
    res = list(offices.find({"_id":ObjectId(id_near)},{"name":1,"offices.latitude":1,"offices.longitude":1,"category_code":1}))    
    return res

#Function to obtain the score of each location
def obtain_score(df):
    n=len(df)
    score = np.ones(n)
    
    for i in range(n):
        #Airport ckeck
        if df["has_airport"][i]:
            score[i] += 1.
        #Vegan check
        if df["has_veg"][i]:
            score[i] += ( df["num_veg"][i] / 10) * 0.5
            dist = obtain_dist([df["latitude"][i], df["longitude"][i]]
                                    ,df["coord_veg"][i])
            score[i] += sigmoid(dist,0.25,100) * 0.5
        #Child daycare check
        if df["has_daycare"][i]:
            dist = obtain_dist([df["latitude"][i], df["longitude"][i]]
                                    ,df["coord_daycare"][i])
            score[i] += sigmoid(dist,0.25,250) 
        #Basket stadium check
        if df["has_basket"][i]:
            score[i] += 1.
        #Nightlife check
        if df["has_night"][i]:
            score[i] += (df["num_night"][i] / 20) *0.5  
            dist = obtain_dist([df["latitude"][i], df["longitude"][i]]
                                    ,df["coord_night"][i])
            score[i] += sigmoid(dist,0.25,100) * 0.5 
        #Pet care check
        if df["has_pet"][i]:
            dist = obtain_dist([df["latitude"][i], df["longitude"][i]]
                                    ,df["coord_pet"][i])
            score[i] += sigmoid(dist,0.25,250) 
            
    
    return pd.Series(score)
