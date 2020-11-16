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
    # Creating empty lists to store required info
    has_airport=[]
    name_airport=[]
    coord_airpott=[]
    for i in range(len(df)):
        # Print status each 25 datapoints to check progress
        if i%25==0:
            print("Airport",i,len(df)-i)
        # Wait to not to get failures from server
        time.sleep(2)
        # Creating a dict with the query.
        # The categoryId is the one for the airports
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="4bf58dd8d48988d1ed931735",
        radius=30_000 
        )
        # Obtaining the query and saving it to the data variable
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        # If statement to prevent error if the server fails
        if len(data["response"])>0:
            # If statement to save info if there are results
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
    # Adding query results as columns of the DataFrame
    df["has_airport"]=pd.Series(has_airport)
    df["name_airport"]=pd.Series(name_airport)
    df["coord_airpott"]=pd.Series(coord_airpott)
    return df

def basket_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    # Creating empty lists to store required info
    has_basket=[]
    name_basket=[]
    coord_basket=[]
    for i in range(len(df)):
        if i%25==0:
            print("Basket",i,len(df)-i)
        # Wait to not to get failures from server
        time.sleep(2)
        # Creating a dict with the query.
        # The categoryId is the one for the basket stadiums
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="4bf58dd8d48988d18b941735",
        radius=10_000 
        )
        # Obtaining the query and saving it to the data variable
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        # If statement to prevent error if the server fails
        if len(data["response"])>0:
            # If statement to save info if there are results
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
    # Adding query results as columns of the DataFrame
    df["has_basket"]=pd.Series(has_basket)
    df["name_basket"]=pd.Series(name_basket)
    df["coord_basket"]=pd.Series(coord_basket)
    return df




def veg_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    # Creating empty lists to store required info
    has_veg=[]
    name_veg=[]
    coord_veg=[]
    num_veg=[]
    for i in range(len(df)):
        # Print status each 25 datapoints to check progress
        if i%25==0:
            print("Vegan",i,len(df)-i)
        # Wait to not to get failures from server
        time.sleep(2)
        # Creating a dict with the query.
        # The categoryId is the one for the vegan restaurants
        # and defined a 10 limit
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=10,
        categoryId="4bf58dd8d48988d1d3941735",
        radius=500 
        )
        # Obtaining the query and saving it to the data variable
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        # If statement to prevent error if the server fails
        if len(data["response"])>0:
            # If statement to save info if there are results
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
    # Adding query results as columns of the DataFrame
    df["has_veg"]=pd.Series(has_veg)
    df["name_veg"]=pd.Series(name_veg)
    df["coord_veg"]=pd.Series(coord_veg)
    df["num_veg"]=pd.Series(num_veg)
    return df

def night_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    # Creating empty lists to store required info
    has_night=[]
    name_night=[]
    coord_night=[]
    num_night=[]
    for i in range(len(df)):
        # Print status each 25 datapoints to check progress
        if i%25==0:
            print("Night",i,len(df)-i)
        # Wait to not to get failures from server
        time.sleep(2)
        # Creating a dict with the query.
        # The categoryId is the one for the nightlife spots
        # and define a 20 limit
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=20,
        categoryId="4d4b7105d754a06376d81259",
        radius=2000 
        )
        # Obtaining the query and saving it to the data variable
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        # If statement to prevent error if the server fails
        if len(data["response"])>0:
            # If statement to save info if there are results
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
    # Adding query results as columns of the DataFrame
    df["has_night"]=pd.Series(has_night)
    df["name_night"]=pd.Series(name_night)
    df["coord_night"]=pd.Series(coord_night)
    df["num_night"]=pd.Series(num_night)
    return df



def daycare_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    # Creating empty lists to store required info
    has_daycare=[]
    name_daycare=[]
    coord_daycare=[]
    for i in range(len(df)):
        # Print status each 25 datapoints to check progress
        if i%25==0:
            print("Daycare",i,len(df)-i)
        # Wait to not to get failures from server
        time.sleep(2)
        # Creating a dict with the query.
        # The categoryId is the one for the child daycare
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="4f4532974b9074f6e4fb0104",
        radius=1_000 
        )
        # Obtaining the query and saving it to the data variable
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        # If statement to prevent error if the server fails
        if len(data["response"])>0:
            # If statement to save info if there are results
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
    # Adding query results as columns of the DataFrame
    df["has_daycare"]=pd.Series(has_daycare)
    df["name_daycare"]=pd.Series(name_daycare)
    df["coord_daycare"]=pd.Series(coord_daycare)
    return df



def pet_info(df,id_4sq,tk_4sq):
    url = 'https://api.foursquare.com/v2/venues/explore'
    # Creating empty lists to store required info
    has_pet=[]
    name_pet=[]
    coord_pet=[]
    for i in range(len(df)):
        # Print status each 25 datapoints to check progress
        if i%25==0:
            print("Pet",i,len(df)-i)
        # Wait to not to get failures from server
        time.sleep(2)
        # Creating a dict with the query.
        # The categoryId is the one for the pet services
        params = dict(
        client_id=id_4sq,
        client_secret=tk_4sq,
        v='20201114',
        ll=str(df["latitude"][i])+","+str(df["longitude"][i]),
        limit=1,
        categoryId="5032897c91d4c4b30a586d69",
        radius=1_000 
        )
        # Obtaining the query and saving it to the data variable
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        # If loop to prevent error if the server fails
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
    # Adding query results as columns of the DataFrame
    df["has_pet"]=pd.Series(has_pet)
    df["name_pet"]=pd.Series(name_pet)
    df["coord_pet"]=pd.Series(coord_pet)
    return df

