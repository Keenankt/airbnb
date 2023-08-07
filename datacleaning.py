import pandas as pd
import numpy as np

df = pd.read_csv("listings.csv")

df = df.drop_duplicates(subset=['Address_line_1']) #dedupe

#print(deduped.describe())
numeric_index = df['Price'].str.isnumeric()
#df['Price'] = df['Price'].str.replace('\D','',regex=True)
df['Price'] = np.where(df['Price'].str.isnumeric(), df["Price"], df['Price'].str.replace('\D','',regex=True))

df['Price'] = pd.to_numeric(df['Price'])
print(df.describe())
print(df[df.Price > 5000])
#print(df['Price'])


