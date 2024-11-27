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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

class ChromeProxy:
    def __init__(self, host: str, port: int, username: str = "", password: str = ""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "proxy_extension")

    def create_extension(self, name: str = "Chrome Proxy", version: str = "1.0.0") -> str:
        proxy_folder = self.get_path()
        os.makedirs(proxy_folder, exist_ok=True)

        # Generate manifesto (set extension name and version)
        manifest = ChromeProxy.manifest_json
        manifest = manifest.replace("<ext_name>", name)
        manifest = manifest.replace("<ext_ver>", version)

        # Write manifest to extension directory
        with open(f"{proxy_folder}/manifest.json", "w") as f:
            f.write(manifest)

        # Generate JavaScript code (replace placeholders)
        js = ChromeProxy.background_js
        js = js.replace("<proxy_host>", self.host)
        js = js.replace("<proxy_port>", str(self.port))
        js = js.replace("<proxy_username>", self.username)
        js = js.replace("<proxy_password>", self.password)

        # Write JavaScript code to extension directory
        with open(f"{proxy_folder}/background.js", "w") as f:
            f.write(js)

        return proxy_folder

    manifest_json = """
    {
        "version": "<ext_ver>",
        "manifest_version": 3,
        "name": "<ext_name>",
        "permissions": [
            "proxy",
            "tabs",
            "storage",
            "webRequest",
            "webRequestAuthProvider"
        ],
        "host_permissions": [
            "<all_urls>"
        ],
        "background": {
            "service_worker": "background.js"
        },
        "minimum_chrome_version": "22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "<proxy_host>",
                port: parseInt("<proxy_port>")
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({
        value: config,
        scope: "regular"
    }, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "<proxy_username>",
                password: "<proxy_password>"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn, {
            urls: ["<all_urls>"]
        },
        ['blocking']
    );
    """

class Scrappy:
    def __init__(self, opcao_selecionada):
        self.opcao_selecionada = opcao_selecionada
        self.driver = None

    def iniciar(self):
        self.termo_pesquisa = self.opcao_selecionada
        self.pesquisa_duckduckgo()
        df = self.organizar_dados()
        json_data = self.exportar_json(df)
        print(json_data)
        if self.driver:
            self.driver.quit()

    def pesquisa_duckduckgo(self):
        # Configurando a extensão do proxy
        proxy = ChromeProxy(
            host="43.159.28.126",
            port=2334,
            username="u66cd4bf7547005a8-zone-custom-region-br-asn-AS52748",
            password="u66cd4bf7547005a8"
        )

        extension_path = proxy.create_extension()
        options = uc.ChromeOptions()
        options.add_argument(f"--load-extension={extension_path}")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = "/usr/bin/google-chrome"  # Substitua pelo caminho real, se necessário

        try:
            self.driver = uc.Chrome(options=options)
            self.driver.get('https://html.duckduckgo.com/html')
            
            search_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "searchbox_input"))
            )
            
            # Tirar uma captura de tela da página carregada
            screenshot_path = '/var/www/html/SistemaWebCaps/CapsExpressWeb/public/scripts/google_screenshot.png'
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot salvo em: {screenshot_path}")
            
            search_box.clear()
            search_box.send_keys(self.termo_pesquisa)
            sleep(2)
            search_box.send_keys(Keys.RETURN)
            
            sleep(10)
            # Tirar uma captura de tela da página carregada
            screenshot_path1 = '/var/www/html/SistemaWebCaps/CapsExpressWeb/public/scripts/google_screenshot1.png'
            self.driver.save_screenshot(screenshot_path1)
            print(f"Screenshot salvo em: {screenshot_path1}")

            sleep(3)
            self.scroll_to_bottom()
        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro na pesquisa do DuckDuckGo: {str(e)}"}, ensure_ascii=False) + "\n")

    def scroll_to_bottom(self):
        try:
            while True:
                sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                mais_resultados = self.driver.find_elements(By.ID, "more-results")

                if not mais_resultados or "disabled" in mais_resultados[0].get_attribute("class"):
                    break
                mais_resultados[0].click()
                sleep(2)
        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro ao clicar em 'Mais resultados': {str(e)}"}, ensure_ascii=False) + "\n")

    def organizar_dados(self):
        try:
            links_encontrados = []
            search_results = self.driver.find_elements(By.XPATH, '//article[@data-testid="result"]')  # Seleciona os resultados

            for result in search_results:
                try:
                    # Captura o link dentro do resultado
                    link_element = result.find_element(By.XPATH, './/a[@data-testid="result-title-a"]')
                    link = link_element.get_attribute('href')
                    
                    if not link:
                        continue

                    # Extração do domínio e filtragem
                    domain_match = re.search(r'^(?:https?:\/\/)?(?:[^:\/\n]+)', link)
                    if domain_match:
                        domain = domain_match.group(0)
                    else:
                        continue

                    domain_limpo = re.sub(r'\W+', '', domain)
                    
                    # Verifica se o termo de pesquisa está presente no domínio
                    opcao_presente = any(part.lower() in domain_limpo.lower() for part in self.opcao_selecionada.split())
                    if not opcao_presente or self.is_marketplace_or_social(link):
                        continue

                    links_encontrados.append(link)
                
                except Exception as e:
                    sys.stderr.write(json.dumps({"message": f"Erro ao coletar link: {str(e)}"}, ensure_ascii=False) + "\n")
                    continue

            return pd.DataFrame({'link': links_encontrados})
        
        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro ao organizar dados: {str(e)}"}, ensure_ascii=False) + "\n")
            return pd.DataFrame()


    def is_marketplace_or_social(self, link):
        marketplaces = ['amazon.', 'mercadolivre.', 'ebay.', 'aliexpress.', 'buscape.', 'shoptime.', 'casasbahia.', 'magazineluiza.', 'submarino.', 
                        'americanas.', 'shopee.', 'zoom.', 'extra.', 'aliexpress.', 'pontofrio.', 'cliquefarma.', 'mercado', 'drogaraia.', 'loja', 'enjoei.', 
                        'farmacia', 'hotmart.', 'reclameaqui.', 'siteconfiavel.']
        social_networks = ['facebook.', 'twitter.', 'instagram.', 'linkedin.', 'tiktok.', 'youtube.', 'kwai.', 'pinterest.', 'globo.', 'noticia']
        for site in marketplaces + social_networks:
            if site in link:
                return True
        return False

    def exportar_json(self, df):
        try:
            if isinstance(df, pd.DataFrame):
                return df.to_json(orient='records', force_ascii=False)
            else:
                return json.dumps(df, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"message": f"Erro ao exportar dados para JSON: {str(e)}"}, ensure_ascii=False)


if __name__ == "__main__":
    marca = sys.argv[1] if len(sys.argv) > 1 else ""
    if marca:
        scrappy = Scrappy(marca)
        scrappy.iniciar()
    else:
        sys.stderr.write(json.dumps({"message": "Nenhum termo de pesquisa fornecido"}, ensure_ascii=False) + "\n")
