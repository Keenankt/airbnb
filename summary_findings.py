## import packages
import pandas as pd
import numpy as np
import pydeck 

## read data
airbnb = pd.read_csv('airbnb_listings_clean.csv')
domain = pd.read_csv('domain_listings_clean.csv')
postcoords = pd.read_csv('australian_postcodes.csv')

## create summary dataframe for PowerBI
#### airbnb

airbnb = airbnb.groupby('postcode')['price'].aggregate(['mean','median','count'])
airbnb.rename(columns={'mean' : 'airbnb_mean_price', 'median' : 'airbnb_median_price', 'count' : 'airbnb_count'}, inplace=True)
airbnb.reset_index(inplace=True)


#### domain

domain = domain.groupby('postcode')['price'].aggregate(['mean','median','count'])
domain.rename(columns={'mean' : 'rental_mean_price', 'median' : 'rental_median_price', 'count' : 'rental_count'}, inplace=True)
domain.reset_index(inplace=True)

print(domain)

#### combined dataframe

combined_summary = domain.merge(airbnb, how='inner', on='postcode')
combined_summary['airbnb_rental_ratio'] = (combined_summary['airbnb_count'] / combined_summary['rental_count'])

# convert postcodes to shared lat/long for pydeck graphing  
postlong = postcoords.set_index('postcode')['long'].to_dict() 
postlat = postcoords.set_index('postcode')['lat'].to_dict()

combined_summary['long'] = combined_summary['postcode'].map(postlong)
combined_summary['lat'] = combined_summary['postcode'].map(postlat)

## write to csv
combined_summary.to_csv('combined_listings_summary.csv', index=False, encoding='utf-8')


## create summary dataframe

layer_rental = pydeck.Layer(
    'ColumnLayer',
    combined_summary,
    get_position=['long','lat'],
    get_elevation=['rental_count'],
    elevation_scale=10,
    get_fill_color=[55,126,184],
    offset=[0.75,-0.75],
    pickable=True,
    extruded=True,
    radius=250
)

layer_airbnb = pydeck.Layer(
    'ColumnLayer',
    combined_summary,
    get_position=['long','lat'],
    get_elevation=['airbnb_count'],
    elevation_scale=10,
    get_fill_color=[228,26,28],
    pickable=True,
    extruded=True,
    radius=250,
)

start_view = pydeck.data_utils.compute_view(combined_summary[['long','lat']])
start_view.pitch = 75
start_view.zoom = 10.5
start_view.bearing = 242.5

render = pydeck.Deck(layers=[layer_airbnb,layer_rental], map_style='dark', initial_view_state=start_view)
## render.to_html('airbnb.html')

