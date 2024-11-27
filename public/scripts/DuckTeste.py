import requests
import random
import time

url = "https://html.duckduckgo.com/html/?q=Glico100"
headers = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/85.0"
    ])
}

# Usando session para gerenciar cookies
with requests.Session() as session:
    response = session.get(url, headers=headers)

    # Verificando o conteúdo da resposta
    print(response.text)  # Ou response.json() se a resposta for em JSON

    # Atraso aleatório entre requisições
    time.sleep(random.uniform(5, 10))
