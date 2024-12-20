import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
response = requests.get('https://bsky.app/profile/nytimes.com')
print(response)

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15'}

response = requests.get('https://bsky.app/profile/nytimes.com', headers=header)
print(response)


cookies = {
    'AWSALB': 'fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN',
    'AWSALBCORS': 'fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    # 'Cookie': 'AWSALB=fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN; AWSALBCORS=fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://bsky.social/',
    'Priority': 'u=0, i',
}

response = requests.get(
    'https://bsky.app/profile/nytimes.com', cookies=cookies, headers=headers)


soup = bs(response.text)
print(soup)


# Caminho para o ChromeDriver
# Substitua pelo caminho correto
chrome_driver_path = "/usr/local/bin/chromedriver"
service = Service(chrome_driver_path)

# Inicializar o WebDriver do Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Opcional: rodar sem interface gráfica
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)

# URL da página de perfil no Bluesky
url = "https://bsky.app/profile/nytimes.com"
driver.get(url)

# Esperar o carregamento inicial
time.sleep(5)

# Função para realizar scrolling na página e carregar mais postagens


def scroll_and_load(driver, scroll_times=10, delay=2):
    action = ActionChains(driver)
    for _ in range(scroll_times):
        driver.execute_script("window.scrollBy(0, 1000);")  # Scroll para baixo
        time.sleep(delay)


# Realizar scrolling para carregar mais postagens
scroll_and_load(driver, scroll_times=10, delay=2)

# Obter o HTML renderizado
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Lista para armazenar as postagens
posts_list = []

# Encontrar todas as postagens
# Classe geral das postagens
posts = soup.find_all("div", class_="css-175oi2r")

for post in posts:
    try:
        # Extrair o título
        title_element = post.find(
            "div", class_="css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-1udbk01")
        title = title_element.text.strip() if title_element else None

        # Extrair o número de likes
        likes_element = post.find("div", {"data-testid": "likeCount"})
        likes = int(likes_element.text.strip()) if likes_element else 0

        # Extrair a quantidade de comentários
        comment_count_element = post.find("div", {"data-testid": "replyBtn"})
        comment_count = int(comment_count_element.text.strip()
                            ) if comment_count_element else 0

        # Extrair os textos dos comentários
        comments = []
        comment_elements = post.find_all(
            "div", {"data-word-wrap": "1", "class": "css-146c3p1 r-1xnzce8"})
        for comment in comment_elements:
            comments.append(comment.text.strip())

        # Criar um dicionário para a postagem
        post_data = {
            "title": title,
            "likes": likes,
            "comment_count": comment_count,
            "comments": comments
        }

        # Adicionar à lista de postagens
        posts_list.append(post_data)

    except Exception as e:
        print(f"Erro ao processar uma postagem: {e}")

# Fechar o navegador
driver.quit()

# Exibir as postagens coletadas
for post in posts_list:
    print(post)

# Opcional: Salvar os dados em um arquivo CSV
df = pd.DataFrame(posts_list)
df.to_csv("bluesky_posts.csv", index=False, encoding="utf-8")
print("Dados salvos em 'bluesky_posts.csv'")
