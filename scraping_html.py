"""
Este script utiliza Selenium para acessar múltiplas páginas de uma pesquisa,
extrair dados de empresas e exportá-los para uma única planilha Excel usando a biblioteca pandas.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configura o serviço do ChromeDriver
CHROMEDRIVER_PATH = 'c:/path/to/chromedriver.exe'
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Função para capturar dados de uma página
def captura_dados_pagina(soup_dados):
    companies = []
    empresas = soup_dados.find_all('div', class_='resultado-busca-gratuito')
    telefones = soup_dados.find_all('div', class_='idAnalytics')

    for idx, company in enumerate(empresas):
        nome = company.find('h2', class_='bd-name-empresa').text.strip()
        endereco = company.find('div', class_='endereco-empresa-gratuito').text.strip()

        if idx < len(telefones):
            telefone = telefones[idx].text.strip()
        else:
            telefone = "Telefone não disponível"

        companies.append({
            'Nome': nome,
            'Telefone': telefone,
            'Endereço': endereco
        })
    return companies

# Função para navegar pelas páginas e coletar os dados
todos_dados = []
pagina_atual = 1
while True:
    try:
        url = f'https://www.listamais.com.br/busca?pagina={pagina_atual}&ordemNumero=37&inicio=10&termo=informatica&campo=todos&localizacao=&codigo=520'
        driver.get(url)

        # Aguardar o carregamento da página
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'resultado-busca-gratuito')))

        # Capturar e analisar o HTML da página
        html_pagina = driver.page_source
        soup_dados = BeautifulSoup(html_pagina, 'html.parser')

        # Capturar os dados da página atual
        dados_pagina = captura_dados_pagina(soup_dados)
        todos_dados.extend(dados_pagina)

        # Verificar se existe um botão para a próxima página
        botao_proxima_pagina = soup_dados.find('a', class_='pagination-next')
        if botao_proxima_pagina:
            pagina_atual += 1  # Avança para a próxima página
            time.sleep(2)  # Pequena pausa entre as páginas
        else:
            break  # Não há mais páginas, saímos do loop
    except Exception as e:
        print(f"Erro ao capturar dados da página {pagina_atual}: {e}")
        break

# Fecha o navegador
driver.quit()

# Converte os dados em um DataFrame do pandas
df = pd.DataFrame(todos_dados)

# Exporta todos os dados para um único arquivo Excel
df.to_excel('dados_empresas_todas_paginas.xlsx', index=False)
print("Dados exportados para 'dados_empresas_todas_paginas.xlsx'")
