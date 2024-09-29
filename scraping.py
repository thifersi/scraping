import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL do site
url = 'https://www.listamais.com.br/busca?pagina=2&ordemNumero=&inicio=10&termo=Advocacia&campo=todos&localizacao=&codigo=520'

# Fazer a requisição HTTP para obter o conteúdo do site
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar a tabela específica no site (ajuste conforme necessário)
table = soup.find('table')

# Converter tabela HTML em dataframe pandas
df = pd.read_html(str(table))[0]

# Salvar o dataframe em um arquivo Excel
df.to_excel('dados_site.xlsx', index=False)
