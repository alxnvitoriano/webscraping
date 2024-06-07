import requests as req
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.mercadolivre.com.br/ofertas#nav-header'
site = req.get(url)
soup = BeautifulSoup(site.content, 'html.parser')

qtd_products = soup.find_all('div', class_='promotion-item')
qtd = len(qtd_products)

dic_products = {'preco': [], 'link': [], 'desconto': [], 'title': []}

for i in range(1, 20):
    url_pag = f'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&page={i}'
    site = req.get(url_pag)
    soup = BeautifulSoup(site.content, 'html.parser')
    products = soup.find_all('div', class_='promotion-item')

    for product in products:
        discount_tag = product.find('span', class_='promotion-item__discount-text')
        if discount_tag:
            try:
                discount = int(discount_tag.text.strip('%'))
                if discount > 15:
                    title_tag = product.find('p', class_='promotion-item__title')
                    preco_tag = product.find('span', class_='promotion-item__price')
                    link_tag = product.find('a', class_='promotion-item__link-container')

                    if title_tag and preco_tag and link_tag:
                        dic_products['title'].append(title_tag.get_text().strip())
                        dic_products['preco'].append(preco_tag.get_text().strip())
                        dic_products['link'].append(link_tag['href'])
                        dic_products['discount'].append(discount)
            except ValueError as e:
                print(f"Error parsing discount: {e}")

df = pd.DataFrame(dic_products)
print(df)