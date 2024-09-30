"""
Este script utiliza Selenium para fazer scraping de uma página web
usando o ChromeDriver e captura o conteúdo HTML da página.
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
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'resultado-busca-gratuito')))

# Captura o HTML após o carregamento completo e execução do JavaScript
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Encontrar os blocos de informações de empresas
companies = []
for company in soup.find_all('div', class_='resultado-busca-gratuito'):
    nome = company.find('h2', class_='bd-name-empresa').text.strip()
    endereco = company.find('div', class_='endereco-empresa-gratuito').text.strip()
    # Capturar o número da classe 'idAnalytics', mesmo com display:none
    try:
        telefone = company.find('div', class_='idAnalytics').text.strip()
    except AttributeError:
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
