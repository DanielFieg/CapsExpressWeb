import requests
from urllib.parse import urlparse
import json
import time

def buscar_titulos_e_links_no_google(query, start_index=1):
    API_KEY = 'AIzaSyBgk37iSeaHM3NiW8OQnVqoFiFbFu1v3XA'
    CSE_ID = '61600e36672c441f0'
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': API_KEY,
        'cx': CSE_ID,
        'start': start_index,
        'num': 10,  # Máximo que a API permite
        'gl': 'br'  # Pesquisa específica para o Brasil
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        resultados = response.json()
        
        resultados_extraidos = []
        for item in resultados.get('items', []):
            titulo = item.get('title')
            link = item.get('link')
            if titulo and link:
                resultados_extraidos.append({'title': titulo, 'link': link})
        
        next_page_info = resultados.get('queries', {}).get('nextPage', [])
        next_page_index = next_page_info[0].get('startIndex', None) if next_page_info else None
        
        return resultados_extraidos, next_page_index
    
    except requests.RequestException as e:
        print(f"Erro na solicitação: {e}")
        return [], None

def buscar_todos_titulos_e_links(termo):
    all_resultados = []
    start_index = 1
    max_results = 1000  # Ajuste conforme necessário
    total_found = 0  # Contador para o total encontrado

    print(f"Buscando com termo: {termo}...")
    
    while start_index and total_found < max_results:
        resultados, start_index = buscar_titulos_e_links_no_google(termo, start_index=start_index)
        if not resultados:
            break
        all_resultados.extend(resultados)
        total_found += len(resultados)
        
        # Adiciona um pequeno delay para evitar limites de taxa
        time.sleep(1)

    return all_resultados

# Termo de pesquisa
termo = 'Glico100'  # Você pode tentar também 'glico' ou variações

# Executar a busca
resultados_encontrados = buscar_todos_titulos_e_links(termo)

# Exibindo os resultados encontrados
for resultado in resultados_encontrados:
    print(f"Título: {resultado['title']}\nLink: {resultado['link']}\n")

# Salvar os resultados em um arquivo JSON para análise futura
with open('resultados_Glico100.json', 'w', encoding='utf-8') as f:
    json.dump(resultados_encontrados, f, ensure_ascii=False, indent=4)
