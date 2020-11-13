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

