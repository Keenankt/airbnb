import pandas as pd
import numpy as np

postcodes = pd.read_csv('au_postcodes.csv')

vic_postcodes = postcodes[postcodes['postcode'].str.startswith('3')]
print(vic_postcodes)

