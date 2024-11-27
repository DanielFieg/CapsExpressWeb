import os
import re
import json
import sys
import pandas as pd
from time import sleep
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
        self.pesquisa_bing()

    def pesquisa_bing(self):
        options = uc.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')

        try:
            self.driver = uc.Chrome(options=options)
            self.driver.get('https://www.bing.com/?cc=br')

            # Fechar a janela de cookies, se aparecer
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "bnp_btn_accept"))
                )
                accept_button = self.driver.find_element(By.ID, "bnp_btn_accept")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", accept_button)
                sleep(1)
                accept_button.click()
                sleep(2)
                if not self.is_element_clickable(accept_button):
                    self.driver.execute_script("arguments[0].click();", accept_button)
                    sleep(2)
            except Exception as e:
                sys.stderr.write(json.dumps({"message": f"Janela de cookies não encontrada ou não foi possível fechar: {str(e)}"}, ensure_ascii=False) + "\n")

            # Realiza a pesquisa
            search_box = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "q")))
            search_box.clear()
            search_box.send_keys(self.termo_pesquisa)
            search_box.send_keys(Keys.RETURN)

            sleep(5)
            self.scroll_to_bottom(max_pages=10)  # Passa o número máximo de páginas

            df = self.organizar_dados(max_pages=10)  # Passa o número máximo de páginas para organizar_dados
            json_data = self.exportar_json(df)
            print(json_data)

        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro na pesquisa do Bing: {str(e)}"}, ensure_ascii=False) + "\n")

    def is_element_clickable(self, element):
        try:
            return element.is_displayed() and element.is_enabled()
        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro ao verificar se o elemento é clicável: {str(e)}"}, ensure_ascii=False) + "\n")
            return False

    def scroll_to_bottom(self, max_pages=10):
        page_count = 0
        while page_count < max_pages:
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                sleep(2)

                # Tenta encontrar o botão "Próxima página"
                next_page = self.driver.find_elements(By.XPATH, '//a[@aria-label="Próxima página"]')
                if next_page:
                    self.driver.execute_script("arguments[0].click();", next_page[0])
                    sleep(3)
                    page_count += 1
                else:
                    break
            except Exception as e:
                sys.stderr.write(json.dumps({"message": f"Erro ao rolar a página: {str(e)}"}, ensure_ascii=False) + "\n")
                break

    def organizar_dados(self, max_pages=10):
        try:
            links_encontrados = []
            page_count = 0
            while page_count < max_pages:
                search_results = self.driver.find_elements(By.XPATH, '//li[@class="b_algo"]')
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

                # Verifica se há um botão para a próxima página e clica nele
                next_button = self.driver.find_elements(By.XPATH, '//a[@aria-label="Próxima página"]')
                if next_button:
                    self.driver.execute_script("arguments[0].click();", next_button[0])
                    sleep(3)
                    page_count += 1
                else:
                    break

            df = pd.DataFrame({'link': links_encontrados})
            return df

        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro ao organizar dados: {str(e)}"}, ensure_ascii=False) + "\n")
            return pd.DataFrame()

    def is_marketplace_or_social(self, link):
        marketplaces = ['amazon.', 'mercadolivre.', 'ebay.', 'aliexpress.', 'buscape.', 'shoptime.', 'casasbahia.', 'magazineluiza.', 'submarino.',
                        'americanas.', 'shopee.', 'zoom.', 'extra.', 'aliexpress.', 'pontofrio.', 'cliquefarma.', 'mercado', 'drogaraia.', 'loja', 'enjoei.',
                        'farmacia', 'hotmart.', 'reclameaqui.', 'siteconfiavel.', 'siteconfiavel.']
        social_networks = ['facebook.', 'twitter.', 'instagram.', 'linkedin.', 'tiktok.', 'youtube.', 'kwai.', 'pinterest.', 'globo.', 'noticia']
        for site in marketplaces + social_networks:
            if site in link or link.startswith(site):
                return True
        return False

    def exportar_json(self, df):
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
