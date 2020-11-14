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



client = MongoClient()



closest = filtering(client)

res = obtain_list(client,closest)


            

"""
OperationFailure: error processing query: ns=companies.officesTree: GEONEAR  field=coord maxdist=100000 isNearSphere=0
Sort: {}
Proj: { offices: 1 }
 planner returned error :: caused by :: unable to find index for $geoNear query, full error: {'ok': 0.0, 'errmsg': 'error processing query: ns=companies.officesTree: GEONEAR  field=coord maxdist=100000 isNearSphere=0\nSort: {}\nProj: { offices: 1 }\n planner returned error :: caused by :: unable to find index for $geoNear query', 'code': 291, 'codeName': 'NoQueryExecutionPlans'}
"""