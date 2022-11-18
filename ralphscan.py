import requests
from bs4 import BeautifulSoup
import os
from shlex import quote

def proces(combined_string):
    with open('tmp/output.html', 'r') as file:
        data = file.read()
    
    soup = BeautifulSoup(data, 'html.parser')
    
    tiles = soup.find_all('div', class_='product-tile')
    
    my_string = ''
    for tile in tiles[:4]:
        try:
            price = tile.find('div', class_='product-pricing').find('span','lowcblack').get_text().replace(',00 DKK','')
        except:
            price = tile.find('input', class_='js-product-grid-prices').get_text().split('Price')[-1].replace('\n','').strip()
        name = tile.find('div', class_='product-name').find('a', 'name-link').get_text().replace('\n','')
        my_string += '\n{} {}'.format(price, name)
        print(price, name)
    return(my_string + '\n')

urls = {
    'Hoodie and sweatshirts':'https://www.ralphlauren.eu/dk/en/men/clothing/hoodies-sweatshirts/10204?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CHoodies%20%26%20Sweatshirts',
    'Jackets and coats': 'https://www.ralphlauren.eu/dk/en/men/clothing/jackets-coats/10205?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CJackets%20%26%20Coats',
    "T-shirts": 'https://www.ralphlauren.eu/dk/en/men/clothing/t-shirts/10203?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CT-Shirts',
    "Jumpers and cardigans": 'https://www.ralphlauren.eu/dk/en/men/clothing/jumpers-cardigans/10206?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CJumpers%20%26%20Cardigans',
    "Casual shirts": 'https://www.ralphlauren.eu/dk/en/men/clothing/casual-shirts/10202?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CCasual%20Shirts',
    "Polo shirts": 'https://www.ralphlauren.eu/dk/en/men/clothing/polo-shirts/10201?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CPolo%20Shirts',
    "Trousers": 'https://www.ralphlauren.eu/dk/en/men/clothing/trousers/102015?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CTrousers',
    "Jeans": 'https://www.ralphlauren.eu/dk/en/men/clothing/jeans/102010?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CJeans',
    "Blazers": 'https://www.ralphlauren.eu/dk/en/men/clothing/blazers/10209?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CBlazers',
    "Dress shirts": 'https://www.ralphlauren.eu/dk/en/men/clothing/formal-shirts/10207?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CFormal%20Shirts',
    "Suits": 'https://www.ralphlauren.eu/dk/en/men/clothing/suits/102019?srule=price-low-high&start=0&sz=32&webcat=Men%7CClothing%7CSuits',
    "Trainers": 'https://www.ralphlauren.eu/dk/en/men/shoes/trainers/10403?srule=price-low-high&start=0&sz=32&webcat=Men%7CShoes%7CTrainers',
    "Casual shoes": 'https://www.ralphlauren.eu/dk/en/men/shoes/casual-shoes/10402?webcat=men%7Cshoes%7Cmen-shoes-casual-shoes'
}

print('Starting script')

combined_string = ''
for url in urls:
    command = "curl '{}' \
      -H 'authority: www.ralphlauren.eu' \
      -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
      -H 'sec-ch-ua: \"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"' \
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' \
      --compressed --silent > tmp/output.html".format(urls[url])
    
    #run script
    os.system(command)
    
    string = '\n{}'.format(url)
    print(string)
    combined_string += string
    combined_string += proces(combined_string)


# Send notification
command = 'curl -d "{}" ntfy.sh/ralphscan'.format(combined_string)
command

os.system(command)

print('Script done')
