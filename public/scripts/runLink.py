import sys
import json
import re
import pandas as pd
import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Scrappy:
    def __init__(self, opcao_selecionada):
        self.opcao_selecionada = opcao_selecionada
        self.palavras_proibidas = []  # Será preenchido dinamicamente
        # Configuração do banco de dados
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'capsexpress',
            'password': 'capsadmin',
            'database': 'capsexpress',
            'port': 3306
        }
        self.carregar_palavras_proibidas()  # Carregar as palavras do banco

    def carregar_palavras_proibidas(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM palavrasProibidas;")
            self.palavras_proibidas = [row[1] for row in cursor.fetchall()]
        except Error as e:
            self.palavras_proibidas = []  # Evitar erros no processamento
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def iniciar(self):
        self.link = self.opcao_selecionada
        return self.abrir_link(self.link)

    def abrir_link(self, link):
        service = Service("/usr/local/bin/chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')

        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(link)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            page_content = self.driver.find_element(By.TAG_NAME, 'body').text
            json_data = self.extrair_palavras_proibidas(page_content)
            return json_data
        except Exception as e:
            # Log the error instead of returning it
            log_message = f"Error accessing {link}: {self.tratar_erro(str(e))}"

            # Return a structured result indicating no forbidden words found
            return json.dumps([{
                "link": link,
                "message": "Nenhuma palavra proibida encontrada"
            }], ensure_ascii=False)
        finally:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()

    def tratar_erro(self, error):
        if "ERR_CONNECTION_CLOSED" in error:
            return "Erro: A conexão foi fechada."
        elif "ERR_TIMED_OUT" in error:
            return "Erro: O tempo de conexão expirou."
        elif "ERR_NAME_NOT_RESOLVED" in error:
            return "Erro: O nome do site não pôde ser resolvido."
        elif "unknown error" in error:
            return "Erro: Um erro desconhecido ocorreu."
        else:
            return "Erro: " + error


    def extrair_palavras_proibidas(self, page_content):
        links_encontrados = []
        palavras_encontradas = []

        for palavra_proibida in self.palavras_proibidas:
            if re.search(r'\b' + re.escape(palavra_proibida.lower()) + r'\b', page_content.lower()):
                links_encontrados.append(self.link)
                palavras_encontradas.append(palavra_proibida)

        if not palavras_encontradas:
            result = [{
                "link": self.link,
                "message": "Nenhuma palavra proibida encontrada"
            }]
        else:
            df = pd.DataFrame({
                'link': links_encontrados,
                'palavra_proibida': palavras_encontradas
            })
            result = df.to_json(orient='records', force_ascii=False)

        return result

if __name__ == "__main__":
    link = sys.argv[1] if len(sys.argv) > 1 else ""
    scrappy = Scrappy(link)
    json_output = scrappy.iniciar()

    # Ensure that stdout only outputs valid JSON
    if isinstance(json_output, list):
        json_output = json.dumps(json_output, ensure_ascii=False)

    sys.stdout.write(json_output)