import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()


def ingest_pdf():
    pdf_path = os.getenv("PDF_PATH")
    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY não encontrada no .env")

    print("🔄 Carregando PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"✅ PDF carregado: {len(documents)} páginas")

    # 3. Chunking
    print("✂️ Dividindo em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Documento dividido em {len(chunks)} chunks")

    # 4. Embeddings e armazenamento com fallback completo
    print("💾 Armazenando no banco vetorial...")
    
    # Tentar Gemini com múltiplos modelos
    gemini_models = ["text-embedding-004", "embedding-001", "models/embedding-001"]
    
    for model in gemini_models:
        try:
            print(f"🧠 Tentando Gemini modelo: {model}")
            embeddings = GoogleGenerativeAIEmbeddings(
                model=model,
                task_type="retrieval_document"  # Otimizado para busca
            )
            vector_store = PGVector(
                connection=connection_string,
                embeddings=embeddings,
                collection_name="document_chunks",
                pre_delete_collection=True
            )
            vector_store.add_documents(chunks)
            print(f"✅ {len(chunks)} chunks armazenados com Gemini modelo {model}!")
            return  # Sucesso!
            
        except Exception as e:
            print(f"❌ Gemini modelo {model} falhou: {e}")
            continue  # Tenta próximo modelo
    
    print("❌ Todos os modelos Gemini falharam")
    print("🔄 Tentando OpenAI embeddings...")
    
    # Tentar OpenAI
    try:
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sk-sua-openai-key-aqui":
            raise ValueError("OPENAI_API_KEY inválida")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = PGVector(
            connection=connection_string,
            embeddings=embeddings,
            collection_name="document_chunks",
            pre_delete_collection=True
        )
        vector_store.add_documents(chunks)
        print(f"✅ {len(chunks)} chunks armazenados com OpenAI embeddings!")
        return  # Sucesso!
        
    except Exception as e2:
        print(f"❌ OpenAI também falhou: {e2}")
        print("🧪 Modo estudo: sem embeddings (apenas texto)")
        
        # Mock embeddings para estudo
        class MockEmbeddings:
            def embed_documents(self, texts):
                return [[0.1] * 1536 for _ in texts]  # Vetores fake
            def embed_query(self, text):
                return [0.1] * 1536
        
        embeddings = MockEmbeddings()
        vector_store = PGVector(
            connection=connection_string,
            embeddings=embeddings,
            collection_name="document_chunks",
            pre_delete_collection=True
        )
        vector_store.add_documents(chunks)
        print(f"✅ {len(chunks)} chunks armazenados com embeddings mock (apenas para estudo)!")

    # 7. Verificação
    print("🔍 Testando busca...")
    results = vector_store.similarity_search("faturamento", k=2)
    print(f"✅ Teste de busca: {len(results)} resultados encontrados")

if __name__ == "__main__":
    ingest_pdf()