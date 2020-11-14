#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:44:56 2020

@author: ordovas
"""

import pandas as pd
from pymongo import MongoClient
from functions.filtering import *
from bson import ObjectId

from dotenv import load_dotenv
import os
import requests
import json

client = MongoClient()



closest = filtering(client)

res = obtain_list(client,closest)


load_dotenv()
tk_google = os.getenv("GOOGLE_TOKEN")
id_4sq = os.getenv("FOURSQ_ID")
tk_4sq = os.getenv("FOURSQ_SEC")


url = 'https://api.foursquare.com/v2/venues/explore'

params = dict(
client_id=id_4sq,
client_secret=tk_4sq,
v='20201114',
ll='40.4439108,-3.6608311',
#query='Airport',
limit=1,
categoryId="4bf58dd8d48988d1ed931735",
radius=100_000 
)
resp = requests.get(url=url, params=params)
data = json.loads(resp.text)
data["response"]["groups"][0]["items"][0]["venue"]['categories'][0]["id"]

data2["response"]["groups"][0]["items"][0]

params = dict(
client_id=id_4sq,
client_secret=tk_4sq,
v='20201114',
ll='40.8438668,-1.8847034',
#query='Airport',
limit=1,
categoryId="4bf58dd8d48988d1ed931735",
radius=100 
)
resp = requests.get(url=url, params=params)
data2= json.loads(resp.text)

"""
In [60]: len(data["response"]["groups"][0]["items"])
Out[60]: 1

In [61]: len(data2["response"]["groups"][0]["items"])
Out[61]: 0

In [66]: data["response"]["groups"][0]["items"][0]["venue"]["location"]["lat"]
Out[66]: 40.481654479394656
In [67]: data["response"]["groups"][0]["items"][0]["venue"]["location"]["lng"]
Out[67]: -3.578023910522461
In [68]: data["response"]["groups"][0]["items"][0]["venue"]["name"]
Out[68]: 'Aeropuerto Adolfo Suárez Madrid-Barajas (MAD) (Aeropuerto Adolfo Suárez Madrid-Barajas)'



"""