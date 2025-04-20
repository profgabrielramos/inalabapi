from datetime import date
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Credenciais do DOU
login = os.getenv("DOU_LOGIN")
senha = os.getenv("DOU_PASSWORD")

tipo_dou="DO1 DO2 DO3 DO1E DO2E DO3E" # Seções separadas por espaço
# Opções DO1 DO2 DO3 DO1E DO2E DO3E

url_login = "https://inlabs.in.gov.br/logar.php"
url_download = "https://inlabs.in.gov.br/index.php?p="

payload = {"email": login, "password": senha}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
s = requests.Session()

def obter_data():
    ano = date.today().strftime("%Y")
    mes = date.today().strftime("%m")
    dia = date.today().strftime("%d")
    return ano, mes, dia, f"{ano}-{mes}-{dia}"

def verificar_cookie():
    if s.cookies.get('inlabs_session_cookie'):
        return s.cookies.get('inlabs_session_cookie')
    else:
        print("Falha ao obter cookie. Verifique suas credenciais")
        exit(37)

def download():
    cookie = verificar_cookie()
    ano, mes, dia, data_completa = obter_data()
    
    for dou_secao in tipo_dou.split(' '):
        print("Aguarde Download...")
        url_arquivo = f"{url_download}{data_completa}&dl={data_completa}-{dou_secao}.zip"
        cabecalho_arquivo = {'Cookie': f'inlabs_session_cookie={cookie}', 'origem': '736372697074'}
        response_arquivo = s.request("GET", url_arquivo, headers=cabecalho_arquivo)
        
        if response_arquivo.status_code == 200:
            with open(f"{data_completa}-{dou_secao}.zip", "wb") as f:
                f.write(response_arquivo.content)
                print(f"Arquivo {data_completa}-{dou_secao}.zip salvo.")
        elif response_arquivo.status_code == 404:
            print(f"Arquivo não encontrado: {data_completa}-{dou_secao}.zip")
    
    print("Aplicação encerrada")
    exit(0)

def download_pdf():
    cookie = verificar_cookie()
    ano, mes, dia, data_completa = obter_data()
    
    for dou_secao in tipo_dou.split(' '):
        print("Aguarde Download...")
        url_arquivo = f"{url_download}{data_completa}&dl={ano}_{mes}_{dia}_ASSINADO_{dou_secao}.pdf"
        cabecalho_arquivo = {'Cookie': f'inlabs_session_cookie={cookie}', 'origem': '736372697074'}
        response_arquivo = s.request("GET", url_arquivo, headers=cabecalho_arquivo)
        
        if response_arquivo.status_code == 200:
            with open(f"{data_completa}-{dou_secao}.pdf", "wb") as f:
                f.write(response_arquivo.content)
                print(f"Arquivo {ano}_{mes}_{dia}_ASSINADO_{dou_secao}.pdf salvo.")
        elif response_arquivo.status_code == 404:
            print(f"Arquivo não encontrado: {ano}_{mes}_{dia}_ASSINADO_{dou_secao}.pdf")
    
    print("Aplicação encerrada")
    exit(0)

def login(download_func=download):
    try:
        s.request("POST", url_login, data=payload, headers=headers)
        download_func()
    except requests.exceptions.ConnectionError:
        login(download_func)

# Iniciar download de arquivos ZIP
login()
