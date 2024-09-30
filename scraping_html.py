"""
Este script utiliza Selenium para acessar uma página web, extrair dados de empresas e
exportá-los para uma planilha Excel usando a biblioteca pandas.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Configura o serviço do ChromeDriver
CHROMEDRIVER_PATH = 'c:/path/to/chromedriver.exe'
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Acessa o site
driver.get('https://www.listamais.com.br/busca?pagina=2&ordemNumero=&inicio=10&termo=Advocacia&campo=todos&localizacao=&codigo=520')

# Aguardar a página carregar completamente
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'resultado-busca-gratuito')))

# Captura o HTML após o carregamento
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Encontrar os blocos de informações de empresas
companies = []
empresas = soup.find_all('div', class_='resultado-busca-gratuito')

# Captura todos os números de telefone na classe 'idAnalytics'
telefones = soup.find_all('div', class_='idAnalytics')

# Iterar por cada empresa e associar com o número de telefone
for idx, company in enumerate(empresas):
    nome = company.find('h2', class_='bd-name-empresa').text.strip()
    endereco = company.find('div', class_='endereco-empresa-gratuito').text.strip()

    # Verifica se o índice do telefone é válido
    if idx < len(telefones):
        telefone = telefones[idx].text.strip()
    else:
        telefone = "Telefone não disponível"

    companies.append({
        'Nome': nome,
        'Endereço': endereco,
        'Telefone': telefone
    })

# Fecha o navegador
driver.quit()

# Converte os dados em um DataFrame do pandas
df = pd.DataFrame(companies)

# Exporta para um arquivo Excel
df.to_excel('dados_empresas.xlsx', index=False)
print("Dados exportados para 'dados_empresas.xlsx'")
