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

def obtain_dist(city_a,city_b):
    citya_in_radians = [radians(_) for _ in city_a]
    cityb_in_radians = [radians(_) for _ in city_b]
    result = haversine_distances([citya_in_radians, cityb_in_radians])
    return result[0][1] * 6371000
    

def sigmoid(d,c1,c2):
    return 1./(1. + np.exp(-c1 * (c2 - d)))


def obtain_closer_data(client,id_near):
    db = client.get_database("companies")
    #Alias to not to write a lot

    offices =db.offices
    res = list(offices.find({"_id":ObjectId(id_near)},{"name":1,"offices.latitude":1,"offices.longitude":1,"category_code":1}))    
    return res
