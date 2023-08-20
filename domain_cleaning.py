## import packages 
import pandas as pd
import numpy as np

## read data
df = pd.read_csv("domain_listings.csv")

# print(df.describe()) ## overview of dataset shape
## de duplicate using address
df = df.drop_duplicates(subset=['Address_line_1']) # removes ~30k results, scraper likely picks up surrounding postcodes each iteration

##########################################
## cleaning data
## cleaning BEDROOMS data

# print(df['Bedrooms'].unique()) # investigate shape of data
df['Bedrooms'] = df['Bedrooms'].str.replace('\D','', regex=True) # removes beds/bed and leaves only numbers
df['Bedrooms'] = pd.to_numeric(df['Bedrooms']) # checks all text removed and converts to numeric
df = df.dropna(subset='Bedrooms') # removes NA or not found info
df = df[df['Bedrooms'] != 0] # removes about 100 properties presumed to be car spaces

# print(df[df['Bedrooms'] > 6]) # investigate bedrooms of an unusual number
df = df.drop([11448,18300,18426,18684,23225,23304,23310,45373]) # bogus listings, either share house or mislabelled by agent

## cleaning BATHROOM data
df['Bathrooms'] = df['Bathrooms'].str.replace('\D','', regex=True) # removes bathrooms/bathroom and leaves only numbers
df['Bathrooms'] = pd.to_numeric(df['Bathrooms']) # convert to numeric
df = df.dropna(subset='Bathrooms') # removes NA or not found info

# print(pd.unique(df['Bathrooms'])) # investigate range of bathrooms
# print(df[df['Bathrooms'] > 4]) # investigate unusually high bathroom count
df = df.drop([4378,5167,23319,24962]) # mostly mis labelled, some share houses

## cleaning CAR_SPACES data

# print(df['Car_spaces'].unique()) ## investigate shape of data

df['Car_spaces'] = df['Car_spaces'].str.replace('[a-zA-Z]','', regex=True) # removes bathrooms/bathroom and leaves only numbers
df['Car_spaces'] = df['Car_spaces'].str.replace('−','0', regex=True) # changes - that resembles no parking to 0
df['Car_spaces'] = pd.to_numeric(df['Car_spaces']) # convert to numeric

# print(df[df['Car_spaces'] > 6]) # investigate unusual car spaces
df = df[df['Car_spaces'] <= 6] # either mislabelled, or agent has listed every square paved inch as a car space. Very few 
#### instances that represent useful information, worth dropping anything over this number

## cleaning BUILDING_TYPE data
# print(df['Building_type'].unique()) ## yields a lot of interesting categories

# print(df[df['Building_type'] == 'Retirement Living']) # often doesnt list price, and somewhat outside the scope of this analysis
# print(df[df['Building_type'] == 'Car space']) # somehow a car space listing that also has 1 bedroom
# print(df[df['Building_type'] == 'Development site']) # no home at all yet somehow has 1 bedroom
# print(df[df['Building_type'] == 'New house and land']) # see above
# print(df[df['Building_type'] == 'Vacant land']) # see above
df = df[
    (df['Building_type'] != 'Retirement Living') &
    (df['Building_type'] != 'Car space') &
    (df['Building_type'] != 'Development site') &
    (df['Building_type'] != 'New house and land') &
    (df['Building_type'] != 'Vacant land')
    ] ## All of these categories can be dropped as either outside of scope or dishonest REA listings

building_dict = {
    'Apartment / Unit / Flat' : 1,
    'Studio' : 1,
    'Penthouse' : 1,
    'New apartments / off the plan' : 1,
    'Block of units' : 1,
    'Townhouse' : 2,
    'Terrace' : 2,
    'Villa' : 2,
    'Semi-detached' : 2,
    'Duplex' : 2,
    'House' : 3,
    } # create dictionary to transform building types to meaningful groupings, 1 = high density apartments, 2 = lesser density semi detached,
#### 3 = free standing house

df['Building_type'].replace(to_replace=building_dict, inplace=True) # replace building types with numeric categories

## cleaning ADDRESS_LINE data
#### line 1 doesn't need to be cleaned as analysis will not be that granular, will just be used as a unique identifier
#### line 2's postcode will be used to analyse geographic distributions

# print(df['Address_line_2'].describe()) # investigate shape

df['Address_line_2'] = df['Address_line_2'].str.replace('\D','', regex=True) # remove suburb/state text
df['Address_line_2'] = pd.to_numeric(df['Address_line_2']) # convert to numeric potscode

# print(df[df['Address_line_2'] >= 4000]) # check postcodes out of range
# print(df[df['Address_line_2'] < 3000]) # check postcodes out of range

df['Address_line_2'].replace(to_replace={30043004 : 3004}, inplace=True) ## replace postcode typo

df = df.rename(columns={'Address_line_2':'Postcode'}) # rename column to postcode now that it represents just postcode


## cleaning address price data 
df['Price'].replace(to_replace='\S*?[pP][cC][mM]', value='', regex=True, inplace=True) # removing per cubic meter from listing
df['Price'].replace(to_replace='\S*?\s[pP][cC][mM]', value='', regex=True, inplace=True)
df['Price'].replace(to_replace='\S*?[pP]\.[cC]\.[mM]', value='', regex=True, inplace=True)
df['Price'].replace(to_replace='\S*?\s[pP]\.[cC]\.[mM]', value='', regex=True, inplace=True)
df['Price'].replace(to_replace='\S*?[pP]er\s[cC]ubic', value='', regex=True, inplace=True)
df['Price'].replace(to_replace='\S*?\s[pP]er\s[cC]ubic', value='', regex=True, inplace=True)


df['Price'].replace(to_replace="[a-zA-Z$|!//&()\-+:\*',]", value='', regex=True, inplace=True) # strip text and special characters not including . which can denote decimals
df['Price'] = df['Price'].str.replace(' ', '',) # remove blank space
df['Price'].replace(to_replace='\..*', value='', regex=True, inplace=True) # strip characters after . to get integer price
df['Price'] = df['Price'].str.replace(' ', '',) # remove blank space

df['Price'] = pd.to_numeric(df['Price']) # convert to numeric

df.dropna(subset='Price',axis=0, inplace=True) # drop listings with no price

df = df[df['Price'] <= 6000] # dropping listings over $6k/week. after investigation most are listings with negotiable prices,
### which truncated make absurdly high values. outside of scope of investigation, drops about ~200 listings

df = df[df['Price'] > 100] # dropping listings under $100/week after investigation almost all listings are car spaces, ~20 listings


########### Stripping address line 1 column as identifier no longer needed
df = df.drop(columns='Address_line_1',axis=1)

######## Write df to csv

df.to_csv('domain_listings_clean.csv', index=False, encoding='utf-8')





