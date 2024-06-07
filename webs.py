import requests
from bs4 import BeautifulSoup

# URL of the Mercado Livre offers page
url = "https://www.mercadolivre.com.br/ofertas"

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all products in the offer selection
    products = soup.find_all('div', {'class': 'promotion-item'})

    # Create a list to store products with more than 15% discount
    discounted_products = []

    # Iterate over the products
    for product in products:
        # Extract the title of the product
        title = product.find('h2', {'class': 'promotion-item__title'}).text.strip()

        # Extract the original price of the product
        original_price = product.find('span', {'class': 'promotion-item__original-price'}).text.strip()

        # Extract the current price of the product
        current_price = product.find('span', {'class': 'promotion-item__price'}).text.strip()

        # Calculate the discount
        discount = (float(original_price.replace('R$', '').replace('.', '')) - float(current_price.replace('R$', '').replace('.', ''))) / float(original_price.replace('R$', '').replace('.', '')) * 100

        # Check if the discount is greater than or equal to 15%
        if discount >= 15:
            # Extract the link of the product
            link = product.find('a', {'class': 'promotion-item__link'})['href']

            # Add the product to the list of discounted products
            discounted_products.append({
                'title': title,
                'original_price': original_price,
                'current_price': current_price,
                'discount': f"{discount:.2f}%",
                'link': link
            })

    # Display information about products with more than 15% discount
    for product in discounted_products:
        print(f"Título: {product['title']}")
        print(f"Preço original: {product['original_price']}")
        print(f"Preço atual: {product['current_price']}")
        print(f"Desconto: {product['discount']}")
        print(f"Link: {product['link']}")
        print("---")
else:
    print("Erro ao acessar a página")