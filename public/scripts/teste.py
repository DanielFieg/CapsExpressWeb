import os
import re
import json
import sys
import pandas as pd
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

class Scrappy:
    def __init__(self, opcao_selecionada):
        self.opcao_selecionada = opcao_selecionada
        self.driver = None

    def iniciar(self):
        self.termo_pesquisa = self.opcao_selecionada
        self.pesquisa_google()

    def pesquisa_google(self):
        
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')

        # Definindo o User-Agent para um navegador real
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")

        try:
            self.driver = uc.Chrome(options=options)
            self.driver.get('https://www.google.com.br/?h1=pt-BR')

            search_box = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "q")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
            search_box.clear()
            search_box.send_keys(self.termo_pesquisa)
            self.simulate_typing(search_box)
            search_box.send_keys(Keys.RETURN)

            time.sleep(random.uniform(2, 4))
            self.scroll_to_bottom()

            df = self.organizar_dados()
            json_data = self.exportar_json(df)
            print(json_data)

        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro na pesquisa do Google: {str(e)}"}, ensure_ascii=False) + "\n")
        finally:
            if self.driver:
                self.driver.quit()

    def simulate_typing(self, element):
        """Simula a digitação no campo de pesquisa."""
        for char in self.termo_pesquisa:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))  # Tempo aleatório entre 50 a 150 ms

    def scroll_to_bottom(self):
        """Rola a página para baixo e simula um comportamento mais humano."""
        while True:
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))  # Tempo aleatório entre 2 a 4 segundos
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                time.sleep(random.uniform(2, 4))  # Tempo aleatório entre 2 a 4 segundos
                element = self.driver.find_elements(By.XPATH, '//*[text()="Mais resultados"]')
                if self.driver.find_elements(By.XPATH, '//*[@id="ofr"]'):
                    return
                elif element:
                    self.driver.execute_script("arguments[0].click();", element[0])
                    time.sleep(random.uniform(2, 4))  # Tempo aleatório entre 2 a 4 segundos
                else:
                    next_page = self.driver.find_elements(By.XPATH, '//a[@id="pnnext"]')
                    if next_page:
                        self.driver.execute_script("arguments[0].click();", next_page[0])
                        time.sleep(random.uniform(2, 4))  # Tempo aleatório entre 2 a 4 segundos
                    else:
                        break
            except Exception as e:
                sys.stderr.write(json.dumps({"message": f"Erro ao rolar a página: {str(e)}"}, ensure_ascii=False) + "\n")
                break

    def organizar_dados(self):
        """Organiza os dados coletados e remove links indesejados."""
        try:
            links_encontrados = []

            while True:
                search_results = self.driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')
                for result in search_results:
                    try:
                        link_element = result.find_element(By.XPATH, './/a')
                        link = link_element.get_attribute('href')
                        domain_match = re.search(r'^(?:https?:\/\/)?(?:[^:\/\n]+)', link)
                        if domain_match:
                            domain = domain_match.group(0)
                        else:
                            continue
                        domain_limpo = re.sub(r'\W+', '', domain)
                        opcao_presente = any(part.lower() in domain_limpo.lower() for part in self.opcao_selecionada.split())
                        if not opcao_presente:
                            continue
                        if self.is_marketplace_or_social(link):
                            continue
                        links_encontrados.append(link)
                    except Exception as e:
                        sys.stderr.write(json.dumps({"message": f"Erro ao coletar link: {str(e)}"}, ensure_ascii=False) + "\n")
                        continue

                next_button = self.driver.find_elements(By.XPATH, '//*[@id="pnnext"]')
                if next_button:
                    next_button[0].click()
                    time.sleep(random.uniform(2, 4))  # Tempo aleatório entre 2 a 4 segundos
                else:
                    break

            df = pd.DataFrame({'link': links_encontrados})
            return df

        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro ao organizar dados: {str(e)}"}, ensure_ascii=False) + "\n")
            return pd.DataFrame()

    def is_marketplace_or_social(self, link):
        """Verifica se o link é de um marketplace ou rede social."""
        marketplaces = ['amazon.', 'mercadolivre.', 'ebay.', 'aliexpress.', 'buscape.', 'shoptime.', 'casasbahia.', 'magazineluiza.', 'submarino.',
                        'americanas.', 'shopee.', 'zoom.', 'extra.', 'aliexpress.', 'pontofrio.', 'cliquefarma.', 'mercado', 'drogaraia.', 'loja', 'enjoei.',
                        'farmacia', 'hotmart.', 'reclameaqui.', 'siteconfiavel.', 'siteconfiavel.']
        social_networks = ['facebook.', 'twitter.', 'instagram.', 'linkedin.', 'tiktok.', 'youtube.', 'kwai.', 'pinterest.', 'globo.', 'noticia']
        for site in marketplaces + social_networks:
            if site in link or link.startswith(site):
                return True
        return False

    def exportar_json(self, df):
        """Exporta os dados organizados para JSON."""
        try:
            if isinstance(df, pd.DataFrame):
                json_data = df.to_json(orient='records', force_ascii=False)
            else:
                json_data = json.dumps(df, ensure_ascii=False)
            return json_data
        except Exception as e:
            return json.dumps({"message": f"Erro ao exportar dados para JSON: {str(e)}"}, ensure_ascii=False)

if __name__ == "__main__":
    marca = sys.argv[1] if len(sys.argv) > 1 else ""
    if marca:
        scrappy = Scrappy(marca)
        scrappy.iniciar()
    else:
        sys.stderr.write(json.dumps({"message": "Nenhum termo de pesquisa fornecido"}, ensure_ascii=False) + "\n")
