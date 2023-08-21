## import packages 
import pandas as pd
import numpy as np
import geopy

df = pd.read_csv('airbnb_listings_clean.csv')
df['postcode'].replace(to_replace='Not Found', value=0000,inplace=True)
df.to_csv('airbnb_listings_clean.csv', index=False, encoding='utf-8')