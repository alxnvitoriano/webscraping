import requests as req
from bs4 import BeautifulSoup
import re 
import pandas as pd

url= 'https://www.mercadolivre.com.br/ofertas#nav-header'
site=req.get(url)
soup = BeautifulSoup(site.content, 'html.parser')

qtd_products = soup.find_all('div', class_='promotion-item')
qtd = len(qtd_products)

# Dicionário para guardar as informações do scraping
dic_products = {'preco': [], 'link': [], 'desconto': [], 'title': []}

for i in range(1, 20):
    url_pag = f'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&page={i}'  # Navegar página por página
    site = req.get(url_pag)
    soup = BeautifulSoup(site.content, 'html.parser')
    products = soup.find_all('div', class_=re.compile('promotion-item'))

    for product in products:
        discount_tag = product.find('span', class_='promotion-item__discount-text')
        if discount_tag:
            try:
                discount = int(discount_tag.text.strip('%'))  # Converter o texto em um número sem caracteres, em um tipo de dados inteiro
                if discount > 15:
                    title_tag = product.find('p', class_=re.compile('promotion-item__title'))
                    preco_tag = product.find('span', class_=re.compile('promotion-item__price'))
                    link_tag = product.find('a', class_='promotion-item__link-container')

                    if title_tag and preco_tag and link_tag:
                        # Adicione os produtos ao dicionário apenas se o desconto for maior que 15%
                        dic_products['title'].append(title_tag.get_text().strip())
                        dic_products['preco'].append(preco_tag.get_text().strip())
                        dic_products['link'].append(link_tag['href'])
                        dic_products['desconto'].append(discount)

            except ValueError as e:
                print(f"{e}")

df = pd.DataFrame(dic_products)
print(df)