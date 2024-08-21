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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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

        manifest = ChromeProxy.manifest_json
        manifest = manifest.replace("<ext_name>", name)
        manifest = manifest.replace("<ext_ver>", version)

        with open(f"{proxy_folder}/manifest.json", "w") as f:
            f.write(manifest)

        js = ChromeProxy.background_js
        js = js.replace("<proxy_host>", self.host)
        js = js.replace("<proxy_port>", str(self.port))
        js = js.replace("<proxy_username>", self.username)
        js = js.replace("<proxy_password>", self.password)

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
        self.pesquisa_google()

    def pesquisa_google(self):
        proxy = ChromeProxy(
            host="43.159.28.126",
            port=2333,
            username="u66cd4bf7547005a8-zone-custom-region-br-asn-AS52748",
            password="u66cd4bf7547005a8"
        )
        extension_path = proxy.create_extension()
        
        service = Service('C:\\Users\\User\\Desktop\\chromedriver.exe')
        options = uc.ChromeOptions()
        options.add_argument(f"--load-extension={extension_path}")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--headless')

        try:
            self.driver = uc.Chrome(service=service, options=options)
            self.driver.get('https://www.google.com.br/?h1=pt-BR')

            search_box = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.NAME, "q")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
            self.driver.execute_script("arguments[0].style.visibility='visible';", search_box)
            search_box.clear()
            search_box.send_keys(self.termo_pesquisa)
            sleep(2)
            search_box.send_keys(Keys.RETURN)

            sleep(3)
            self.scroll_to_bottom()

            df = self.organizar_dados()
            json_data = self.exportar_json(df)
            print(json_data)

        except Exception as e:
            sys.stderr.write(json.dumps({"message": f"Erro na pesquisa do Google: {str(e)}"}, ensure_ascii=False) + "\n")

    def scroll_to_bottom(self):
        while True:
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                sleep(2)
                element = self.driver.find_elements(By.XPATH, '//*[text()="Mais resultados"]')
                if self.driver.find_elements(By.XPATH, '//*[@id="ofr"]'):
                    return
                elif element:
                    self.driver.execute_script("arguments[0].click();", element[0])
                    sleep(2)
                else:
                    next_page = self.driver.find_elements(By.XPATH, '//a[@id="pnnext"]')
                    if next_page:
                        self.driver.execute_script("arguments[0].click();", next_page[0])
                        sleep(2)
                    else:
                        break
            except Exception as e:
                sys.stderr.write(json.dumps({"message": f"Erro ao rolar a página: {str(e)}"}, ensure_ascii=False) + "\n")
                break

    def organizar_dados(self):
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
                    sleep(2)
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