from selenium import webdriver
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np

#initialise webdriver
driver = webdriver.Chrome()

#initialise frames
prices = []
beds = []
baths = []
cars = []
types = []
addresses1 = []
addresses2 = []

#read postcode list
postcodes = pd.read_csv('vic_postcodes.csv')
postcodes = postcodes['postcode']

for postcode in postcodes:
    driver.get('https://www.domain.com.au/rent/?postcode=' + str(postcode) + '&excludedeposittaken=1&page=1')
    webpage = driver.page_source
    parsed_webpage = soup(webpage,features='html.parser')    
    total_listings = parsed_webpage.find('h1', attrs={'class': 'css-ekkwk0'}).get_text() 
    total_listings = total_listings.split()
    total_listings = int(total_listings[0])
    pages_to_search = int(round(total_listings / 20))

    for page in range(1,pages_to_search+1):
        driver.get('https://www.domain.com.au/rent/?postcode=' + str(postcode) + '&excludedeposittaken=1&page=' + str(page))

        webpage = driver.page_source

        parsed_webpage = soup(webpage,features='html.parser')

        for element in parsed_webpage.findAll('li', attrs={'class': 'css-1qp9106'}):
            price = element.find('p', attrs={'data-testid': 'listing-card-price'})
            prices.append(price.get_text())

            features = element.findAll('span', attrs={'data-testid': 'property-features-text-container'}, limit=3) #not great but good enough
            if len(features) == 3:     
                bed, bath, car = features
                beds.append(bed.get_text())
                baths.append(bath.get_text())
                cars.append(car.get_text())
            else:
                beds.append("Unknown")
                baths.append("Unknown")
                cars.append("Unknown") 

            type = element.find('div', attrs={'class': 'css-11n8uyu'})
            if type != None:
                types.append(type.get_text())
            else:
                types.append('Unknown')

            address1 = element.find('span', attrs={'data-testid': 'address-line1'})
            if address1 != None:
                addresses1.append(address1.get_text())
            else:
                addresses1.append('Unknown')

            address2 = element.find('span', attrs={'data-testid': 'address-line2'})
            if address2 != None:
                addresses2.append(address2.get_text())
            else:
                addresses2.append('Unknown')


print(prices)
print(beds)
print(baths)
print(cars)
print(types)
print(addresses1)
print(addresses2)

df = pd.DataFrame(
    {'Price': prices, 
     'Bedrooms': beds, 
     'Bathrooms': baths, 
     'Car_spaces': cars, 
     'Building_type': types, 
     'Address_line_1': addresses1,
     'Address_line_2': addresses2})

df.to_csv('listings.csv', index=False, encoding='utf-8')