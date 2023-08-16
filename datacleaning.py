## import packages 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## read data
df = pd.read_csv("listings.csv")

print(df.describe())
## de duplicate using address
df = df.drop_duplicates(subset=['Address_line_1']) # removes ~30k results, scraper likely picks up surrounding postcodes each iteration

# print(df.iloc[108]) ## trouble shooting

## cleaning data
## cleaning bedroom data
df['Bedrooms'] = df['Bedrooms'].str.replace('\D','', regex=True) # removes beds/bed and leaves only numbers
df['Bedrooms'] = pd.to_numeric(df['Bedrooms']) # checks all text removed and converts to numeric
df = df.dropna(subset='Bedrooms') # removes NA or not found info
df = df[df['Bedrooms'] != 0] # removes about 100 properties presumed to be car spaces

# print(pd.unique(df['Bedrooms'])) # investigate range of bedrooms
# print(df[df['Bedrooms'] > 6]) # investigate bedrooms of an unusual number
df = df.drop([11448,18300,18426,18684,23225,23304,23310,45373]) # bogus listings, either share house or mislabelled by agent

## cleaning bathroom data
df['Bathrooms'] = df['Bathrooms'].str.replace('\D','', regex=True) # removes beds/bed and leaves only numbers
df['Bathrooms'] = pd.to_numeric(df['Bathrooms']) # checks all text removed and converts to numeric
df = df.dropna(subset='Bathrooms') # removes NA or not found info

print(pd.unique(df['Bathrooms'])) # investigate range of bathrooms
print(df[df['Bathrooms'] > 4]) # investigate unusually high bathroom count
df = df.drop([4378,5167,23319,24962]) # mostly mis labelled, some share houses

## cleaning address price data 

#df['Price'] = np.where(df['Price'].str.isnumeric(), df["Price"], df['Price'].str.replace('[a-zA-Z$,]','',regex=True))
#df['Price'] = np.where(df['Price'].str.isnumeric(), df["Price"], df['Price'].str.replace('$','',regex=True))
#df['Price'] = df['Price'].str.strip()
#df['Price'] = np.where(df['Price'].str.isnumeric(), df["Price"], df['Price'].str.replace('^.','',regex=True))

#df['Price'] = pd.to_numeric(df['Price'])
#print(df.describe())
#print(df[df.Price > 5000])




