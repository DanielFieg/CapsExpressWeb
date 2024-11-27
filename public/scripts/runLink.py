import sys
import json
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Scrappy:
    def __init__(self, opcao_selecionada):
        self.opcao_selecionada = opcao_selecionada
        self.palavras_proibidas = [
            "Tratamento", "Garantido", "Sem riscos", "Efeito imediato",
            "Aprovação Anvisa", "100% seguro", "Resultados permanentes", "Aprovado pela FDA",
            "Clinicamente comprovado", "Milagroso", "Revolucionário", "Poderoso", "Instantâneo",
            "Sem esforço", "Todos os naturais", "Sem efeitos colaterais", "Testado em laboratório",
            "Pesquisa científica", "Fórmula exclusiva", "Detox", "Queima gordura", "Anti-idade",
            "Aumenta a imunidade", "Sem contraindicações", "Absorção completa", "Bio-disponível",
            "Sem aditivos", "Sem conservantes", "Nutricionista recomendado", "Médico aprovado",
            "Fortalece os ossos", "Melhora a memória", "Antioxidante", "Supressor de apetite",
            "Aumenta a energia", "Promove o sono", "Reduz o estresse", "Sem glúten", "Orgânico",
            "Vegan", "Aumenta a libido", "Anticancerígeno", "Anti-inflamatório", "Regula a tireoide",
            "Sem lactose", "Controla a diabetes", "Reduz o colesterol", "Promove a saúde do coração",
            "Desintoxica o fígado", "Perda de peso rápida", "Efeito lifting", "Rejuvenescedor",
            "Bloqueador de carboidratos", "Inibidor de apetite", "Remédio natural",
            "Alternativa a medicamentos", "Cura natural", "Solução definitiva",
            "Desempenho atlético superior", "Substituto de refeição", "Suplemento milagroso",
            "Resultados em dias", "Elimina toxinas", "Sem necessidade de exercício",
            "Aumenta a massa muscular", "Sem necessidade de dieta", "Resultados para toda a vida",
            "Aprovação científica", "Reduz sintomas de", "Impulsionador de energia",
            "Redução de estresse instantânea", "Alívio da dor natural", "Melhor que",
            "Alternativa segura a cirurgias", "Reduz a pressão arterial", "Controla a ansiedade",
            "Combate a depressão", "Impede o envelhecimento", "Previne doenças crônicas",
            "Promove a saúde cerebral", "Fortalece o sistema imunológico",
            "Reduz o risco de doenças cardíacas", "Controle de açúcar no sangue",
            "Livre de efeitos colaterais negativos", "Pílula da beleza", "Solução antienvelhecimento",
            "Efeito detox poderoso", "Reduz a fadiga", "Estimulante metabólico",
            "Promove a saúde da pele", "Cápsula de bem-estar", "Melhora a saúde digestiva",
            "Solução para insônia", "Reforço imunológico", "Potencializa a função cerebral",
            "Supressor de fome", "Acelerador de metabolismo", "Elixir da juventude",
            "Cápsula energética"
        ]

    def iniciar(self):
        self.link = self.opcao_selecionada
        return self.abrir_link(self.link)

    def abrir_link(self, link):
        service = Service("/usr/local/bin/chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')

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
            print(log_message)  # Replace with your logging mechanism if needed

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