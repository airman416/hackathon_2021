from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.trendhunter.com/slideshow/2021-eco-innovations")
soup = BeautifulSoup(page.content, 'html.parser')

def retrieve_product_name():
    name =  [i.text for i in soup.find_all('div', class_='thar__title1', text=True)]
    print(name)
    image = [i.attrs['src'] for i in soup.find_all('img', class_='thar__img') if i.attrs['src'] != 
             'https://cdn.trendhunterstatic.com/icons/tha/lazyplaceholder.jpeg']

    product_data = []
    
    for i, j in zip(name, image):
        product_data.append({'name': i,
                             'image': j})
        
    return product_data

retrieve_product_name()