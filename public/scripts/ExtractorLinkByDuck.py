#!/usr/bin/env python3

import pandas as pd
import sys
from duckduckgo_search import DDGS
import json
import re
from difflib import SequenceMatcher
import time
import requests  # Importando a biblioteca requests

class Scrappy:
    def __init__(self, search_query, proxy=None):
        self.search_query = search_query
        self.ddgs = DDGS()  # Removido o proxy da inicialização do DDGS
        self.results = []  # Armazena os resultados
        self.proxy = proxy  # Armazena o proxy para requisições HTTP externas

    def is_marketplace_or_social(self, link):
        marketplaces = ['amazon.', 'mercadolivre.', 'ebay.', 'aliexpress.', 'buscape.', 'shoptime.', 'casasbahia.', 
                        'magazineluiza.', 'submarino.', 'americanas.', 'shopee.', 'zoom.', 'extra.', 'pontofrio.', 
                        'cliquefarma.', 'drogaraia.', 'loja.', 'enjoei.', 'farmacia.', 'hotmart.', 'reclameaqui.', 
                        'siteconfiavel.']
        social_networks = ['facebook.', 'twitter.', 'instagram.', 'linkedin.', 'tiktok.', 'youtube.', 'kwai.', 
                           'pinterest.', 'globo.', 'noticia.', 'uol.', 'conpass.', 'wikipedia.', 'cnn.']
        for site in marketplaces + social_networks:
            if site in link:
                return True
        return False

    def similar(self, a, b):
        """ Retorna a similaridade entre duas strings usando a razão de similaridade de sequência """
        return SequenceMatcher(None, a, b).ratio()

    def organizar_dados(self, links):
        organized_links = []
        for link in links:
            domain_match = re.search(r'^(?:https?:\/\/)?(?:[^:\/\n]+)', link)
            if domain_match:
                domain = domain_match.group(0)
                domain_limpo = re.sub(r'\W+', '', domain)
                similarity = self.similar(self.search_query.lower(), domain_limpo.lower())
                
                # Verifica se o domínio contém parte significativa do nome da marca ou é semelhante
                if (any(part.lower() in domain_limpo.lower() for part in self.search_query.split()) or
                    similarity > 0.5 or  # Ajuste a similaridade para capturar variações próximas
                    self.search_query.lower() in domain_limpo.lower()):  # Verifica se a consulta é parte do domínio
                    organized_links.append(link)
        return organized_links

    def fetch_results(self, max_retries=5, retry_interval=20):
        """Busca os resultados usando DuckDuckGo em uma única solicitação com tratamento de rate limit."""
        retries = 0
        while retries < max_retries:
            try:
                ddgs = DDGS(proxy=self.proxy, timeout=20)
                result = ddgs.text(
                    keywords=self.search_query,
                    region='br-pt',
                    safesearch='off',
                    timelimit='7d',
                    max_results=100
                )
                self.results.extend(result)  # Adiciona os resultados à lista
                return  # Sucesso, sai do loop
            except Exception as e:
                # Estratégia de backoff em caso de erro de 'Ratelimit'
                if "rate limit" in str(e).lower():
                    retries += 1
                    wait_time = 2 ** retries  # Backoff exponencial
                    time.sleep(wait_time)
                else:
                    # Espera um tempo fixo caso o erro não seja de 'Ratelimit'
                    time.sleep(retry_interval)


    def get_filtered_links_as_dataframe(self):
        """Filtra os resultados para remover links de marketplaces e redes sociais."""
        if not self.results:
            return pd.DataFrame(columns=['link'])  # Retorna um DataFrame vazio com a coluna 'link'
        
        filtered_links = [link for link in [result['href'] for result in self.results] if not self.is_marketplace_or_social(link)]
        organized_links = self.organizar_dados(filtered_links)

        # Cria um DataFrame com os links organizados
        organized_df = pd.DataFrame({'link': organized_links})
        return organized_df

    def exportar_json(self, df):
        """Exporta o DataFrame de links para JSON.""" 
        try:
            if isinstance(df, pd.DataFrame):
                json_data = df.to_json(orient='records', force_ascii=False, indent=4)
            else:
                json_data = json.dumps(df, ensure_ascii=False, indent=4)
            return json_data
        except Exception as e:
            return json.dumps({"message": f"Erro ao exportar dados para JSON: {str(e)}"}, ensure_ascii=False)

    # def mostrar_ip(self):
    #     """Mostra o IP público que está sendo usado para verificar a rotação de IP.""" 
    #     try:
    #         response = requests.get("http://api.ipify.org?format=json", proxies={"http": self.proxy, "https": self.proxy})
    #         ip_info = response.json()
    #         print(f"IP em uso: {ip_info['ip']}")
    #     except Exception as e:
    #         print(f"Erro ao obter IP: {e}")

if __name__ == "__main__":
    marca = sys.argv[1] if len(sys.argv) > 1 else ""

    # Configuração do proxy
    # proxy_url = "socks5://u66cd4bf7547005a8-zone-custom:u66cd4bf7547005a8@43.152.113.55:2333"

    if marca:
        scrappy = Scrappy(marca)  # Passa o proxy para a classe Scrappy
        # scrappy.mostrar_ip()  # Mostra o IP antes de buscar os resultados
        scrappy.fetch_results()  # Chama o método para buscar resultados
        organized_df = scrappy.get_filtered_links_as_dataframe()
        json_data = scrappy.exportar_json(organized_df)
        print(json_data)
    else:
        sys.stderr.write(json.dumps({"message": "Nenhum termo de pesquisa fornecido"}, ensure_ascii=False) + "\n")
