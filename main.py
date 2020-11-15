#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:44:56 2020

@author: ordovas
"""

import pandas as pd
from pymongo import MongoClient
from functions.filtering import *
from functions.api_crossmatch import *
from bson import ObjectId

from dotenv import load_dotenv
import os
import requests
import json
import time

client = MongoClient()



closest = filtering(client)

candidates = obtain_list(client,closest)


load_dotenv()
tk_google = os.getenv("GOOGLE_TOKEN")
id_4sq = os.getenv("FOURSQ_ID")
tk_4sq = os.getenv("FOURSQ_SEC")
#temporal_database/
candidates.to_csv('temporal_database/candidates_pre_apis.csv')

candidates=veg_info(candidates,id_4sq,tk_4sq)
candidates.to_csv('temporal_database/candidates_veg.csv')
candidates=basket_info(candidates,id_4sq,tk_4sq)
candidates.to_csv('temporal_database/candidates_basket.csv')
candidates=night_info(candidates,id_4sq,tk_4sq)
candidates.to_csv('temporal_database/candidates_night.csv')
candidates=daycare_info(candidates,id_4sq,tk_4sq)
candidates.to_csv('temporal_database/candidates_daycare.csv')
candidates=pet_info(candidates,id_4sq,tk_4sq)
candidates.to_csv('temporal_database/candidates_pet_4sq_end.csv')

candidates=airport_info(candidates,id_4sq,tk_4sq)
candidates.to_csv('temporal_database/candidates_airports_def.csv')

