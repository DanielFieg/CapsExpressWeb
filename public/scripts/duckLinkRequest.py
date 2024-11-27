import requests
from bs4 import BeautifulSoup

def duckduckgo_search(query, page=1):
    # URL da busca com parâmetro de página
    url = f"https://html.duckduckgo.com/html/?q={query}&next={page}"

    # Cabeçalhos para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    try:
        # Fazendo a requisição
        response = requests.get(url, headers=headers, timeout=10)  # 10 segundos de timeout

        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrar todos os resultados da busca
            results = soup.find_all('a', class_='result__a')  # classe que contém os links dos resultados

            # Extrair e imprimir os links dos resultados
            for result in results:
                link = result.get('href')
                title = result.get_text()
                print(f'Título: {title}\nLink: {link}\n')
        else:
            print(f"Erro na requisição: {response.status_code}")

    except Exception as e:
        print(f"Erro ao buscar: {e}")

if __name__ == "__main__":
    query = input("Digite sua busca: ")
    
    # Busca na primeira página
    print("Resultados da página 1:")
    duckduckgo_search(query, page=1)
    
    # Busca na segunda página
    print("\nResultados da página 2:")
    duckduckgo_search(query, page=2)
