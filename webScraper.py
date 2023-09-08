# import re
# import sys
# import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

# Find the criterion movie URL's
url = 'https://orangecounty.craigslist.org/search/santa-ana-ca/apa?housing_type=1&housing_type=6&housing_type=7&housing_type=9&lat=33.7707&lon=-117.8859&max_bedrooms=2&max_price=2200&min_bedrooms=1&min_price=1500&search_distance=5.5#search=1~list~0~0'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print(soup)

divs = soup.find_all("a", attrs={"class": "posting-title"})

urls = [div['href'] for div in divs ]

# urls = [div.a['href'] for div in divs ] # array of URL's for rental pages

rental_data = []
count = 0

for page in urls:
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        address = soup.find("h2", attrs={'class':'street-address'})
        price = soup.find("span", attrs={"class":"price"})
        housing = soup.find("span", attrs={"class":"housing"})
        title = soup.find("span", attrs={"id":"titletextonly"})
        data = {
            "title": title,
            "address": address,
            "price": price,
            "housing": housing,
            "link": page
        }
        rental_data.append(data)
        count += 1
        print(count)
    except:
        print('Title not found')

#len is 2703

with open('rentaldata.json', 'w') as fp:
    json.dump(rental_data, fp)
