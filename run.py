import uvicorn
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8001"))
    
    print(f"Iniciando API DOU em http://{host}:{port}")
    print("Acesse a documentação em http://localhost:8001/docs")
    
    uvicorn.run("api:app", host=host, port=port, reload=True)