from datetime import date, datetime
import requests
import os
import structlog
from dotenv import load_dotenv
from typing import Optional, Tuple, Union
from cache import cached, clear_cache
from resilience import resilient_call, circuit_breaker, retry_with_exponential_backoff

# Configuração de logging
logger = structlog.get_logger()

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
DOU_LOGIN = os.getenv("DOU_LOGIN")
DOU_PASSWORD = os.getenv("DOU_PASSWORD")
DOU_TIMEOUT = int(os.getenv("DOU_TIMEOUT", "30"))
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
CACHE_DIR = os.getenv("CACHE_DIR", ".cache")

# URLs do DOU
URL_LOGIN = "https://inlabs.in.gov.br/logar.php"
URL_DOWNLOAD = "https://inlabs.in.gov.br/index.php?p="

class DOUError(Exception):
    """Exceção personalizada para erros do DOU"""
    pass

class DOUClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        })
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Garante que o diretório de cache existe"""
        os.makedirs(CACHE_DIR, exist_ok=True)

    @staticmethod
    def obter_data(data_str: Optional[str] = None) -> Tuple[str, str, str, str]:
        """Converte a data do formato DD-MM-YYYY para os formatos necessários"""
        if data_str:
            try:
                data = datetime.strptime(data_str, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Data inválida. Use o formato DD-MM-YYYY")
        else:
            data = date.today()

        return (
            data.strftime("%Y"),
            data.strftime("%m"),
            data.strftime("%d"),
            data.strftime("%Y-%m-%d")
        )

    @circuit_breaker()
    @retry_with_exponential_backoff()
    def _get_cookie(self) -> str:
        """Obtém o cookie de sessão do DOU"""
        if not DOU_LOGIN or not DOU_PASSWORD:
            raise DOUError("Credenciais do DOU não configuradas")

        try:
            response = self.session.post(
                URL_LOGIN,
                data={"email": DOU_LOGIN, "password": DOU_PASSWORD},
                timeout=DOU_TIMEOUT
            )
            response.raise_for_status()
            
            cookie = self.session.cookies.get('inlabs_session_cookie')
            if not cookie:
                raise DOUError("Falha ao obter cookie de sessão")
            
            return cookie
        except requests.exceptions.RequestException as e:
            logger.error("erro_obter_cookie", error=str(e))
            raise DOUError(f"Erro de conexão com o DOU: {str(e)}")

    @cached(prefix="dou_download", ttl=CACHE_TTL)
    def download(self, data_str: Optional[str] = None, tipo_dou: str = "DO1") -> Optional[str]:
        """Download do arquivo XML do DOU"""
        try:
            cookie = self._get_cookie()
            ano, mes, dia, data_completa = self.obter_data(data_str)
            
            logger.info("iniciando_download_dou", tipo_dou=tipo_dou, data=data_completa)
            url_arquivo = f"{URL_DOWNLOAD}{data_completa}&dl={data_completa}-{tipo_dou}.zip"
            
            response = resilient_call(
                self.session.get,
                url_arquivo,
                headers={'Cookie': f'inlabs_session_cookie={cookie}', 'origem': '736372697074'},
                timeout=DOU_TIMEOUT
            )
            
            if response.status_code == 200:
                filepath = os.path.join(CACHE_DIR, f"{data_completa}-{tipo_dou}.zip")
                with open(filepath, "wb") as f:
                    f.write(response.content)
                logger.info("arquivo_salvo", filepath=filepath)
                return filepath
            elif response.status_code == 404:
                logger.warning("arquivo_nao_encontrado", arquivo=f"{data_completa}-{tipo_dou}.zip")
                return None
            else:
                raise DOUError(f"Erro ao baixar arquivo: {response.status_code}")
                
        except Exception as e:
            logger.error("erro_download", error=str(e))
            raise

    @cached(prefix="dou_download_pdf", ttl=CACHE_TTL)
    def download_pdf(self, data_str: Optional[str] = None, tipo_dou: str = "DO1") -> Optional[str]:
        """Download do arquivo PDF do DOU"""
        try:
            cookie = self._get_cookie()
            ano, mes, dia, data_completa = self.obter_data(data_str)
            
            logger.info("iniciando_download_pdf", tipo_dou=tipo_dou, data=data_completa)
            url_arquivo = f"{URL_DOWNLOAD}{data_completa}&dl={ano}_{mes}_{dia}_ASSINADO_{tipo_dou}.pdf"
            
            response = resilient_call(
                self.session.get,
                url_arquivo,
                headers={'Cookie': f'inlabs_session_cookie={cookie}', 'origem': '736372697074'},
                timeout=DOU_TIMEOUT
            )
            
            if response.status_code == 200:
                filepath = os.path.join(CACHE_DIR, f"{data_completa}-{tipo_dou}.pdf")
                with open(filepath, "wb") as f:
                    f.write(response.content)
                logger.info("arquivo_salvo", filepath=filepath)
                return filepath
            elif response.status_code == 404:
                logger.warning("arquivo_nao_encontrado", arquivo=f"{ano}_{mes}_{dia}_ASSINADO_{tipo_dou}.pdf")
                return None
            else:
                raise DOUError(f"Erro ao baixar arquivo: {response.status_code}")
                
        except Exception as e:
            logger.error("erro_download_pdf", error=str(e))
            raise

# Instância global do cliente DOU
dou_client = DOUClient()