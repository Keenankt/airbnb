import pandas as pd
import numpy as np

postcodes = pd.read_csv('au_postcodes.csv')


#vic_postcodes = postcodes[postcodes['postcode'].astype(str).str.startswith('3')]
#vic_postcodes = postcodes[postcodes['state_code']=="VIC"]

vic_postcodes = postcodes[(postcodes['state_code']=="VIC") & postcodes['postcode'].astype(str).str.startswith('3')]

pd.DataFrame.to_csv(vic_postcodes,"vic_postcodes.csv")

print(vic_postcodes)

