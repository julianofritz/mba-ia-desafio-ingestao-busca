PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

def search_prompt(question=None):
    """Função completa de busca semântica + LLM com fallback robusto"""
    
    def try_gemini_embeddings():
        """Tenta embeddings Gemini"""
        models = ["text-embedding-004", "embedding-001", "models/embedding-001", "models/text-embedding-004"]
        
        for model in models:
            try:
                print(f"🧠 Tentando Gemini modelo: {model}")
                embeddings = GoogleGenerativeAIEmbeddings(
                    model=model,
                    task_type="retrieval_query"
                )
                # Testa se funciona
                embeddings.embed_query("test")
                print(f"✅ Gemini embeddings funcionando: {model}")
                return embeddings
            except Exception as e:
                print(f"❌ Gemini modelo {model} falhou: {e}")
                continue
        
        return None
    
    def try_openai_embeddings():
        """Tenta embeddings OpenAI"""
        try:
            print("🔄 Tentando OpenAI embeddings...")
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            # Testa se funciona
            embeddings.embed_query("test")
            print("✅ OpenAI embeddings funcionando")
            return embeddings
        except Exception as e:
            print(f"❌ OpenAI embeddings falhou: {e}")
            return None
    
    def try_mock_embeddings():
        """Modo estudo com embeddings mock"""
        print("🧪 Modo estudo: embeddings mock")
        class MockEmbeddings:
            def embed_query(self, text):
                return [0.1] * 1536
        embeddings = MockEmbeddings()
        print("✅ Usando embeddings mock")
        return embeddings
    
    def try_gemini_llm():
        """Tenta LLM Gemini"""
        try:
            print("🤖 Configurando LLM com Gemini...")
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
            print("✅ Usando Gemini LLM")
            return llm
        except Exception as e:
            print(f"❌ Gemini LLM falhou: {e}")
            return None
    
    def try_openai_llm():
        """Tenta LLM OpenAI"""
        try:
            print("🔄 Tentando OpenAI LLM...")
            llm = ChatOpenAI(model="gpt-3.5-turbo")
            print("✅ Usando OpenAI LLM")
            return llm
        except Exception as e:
            print(f"❌ OpenAI LLM falhou: {e}")
            return None
    
    # 1. Tentar embeddings em cascata
    embeddings = try_gemini_embeddings()
    if not embeddings:
        embeddings = try_openai_embeddings()
    if not embeddings:
        embeddings = try_mock_embeddings()
    
    # 2. Conectar ao banco vetorial
    try:
        connection_string = os.getenv("POSTGRES_CONNECTION_STRING")
        vector_store = PGVector(
            connection=connection_string,
            embeddings=embeddings,
            collection_name="document_chunks"
        )
        print("✅ Conectado ao banco vetorial")
    except Exception as e:
        print(f"❌ Erro no banco: {e}")
        return None
    
    # 3. Tentar LLM em cascata
    llm = try_gemini_llm()
    if not llm:
        llm = try_openai_llm()
    
    if not llm:
        print("🧪 Modo estudo: sem LLM")
    
    # 4. Criar prompt template
    prompt = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )
    
    # 5. Criar chain
    chain = None
    if llm:
        try:
            chain = LLMChain(llm=llm, prompt=prompt)
            print("✅ Chain criada com LLM")
        except Exception as e:
            print(f"❌ Erro na chain: {e}")
            chain = None
    
    if not chain:
        print("⚠️ Chain criada sem LLM (modo busca apenas)")
    
    # 6. Função de busca
    def search_and_answer(question):
        """Busca documentos e gera resposta"""
        
        print(f"🔍 Buscando: '{question}'")
        
        # Busca semântica
        try:
            docs = vector_store.similarity_search(question, k=10)
            print(f"✅ Encontrados {len(docs)} documentos")
            
            # Combinar contexto
            context = "\n\n".join([doc.page_content for doc in docs])
            print(f"📄 Contexto: {len(context)} caracteres")
            
            if chain:
                # Gerar resposta com LLM
                try:
                    response = chain.run(contexto=context, pergunta=question)
                    return response
                except Exception as e:
                    print(f"❌ Erro na geração de resposta: {e}")
                    return f"CONTEXTO ENCONTRADO:\n\n{context}"
            else:
                # Retornar contexto bruto
                return f"CONTEXTO ENCONTRADO:\n\n{context}"
                
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return "Erro na busca semântica"
    
    # 7. Interface interativa
    if question:
        return search_and_answer(question)
    else:
        return search_and_answer