# 🤖 Sistema RAG: Ingestão e Busca Semântica

Sistema completo de **Retrieval-Augmented Generation (RAG)** com ingestão de documentos PDF/TXT, embeddings, busca semântica e chat interativo.

## 🎯 Funcionalidades

- ✅ **Ingestão de PDF/TXT** com chunking inteligente
- ✅ **Embeddings** com suporte a Gemini e OpenAI
- ✅ **Armazenamento vetorial** em PostgreSQL + pgVector
- ✅ **Busca semântica** por similaridade
- ✅ **Chat RAG** com LLM integrado
- ✅ **Fallback robusto** para modo estudo
- ✅ **Interface interativa** amigável

## 📋 Pré-requisitos

- **Python 3.12+**
- **PostgreSQL** com extensão **pgVector** (LangChain cria tabelas automaticamente)
- **API Keys** (opcional, tem modo estudo):
  - Google AI Studio (Gemini)
  - OpenAI (opcional)

## 🚀 Instalação

### 1. Clonar o projeto
```bash
git clone <repository-url>
cd mba-ia-desafio-ingestao-busca
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Copie e edite o arquivo `.env`:
```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:
```env
# Gemini API Key (opcional)
GOOGLE_API_KEY=sua-gemini-api-key-aqui

# OpenAI API Key (opcional)
OPENAI_API_KEY=sk-sua-openai-key-aqui

# Caminho do documento para ingestão
PDF_PATH=./documentos/documento.pdf

# String de conexão PostgreSQL
POSTGRES_CONNECTION_STRING=postgresql+psycopg2://postgres:sua-senha@localhost:5432/rag
```

## 🏃‍♂️ Execução

### 1. Ingestão de Documentos
```bash
python src/ingest.py
```

**O que acontece:**
- 🔄 Carrega o PDF/TXT
- ✂️ Divide em chunks (1000 caracteres, 150 overlap)
- 🧠 Gera embeddings (com fallback automático)
- 💾 Armazena no PostgreSQL
- 🔍 Testa busca semântica

### 2. Chat Interativo
```bash
python src/chat.py
```

**Exemplos de uso:**
```
🔍 Sua pergunta: faturamento
🔍 Sua pergunta: clientes
🔍 Sua pergunta: relatório financeiro
```

### 3. Verificar Modelos Disponíveis
```bash
python src/check_models.py
```

## 🔄 Modo de Operação

### Modo Produção (com API Keys)
- **Gemini embeddings** → **OpenAI embeddings** → **Erro**
- **Gemini LLM** → **OpenAI LLM** → **Erro**

### Modo Estudo (sem API Keys)
- **Embeddings mock** (vetores fixos de 1536 dimensões)
- **Busca semântica** funciona normalmente
- **Retorno de contexto bruto** (sem LLM)

## 📁 Estrutura do Projeto

```
├── src/
│   ├── ingest.py          # Ingestão de documentos
│   ├── search.py          # Busca semântica + LLM
│   ├── chat.py            # Interface de chat
│   └── check_models.py    # Verificar modelos Gemini
├── pdfs/                  # Documentos para ingestão
├── .env                   # Variáveis de ambiente
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 🛠️ Tecnologias

- **LangChain**: Framework principal
- **PostgreSQL + pgVector**: Banco vetorial
- **Gemini API**: Embeddings e LLM
- **OpenAI API**: Fallback embeddings/LLM
- **PyPDF**: Processamento de PDFs
- **Python-dotenv**: Gestão de variáveis

## 🔧 Configuração Avançada

### Chunking
- **chunk_size**: 1000 caracteres
- **chunk_overlap**: 150 caracteres
- **Separadores**: `\n\n`, `\n`, ` `, `""`

### Embeddings
- **Gemini**: `text-embedding-004`
- **OpenAI**: `text-embedding-3-small`
- **Mock**: `[0.1] * 1536` (modo estudo)

### Busca Semântica
- **k**: 3 documentos mais similares
- **threshold**: Similaridade coseno
- **task_type**: `retrieval_query`


## 📊 Exemplo de Saída

### Ingestão
```
🔄 Carregando PDF...
✅ PDF carregado: 34 páginas
✂️ Dividindo em chunks...
✅ Documento dividido em 67 chunks
🧪 Modo estudo: sem embeddings (apenas texto)
✅ 67 chunks armazenados com embeddings mock!
🔍 Testando busca...
✅ Teste de busca: 2 resultados encontrados
```

### Chat
```
🤖 Iniciando sistema de chat RAG...
✅ Sistema RAG pronto!
💡 Digite 'sair' para encerrar

🔍 Sua pergunta: faturamento
🔄 Processando...
✅ Encontrados 3 documentos
📝 RESPOSTA:
CONTEXTO ENCONTRADO:
[documentos relevantes sobre faturamento...]
```

## 🎓 Para Estudo

Este projeto é ideal para aprender:
- **Embeddings** e vetores
- **Busca semântica** com pgVector
- **RAG** (Retrieval-Augmented Generation)
- **Fallback patterns** em produção
- **LangChain** e ecossistema

## 📝 Licença

MIT License - uso livre para estudo e desenvolvimento.

## 🤝 Contribuições

Contribuições são bem-vindas! Abra issues para bugs e pull requests para melhorias.