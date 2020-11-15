#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:12:37 2020

@author: ordovas
"""

import pandas as pd
from bson import ObjectId
import requests
import json
import time

def airport_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    has_airport=[]
    name_airport=[]
    coord_airpott=[]
    for i in range(len(df)):
        if i%25==0:
            print("Airport",i,len(df)-i)
        time.sleep(2)
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="4bf58dd8d48988d1ed931735",
        radius=30_000 
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        if len(data["response"])>0:
            if len(data["response"]["groups"][0]["items"]) > 0:
                
                has_airport.append([True])
                name_airport.append([data["response"]["groups"][0]["items"][0]["venue"]["name"]])
                coord_airpott.append([ data["response"]["groups"][0]["items"][0]["venue"]["location"]["lng"] , 
                                      data["response"]["groups"][0]["items"][0]["venue"]["location"]["lat"]])
            else:
                has_airport.append([False])
                name_airport.append([None])
                coord_airpott.append([ None, None ])
        else:
            has_airport.append([False])
            name_airport.append([None])
            coord_airpott.append([ None, None ])
    df["has_airport"]=pd.Series(has_airport)
    df["name_airport"]=pd.Series(name_airport)
    df["coord_airpott"]=pd.Series(coord_airpott)
    return df

def basket_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    has_basket=[]
    name_basket=[]
    coord_basket=[]
    for i in range(len(df)):
        if i%25==0:
            print("Basket",i,len(df)-i)
        time.sleep(2)
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="4bf58dd8d48988d18b941735",
        radius=10_000 
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        if len(data["response"])>0:
            if len(data["response"]["groups"][0]["items"]) > 0:
                
                has_basket.append([True])
                name_basket.append([data["response"]["groups"][0]["items"][0]["venue"]["name"]])
                coord_basket.append([ data["response"]["groups"][0]["items"][0]["venue"]["location"]["lng"] , 
                                      data["response"]["groups"][0]["items"][0]["venue"]["location"]["lat"]])
            else:
                has_basket.append([False])
                name_basket.append([None])
                coord_basket.append([ None, None ])
        else:
            has_basket.append([False])
            name_basket.append([None])
            coord_basket.append([ None, None ])
    df["has_basket"]=pd.Series(has_basket)
    df["name_basket"]=pd.Series(name_basket)
    df["coord_basket"]=pd.Series(coord_basket)
    return df




def veg_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    has_veg=[]
    name_veg=[]
    coord_veg=[]
    num_veg=[]
    for i in range(len(df)):
        if i%25==0:
            print("Vegan",i,len(df)-i)
        time.sleep(2)
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=10,
        categoryId="4bf58dd8d48988d1d3941735",
        radius=500 
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        if len(data["response"])>0:
            if len(data["response"]["groups"][0]["items"]) > 0:
                num_veg.append([len(data["response"]["groups"][0]["items"])])
                has_veg.append([True])
                name_veg.append([data["response"]["groups"][0]["items"][0]["venue"]["name"]])
                coord_veg.append([ data["response"]["groups"][0]["items"][0]["venue"]["location"]["lng"] , 
                                      data["response"]["groups"][0]["items"][0]["venue"]["location"]["lat"]])
            else:
                num_veg.append([0])
                has_veg.append([False])
                name_veg.append([None])
                coord_veg.append([ None, None ])
        else:
            num_veg.append([-1])
            has_veg.append([False])
            name_veg.append([None])
            coord_veg.append([ None, None ])
    df["has_veg"]=pd.Series(has_veg)
    df["name_veg"]=pd.Series(name_veg)
    df["coord_veg"]=pd.Series(coord_veg)
    df["num_veg"]=pd.Series(num_veg)
    return df

def night_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    has_night=[]
    name_night=[]
    coord_night=[]
    num_night=[]
    for i in range(len(df)):
        if i%25==0:
            print("Night",i,len(df)-i)
        time.sleep(2)
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=20,
        categoryId="4d4b7105d754a06376d81259",
        radius=2000 
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        if len(data["response"])>0:
            if len(data["response"]["groups"][0]["items"]) > 0:
                num_night.append([len(data["response"]["groups"][0]["items"])])
                has_night.append([True])
                name_night.append([data["response"]["groups"][0]["items"][0]["venue"]["name"]])
                coord_night.append([ data["response"]["groups"][0]["items"][0]["venue"]["location"]["lng"] , 
                                      data["response"]["groups"][0]["items"][0]["venue"]["location"]["lat"]])
            else:
                num_night.append([0])
                has_night.append([False])
                name_night.append([None])
                coord_night.append([ None, None ])
        else:
            num_night.append([-1])
            has_night.append([False])
            name_night.append([None])
            coord_night.append([ None, None ])
    df["has_night"]=pd.Series(has_night)
    df["name_night"]=pd.Series(name_night)
    df["coord_night"]=pd.Series(coord_night)
    df["num_night"]=pd.Series(num_night)
    return df



def daycare_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    has_daycare=[]
    name_daycare=[]
    coord_daycare=[]
    for i in range(len(df)):
        if i%25==0:
            print("Daycare",i,len(df)-i)
        time.sleep(2)
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="4f4532974b9074f6e4fb0104",
        radius=1_000 
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        if len(data["response"])>0:
            if len(data["response"]["groups"][0]["items"]) > 0:
                
                has_daycare.append([True])
                name_daycare.append([data["response"]["groups"][0]["items"][0]["venue"]["name"]])
                coord_daycare.append([ data["response"]["groups"][0]["items"][0]["venue"]["location"]["lng"] , 
                                      data["response"]["groups"][0]["items"][0]["venue"]["location"]["lat"]])
            else:
                has_daycare.append([False])
                name_daycare.append([None])
                coord_daycare.append([ None, None ])
        else:
            has_daycare.append([False])
            name_daycare.append([None])
            coord_daycare.append([ None, None ])
    df["has_daycare"]=pd.Series(has_daycare)
    df["name_daycare"]=pd.Series(name_daycare)
    df["coord_daycare"]=pd.Series(coord_daycare)
    return df



def pet_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    has_pet=[]
    name_pet=[]
    coord_pet=[]
    for i in range(len(df)):
        if i%25==0:
            print("Pet",i,len(df)-i)
        time.sleep(2)
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="5032897c91d4c4b30a586d69",
        radius=1_000 
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        if len(data["response"])>0:
            if len(data["response"]["groups"][0]["items"]) > 0:
                
                has_pet.append([True])
                name_pet.append([data["response"]["groups"][0]["items"][0]["venue"]["name"]])
                coord_pet.append([ data["response"]["groups"][0]["items"][0]["venue"]["location"]["lng"] , 
                                      data["response"]["groups"][0]["items"][0]["venue"]["location"]["lat"]])
            else:
                has_pet.append([False])
                name_pet.append([None])
                coord_pet.append([ None, None ])
        else:
            has_pet.append([False])
            name_pet.append([None])
            coord_pet.append([ None, None ])
    df["has_pet"]=pd.Series(has_pet)
    df["name_pet"]=pd.Series(name_pet)
    df["coord_pet"]=pd.Series(coord_pet)
    return df



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

airport categoryId: "4bf58dd8d48988d1ed931735"
Pet Service   5032897c91d4c4b30a586d69
Child Care Service  5744ccdfe4b0c0459246b4c7
Daycare  4f4532974b9074f6e4fb0104
Basketball Court  4bf58dd8d48988d1e1941735
Nightlife Spot 4d4b7105d754a06376d81259
Vegetarian / Vegan Restaurant 4bf58dd8d48988d1d3941735
Basketball Stadium 4bf58dd8d48988d18b941735

time.sleep(1.25)



        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll='40.4439108,-3.6608311',
        #query='Airport',
        limit=1,
        categoryId="4bf58dd8d48988d1ed931735",
        radius=30_000 
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        data["response"]["groups"][0]["items"][0]["venue"]['categories'][0]["id"]
        
        data2["response"]["groups"][0]["items"][0]


"""
