import pandas as pd
import re
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Scrappy:
    def __init__(self, opcao_selecionada):
        self.opcao_selecionada = opcao_selecionada
        self.palavras_proibidas = [
        "Cura",
        "Tratamento",
        "Garantido",
        "Sem riscos",
        "Efeito imediato",
        "Aprovação Anvisa",
        "100% seguro",
        "Resultados permanentes",
        "Aprovado pela FDA",
        "Clinicamente comprovado",
        "Milagroso",
        "Revolucionário",
        "Poderoso",
        "Instantâneo",
        "Sem esforço",
        "Todos os naturais",
        "Sem efeitos colaterais",
        "Testado em laboratório",
        "Pesquisa científica",
        "Fórmula exclusiva",
        "Detox",
        "Queima gordura",
        "Anti-idade",
        "Aumenta a imunidade",
        "Sem contraindicações",
        "Absorção completa",
        "Bio-disponível",
        "Sem aditivos",
        "Sem conservantes",
        "Nutricionista recomendado",
        "Médico aprovado",
        "Fortalece os ossos",
        "Melhora a memória",
        "Antioxidante",
        "Supressor de apetite",
        "Aumenta a energia",
        "Promove o sono",
        "Reduz o estresse",
        "Sem glúten",
        "Orgânico",
        "Vegan",
        "Aumenta a libido",
        "Anticancerígeno",
        "Anti-inflamatório",
        "Regula a tireoide",
        "Sem lactose",
        "Controla a diabetes",
        "Reduz o colesterol",
        "Promove a saúde do coração",
        "Desintoxica o fígado",
        "Perda de peso rápida",
        "Efeito lifting",
        "Rejuvenescedor",
        "Bloqueador de carboidratos",
        "Inibidor de apetite",
        "Remédio natural",
        "Alternativa a medicamentos",
        "Cura natural",
        "Solução definitiva",
        "Desempenho atlético superior",
        "Substituto de refeição",
        "Suplemento milagroso",
        "Resultados em dias",
        "Elimina toxinas",
        "Sem necessidade de exercício",
        "Aumenta a massa muscular",
        "Sem necessidade de dieta",
        "Resultados para toda a vida",
        "Aprovação científica",
        "Reduz sintomas de",
        "Impulsionador de energia",
        "Redução de estresse instantânea",
        "Alívio da dor natural",
        "Melhor que",
        "Alternativa segura a cirurgias",
        "Reduz a pressão arterial",
        "Controla a ansiedade",
        "Combate a depressão",
        "Impede o envelhecimento",
        "Previne doenças crônicas",
        "Promove a saúde cerebral",
        "Fortalece o sistema imunológico",
        "Reduz o risco de doenças cardíacas",
        "Controle de açúcar no sangue",
        "Livre de efeitos colaterais negativos",
        "Pílula da beleza",
        "Solução antienvelhecimento",
        "Efeito detox poderoso",
        "Reduz a fadiga",
        "Estimulante metabólico",
        "Promove a saúde da pele",
        "Cápsula de bem-estar",
        "Melhora a saúde digestiva",
        "Solução para insônia",
        "Reforço imunológico",
        "Potencializa a função cerebral",
        "Supressor de fome",
        "Acelerador de metabolismo",
        "Elixir da juventude",
        "Cápsula energética"
        ];

    def iniciar(self):
        self.termo_pesquisa = self.opcao_selecionada
        self.pesquisa_google()

    def pesquisa_google(self):
        try:
            # Configurando o driver do Chrome em modo headless
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Execução sem interface gráfica
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Realizar a pesquisa sem abrir a janela visível
            self.driver.get('https://www.google.com.br/?h1=pt-BR')

            # Encontrar a barra de pesquisa do Google pelo nome do campo
            search_box = self.driver.find_element(By.NAME, "q")

            # Digitar o termo de pesquisa na barra de pesquisa
            search_box.send_keys(self.termo_pesquisa)
            sleep(2)
            search_box.send_keys(Keys.RETURN)

            # Esperar um pouco para os resultados serem carregados
            sleep(5)

            # Scroll down até o final da página (se necessário)
            self.scroll_to_bottom()

            # Coletar os dados e organizar em um DataFrame
            df = self.organizar_dados()

            # Fechar o navegador
            self.driver.quit()

            # Exportar os dados para JSON e imprimir
            json_data = self.exportar_json(df)
            print(json_data)

        except Exception as e:
            print(json.dumps({"message": f"Erro na pesquisa do Google: {str(e)}"}, ensure_ascii=False))


    def scroll_to_bottom(self):
        while True:
            try:
                # Obter a altura da página atual
                last_height = self.driver.execute_script("return document.body.scrollHeight")

                # Scroll down para o final da página
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Aguardar o carregamento da página
                sleep(2)

                # Calcular nova altura e comparar com a altura anterior
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

                # Procurar pelo botão "Mostrar Mais"
                element = self.driver.find_elements(By.XPATH, '//*[text()="Mais resultados"]')
                if self.driver.find_elements(By.XPATH, '//*[@id="ofr"]'):
                    print("Elemento encontrado. Parando de rolar.")
                    return
                elif element:
                    # Usar JavaScript para clicar no botão "Mais resultados"
                    self.driver.execute_script("arguments[0].click();", element[0])
                    # Aguardar um tempo para o carregamento após clicar em "Mostrar Mais"
                    sleep(2)
                    # Chamar a função scroll_to_bottom() novamente para continuar rolando
                    self.scroll_to_bottom()
                else:
                    print("Element is not present")
            except Exception as e:
                print(json.dumps({"message": f"Erro ao rolar a página: {str(e)}"}, ensure_ascii=False))
                break

    def organizar_dados(self):
        try:
            # Inicializar listas para armazenar os dados
            links_encontrados = []
            palavras_encontradas = []

            # Coletar os dados dos resultados da pesquisa
            search_results = self.driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')
            for result in search_results:
                # Capturar título, URL e snippet
                try:
                    link_element = result.find_element(By.XPATH, './/a')
                    link = link_element.get_attribute('href')
                    title = result.find_element(By.XPATH, './/h3').text

                    # Extrair o domínio do URL
                    domain_match = re.search(r'^(?:https?:\/\/)?(?:[^:\/\n]+)', link)
                    if domain_match:
                        domain = domain_match.group(0)
                    else:
                        continue

                    # Remover caracteres não alfanuméricos da opção selecionada e do domínio
                    domain_limpo = re.sub(r'\W+', '', domain)

                    # Verificar se alguma parte da opção selecionada está presente no domínio
                    opcao_presente = any(part.lower() in domain_limpo.lower() for part in self.opcao_selecionada.split())

                    if not opcao_presente:
                        continue

                    # Verificar se a opcao_selecionada está presente no título ou no domínio
                    if self.opcao_selecionada.lower() in title.lower() or opcao_presente:
                        # Verificar se o link não pertence a um marketplace ou rede social
                        if not self.is_marketplace_or_social(link):
                            # Abrir o link para obter o conteúdo da página
                            self.driver.execute_script("window.open('" + link + "');")
                            sleep(5)  # Esperar o carregamento da página

                            # Trocar para a nova aba
                            self.driver.switch_to.window(self.driver.window_handles[-1])

                            # Obter o conteúdo da página
                            page_content = self.driver.find_element(By.TAG_NAME, 'body').text

                            # Verificar se alguma palavra proibida está presente no conteúdo da página
                            for palavra_proibida in self.palavras_proibidas:
                                # Verificar se a palavra exata está presente usando expressões regulares
                                if re.search(r'\b' + palavra_proibida.lower() + r'\b', page_content.lower()):
                                    links_encontrados.append(link)
                                    palavras_encontradas.append(palavra_proibida)

                            # Fechar a aba atual
                            self.driver.close()

                            # Voltar para a aba original
                            self.driver.switch_to.window(self.driver.window_handles[0])
                except Exception as e:
                    print(f"Erro ao processar o resultado: {e}")
                    continue

                # Recarregar os resultados da pesquisa
                search_results = self.driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')

            # Verificar se há dados coletados
            if not links_encontrados:
                return {"message": "Nenhum dado encontrado para a marca especificada"}

            # Criar um DataFrame do Pandas com os dados coletados
            df = pd.DataFrame({
                'Marca': [self.opcao_selecionada] * len(links_encontrados),
                'Link': links_encontrados,
                'Palavra Proibida': palavras_encontradas
            })

            return df
        except Exception as e:
            return {"message": f"Erro ao organizar dados: {str(e)}"}

    def is_marketplace_or_social(self, link):
        # Lista de partes específicas de URLs de marketplaces e redes sociais
        marketplaces = ['amazon.', 'mercadolivre.', 'ebay.', 'aliexpress.', 'buscape.', 'shoptime.', 'casasbahia.', 'magazineluiza.', 'submarino.',
                        'americanas.', 'shopee.', 'zoom.', 'extra.', 'aliexpress.', 'pontofrio.', 'cliquefarma.', 'mercado', 'drogaraia.', 'loja', 'enjoei.',
                        'farmacia', 'hotmart.', 'reclameaqui.', 'siteconfiavel.', 'siteconfiavel.']
        social_networks = ['facebook.', 'twitter.', 'instagram.', 'linkedin.', 'tiktok.', 'youtube.', 'kwai.', 'pinterest.', 'globo.', 'noticia']

        # Verificar se o link contém alguma parte específica de URLs de marketplaces ou redes sociais
        for site in marketplaces + social_networks:
            if site in link or link.startswith(site):
                return True

        return False

    def exportar_json(self, df):
        try:
            # Verificar se df é um DataFrame
            if isinstance(df, pd.DataFrame):
                # Convertendo DataFrame para JSON
                json_data = df.to_json(orient='records', force_ascii=False)
            else:
                # Convertendo o dicionário para JSON
                json_data = json.dumps(df, ensure_ascii=False)
            return json_data
        except Exception as e:
            return json.dumps({"message": f"Erro ao exportar dados para JSON: {str(e)}"}, ensure_ascii=False)


if __name__ == "__main__":
    # Obter a marca como argumento da linha de comando
    import sys
    marca = sys.argv[1] if len(sys.argv) > 1 else ""

    # Exemplo de uso da classe Scrappy com a marca como argumento
    scrappy = Scrappy(marca)
    scrappy.iniciar()
