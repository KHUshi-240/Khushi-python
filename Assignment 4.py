import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://vegetablemarketprice.com/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'table table-striped'})

# Extract the table headers
headers = [th.text.strip() for th in table.find('tr').find_all('th')]

# Extract the data for California from 1 May 2024 to 30 June 2024
data = []
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    date = cols[0].text.strip()
    if '2024-05-' in date or '2024-06-' in date:
        state_name = cols[1].text.strip()
        if state_name == 'California':
            vegetable_name = cols[2].text.strip()
            wholesale_price = cols[3].text.strip()
            retail_price = cols[4].text.strip()
            shopping_mall_price = cols[5].text.strip()
            units = cols[6].text.strip()
            vegetable_image = cols[7].find('img')['src']
            data.append({
                'Date': date,
                'State Name': state_name,
                'Vegetable Name': vegetable_name,
                'Wholesale Price': wholesale_price,
                'Retail Price': retail_price,
                'Shopping Mall Price': shopping_mall_price,
                'Units': units,
                'Vegetable Image': vegetable_image
            })


df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('california_vegetable_data.csv', index=False)
