"""
Este script utiliza Selenium para fazer scraping de uma página web
usando o ChromeDriver e captura o conteúdo HTML da página.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd

# Configura o serviço do ChromeDriver
CHROMEDRIVER_PATH = 'c:/path/to/chromedriver.exe'
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Acessa o site
driver.get('https://www.listamais.com.br/busca?pagina=2&ordemNumero=&inicio=10&termo=Advocacia&campo=todos&localizacao=&codigo=520')

# Captura o HTML da página
html = driver.page_source

# Usa o BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html, 'lxml')

# Encontrar os blocos de informações de empresas
companies = []
for company in soup.find_all('id', class_='class_do_bloco_de_empresa'):  # Troque pela classe correta
    nome = company.find('cli_nome').text  # Troque pela tag correta
    endereco = company.find('end_completo', class_='endereco').text  # Troque pela classe correta
    telefone = company.find('telefones_negocios', class_='telefone').text  # Troque pela classe correta
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
