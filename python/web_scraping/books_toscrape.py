import requests
from bs4 import BeautifulSoup
import pandas as pd

title_list = []
price_list = []

for num in range(1,51):
    url_book = f'https://books.toscrape.com/catalogue/page-{num}.html'
    
    r = requests.get(url_book, timeout=10)
    r.raise_for_status()
    html_markup = r.text

    soup = BeautifulSoup(html_markup, 'html.parser')

    # Get titles
    for element in soup.find_all('a'):
        title = element.get('title')
        if title is not None:
            title_list.append(title)

    # Get prices
    for prices in soup.find_all('p', class_='price_color'):
        price = prices.get_text()
        price = price.replace('Â£', '')
        price_list.append(float(price))

# Dataframe
df = pd.DataFrame({
    'title': title_list,
    'price (in £)': price_list
})

print(len(df))
print(df.head())
print(df.tail())


# Further learning:
# https://chatgpt.com/share/6ade05f3-afd4-83ee-a4fa-717af7fdbdf3
