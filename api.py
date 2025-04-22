from fastapi import FastAPI, HTTPException, Query, Response, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import structlog
from datetime import datetime, date
import time
from main import dou_client, DOUError

# Configuração de logging
logger = structlog.get_logger()

# Criação da aplicação FastAPI
app = FastAPI(
    title="API DOU",
    description="API para consulta e download de publicações do Diário Oficial da União (DOU)",
    version="1.0.0",
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados
class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class DownloadResponse(BaseModel):
    success: bool
    file_path: Optional[str] = None
    message: Optional[str] = None

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica o status da API"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/dou", response_class=FileResponse)
async def get_dou(
    data: Optional[str] = Query(None, description="Data no formato DD-MM-YYYY"),
    secao: str = Query("1", description="Seção do DOU (1, 2, 3)"),
    formato: str = Query("pdf", description="Formato de saída (pdf, xml)")
):
    """
    Consulta e baixa publicações do DOU
    
    - **data**: Data no formato DD-MM-YYYY (opcional, padrão: data atual)
    - **secao**: Seção do DOU (1, 2, 3) (opcional, padrão: 1)
    - **formato**: Formato de saída (pdf, xml) (opcional, padrão: pdf)
    """
    try:
        # Validação da data
        if data:
            try:
                datetime.strptime(data, "%d-%m-%Y")
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use DD-MM-YYYY")
        
        # Validação da seção
        tipo_dou = f"DO{secao}"
        if secao not in ["1", "2", "3"]:
            raise HTTPException(status_code=400, detail="Seção inválida. Use 1, 2 ou 3")
        
        # Download do arquivo
        start_time = time.time()
        logger.info("iniciando_download", data=data, secao=secao, formato=formato)
        
        if formato.lower() == "pdf":
            file_path = dou_client.download_pdf(data_str=data, tipo_dou=tipo_dou)
        elif formato.lower() == "xml":
            file_path = dou_client.download(data_str=data, tipo_dou=tipo_dou)
        else:
            raise HTTPException(status_code=400, detail="Formato inválido. Use pdf ou xml")
        
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        logger.info("download_concluido", 
                   tempo_execucao=f"{time.time() - start_time:.2f}s",
                   tamanho_arquivo=f"{os.path.getsize(file_path) / 1024 / 1024:.2f}MB")
        
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type="application/pdf" if formato.lower() == "pdf" else "application/xml"
        )
        
    except DOUError as e:
        logger.error("erro_dou", erro=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("erro_inesperado", erro=str(e))
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/docs/openapi.json")
async def get_open_api_endpoint():
    return get_openapi(
        title="API DOU",
        version="1.0.0",
        description="API para consulta e download de publicações do Diário Oficial da União (DOU)",
        routes=app.routes,
    )

# Tratamento de erros
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Erro na requisição", "detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error("erro_nao_tratado", erro=str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": "Erro interno do servidor"},
    )