# API DOU

API para consulta e download de publicações do Diário Oficial da União (DOU).

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/profgabrielramos/inalabapi.git
cd inalabapi
```

2. Crie e ative o ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

3. Instale as dependências usando uv:
```bash
brew install uv  # Se ainda não tiver o uv instalado
uv pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Executando a API

1. Inicie o servidor:
```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

2. Acesse a documentação da API:
```
http://localhost:8001/docs
```

## Endpoints

- `GET /api/v1/dou`: Consulta publicações do DOU
  - Parâmetros:
    - `data`: Data no formato DD-MM-YYYY
    - `secao`: Seção do DOU (1, 2, 3, etc)
    - `formato`: Formato de saída (pdf, html)

## Docker

Para executar usando Docker:

```bash
docker build -t profgabrielramos/inalabapi:latest .
docker run -p 8001:8001 profgabrielramos/inalabapi:latest
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🌐 API em Produção

A API está disponível em: [https://dou.proframos.com](https://dou.proframos.com)

## 🚀 Funcionalidades

- Consulta por data específica (formato DD-MM-YYYY)
- Seleção de seção (01, 02 ou 03)
- Download em múltiplos formatos (XML e PDF)
- Interface simples e intuitiva
- Hospedagem em VPS com Traefik
- Cache para melhor performance
- Logs detalhados para monitoramento

## 📋 Pré-requisitos

- Python 3.11 ou superior
- [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências
- Acesso à internet para download dos arquivos

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte, envie um email para [gabrielgfcramos@outlook.com](mailto:gabrielgfcramos@outlook.com) ou abra uma issue no GitHub.

---
⌨️ com ❤️ por [Gabriel Ramos](https://github.com/profgabrielramos)