## import packages 
import pandas as pd
import numpy as np
import geopy

## read data
df = pd.read_csv("airbnb_listings.csv")

## clean data

#print(df.count())
#print(df.columns.values.tolist())

## clean BUILDING TYPE data
valid_building_types = ['Entire rental unit', ## create list of place reasonably able to be leased out long term
                        'Entire loft',
                        'Entire townhouse',
                        'Farm stay',
                        'Entire home',
                        'Entire bungalow',
                        'Entire condo',
                        'Tiny home',
                        'Entire cottage',
                        'Entire villa',
                        'Entire serviced apartment',
                        'Entire cabin',
                        'Entire place',
                        'Earthen home',
                        'Entire chalet',
                        'Entire vacation home',
                        ]

df = df[df['property_type'].isin(valid_building_types)] # drop listings outside of our valid home types

###clean INACTIVE listings
df = df[df['number_of_reviews_l30d'] > 0] # anything reviewed in last 30 days consider active, drops ~10 000

###clean PRICE data
df['price'].replace(to_replace='[,$]',value='',regex=True,inplace=True) # remove $ and ,
df['price'] = pd.to_numeric(df['price']) # convert to numeric

#print(df.nlargest(10,columns='price'))
df = df[df['price'] < 9999] # anything more than this per night appears to be a typo, removes ~5 entries

def weekly_price(price):  ## apply formula for weekly price
    return price*7
df['price'] = df['price'].apply(weekly_price) # change night price to weekly price equiv for rent

### change lat/long data to postcode to compare against domain listings

def get_postcode(df, geolocator, lat_field, lon_field):
    location = geolocator.reverse((df[lat_field], df[lon_field]))
    try:
        location = location.raw['address']['postcode'] 
    except:
        location = ['Not Found'][0000]
    print(location)
    return location

geolocator = geopy.Nominatim(user_agent='KTunhla')

df['postcode'] = df.apply(get_postcode, axis=1, geolocator=geolocator, lat_field='latitude', lon_field='longitude')

## create final dataframe and write cleaned data
df = df[['price','bedrooms','postcode','latitude','longitude','host_listings_count']] 
df.to_csv('airbnb_listings_clean.csv', index=False, encoding='utf-8')










