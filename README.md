# InaLabAPI

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)]()
[![API](https://img.shields.io/badge/API-dou.proframos.com-blue.svg)](https://dou.proframos.com)
[![Docker](https://img.shields.io/badge/Docker-Available-blue.svg)](https://hub.docker.com/r/profgabrielramos/inalabapi)

API não oficial para acesso aos dados do Diário Oficial da União (DOU), desenvolvida para facilitar o acesso e download de informações publicadas.

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

## 🔧 Instalação

### Via Docker (Recomendado)

1. Clone o repositório:
```bash
git clone git@github.com:profgabrielramos/inalabapi.git
cd inalabapi
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Inicie o container:
```bash
docker-compose up -d
```

### Via Portainer

1. No Portainer, vá para "Stacks"
2. Clique em "Add stack"
3. Cole o conteúdo do arquivo `docker-compose.yml`
4. Configure as variáveis de ambiente necessárias
5. Clique em "Deploy the stack"

### Via Python (Desenvolvimento)

1. Clone o repositório:
```bash
git clone git@github.com:profgabrielramos/inalabapi.git
cd inalabapi
```

2. Crie e ative o ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate  # No macOS/Linux
```

3. Instale as dependências usando uv:
```bash
uv pip install -r requirements.txt
```

## 🛠️ Configuração

1. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

2. Configure as variáveis de ambiente no arquivo `.env`

## 🚀 Como Usar

### Via API Web

Acesse a interface web em: [https://dou.proframos.com](https://dou.proframos.com)

### Via API REST

#### Download de PDF
```
GET https://dou.proframos.com/api/v1/dou?data=20-04-2024&secao=01&formato=pdf
```

#### Download de XML
```
GET https://dou.proframos.com/api/v1/dou?data=20-04-2024&secao=02&formato=xml
```

### Parâmetros da API

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| data | Data no formato DD-MM-YYYY | 20-04-2024 |
| secao | Seção do DOU (01, 02 ou 03) | 01 |
| formato | Formato do arquivo (pdf ou xml) | pdf |

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autor

- **Gabriel Ramos** - *Trabalho Inicial* - [profgabrielramos](https://github.com/profgabrielramos)

## 📞 Suporte

Para suporte, envie um email para [gabrielgfcramos@outlook.com](mailto:gabrielgfcramos@outlook.com) ou abra uma issue no GitHub.

---
⌨️ com ❤️ por [Gabriel Ramos](https://github.com/profgabrielramos)