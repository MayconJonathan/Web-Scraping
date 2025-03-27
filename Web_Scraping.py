## 1. TESTE DE WEB SCRAPING -  Este teste deve ser realizado nas linguagens Python ou Java. E o código deverá executar o/a:

import os
import requests
from bs4 import BeautifulSoup
import zipfile
import re

###### 1.1. Acesso ao site: https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-dasociedade/atualizacao-do-rol-de-procedimentos #####

## URL do site para scraping:
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

# Enviar requisição HTTP para o site
response = requests.get(url)

if response.status_code == 200:
    print("Página acessada com sucesso.")
else:
    print(f"Erro ao acessar a página. Código de status: {response.status_code}")


##### 1.2. Download dos Anexos I e II em formato PDF: #####

# Analisando o conteúdo da página com BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Usando expressão regular para encontrar links com 'anexo' no nome e terminando com .pdf
download_links = [link['href'] for link in soup.find_all('a', href=True) if re.search(r'Anexo.*\.pdf$', link['href'])]

os.makedirs('downloads', exist_ok=True)


def baixar_arquivos():
    for link in download_links:
        # Extrair o nome do arquivo da URL
        filename = link.split('/')[-1]
        file_path = os.path.join('downloads', filename)

        # Baixar o arquivo
        print(f'Baixando {filename}...')
        file_response = requests.get(link)
        with open(file_path, 'wb') as f:
            f.write(file_response.content)
        print(f'{filename} baixado.')

## 1.3. Compactação de todos os anexos em um único arquivo (formatos ZIP, RAR, etc.).

def compactar_arquivos_zip():
    arquivo_zip = 'anexos.zip'
    
    with zipfile.ZipFile(arquivo_zip, 'w') as zipf:
        for root, dirs, files in os.walk('downloads'):
            for file in files:
                if file.endswith('.pdf'):  # Adiciona apenas arquivos .pdf
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, 'downloads'))
    
    print(f'Arquivos compactados em {arquivo_zip}')

# Executar função de download
baixar_arquivos()
# Executar a compactação em ZIP
compactar_arquivos_zip()
