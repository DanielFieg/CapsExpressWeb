import time
from duckduckgo_search import DDGS

proxy_url = "socks5://u66cd4bf7547005a8-zone-custom:u66cd4bf7547005a8@43.152.113.55:2333"
search_term = "Glico100"
max_retries = 5
results = []

# Intervalo fixo entre as tentativas
retry_interval = 15  # em segundos

for attempt in range(max_retries):
    ddgs = DDGS(proxy=proxy_url, timeout=20)
    try:
        # Realiza a busca
        search_results = ddgs.text(search_term, max_results=70)
        links = [result['href'] for result in search_results if 'href' in result]
        results.extend(links)
        print(f"Results from attempt {attempt + 1}: {links}")
        break  # Sai do loop se a busca for bem-sucedida
    except Exception as e:
        print(f"Attempt {attempt + 1} failed with error: {e}")
        # Estratégia de backoff em caso de erro de 'Ratelimit'
        if "Ratelimit" in str(e):
            wait_time = 2 ** attempt  # Backoff exponencial
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        else:
            # Espera um tempo fixo caso o erro não seja de 'Ratelimit'
            print(f"Waiting for {retry_interval} seconds before retrying...")
            time.sleep(retry_interval)

print("Final results:", results)
