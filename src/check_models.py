import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def check_gemini_models():
    """Verifica quais modelos de embedding funcionam com LangChain"""
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY não encontrada no .env")
        return
    
    print("🔍 Testando modelos de embedding do Gemini...")
    print(f"📝 API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Lista de modelos conhecidos para testar
    test_models = [
        "text-embedding-004",
        "embedding-001", 
        "models/embedding-001",
        "models/text-embedding-004"
    ]
    
    working_models = []
    
    for model_name in test_models:
        try:
            print(f"🧪 Testando modelo: {model_name}")
            
            # Criar embeddings
            embeddings = GoogleGenerativeAIEmbeddings(
                model=model_name,
                task_type="retrieval_document"
            )
            
            # Testar embedding
            result = embeddings.embed_query("Teste de embedding")
            
            print(f"   ✅ SUCESSO!")
            print(f"   📊 Dimensões: {len(result)}")
            print(f"   🔢 Exemplo: {result[:5]}...")
            working_models.append((model_name, len(result)))
            
        except Exception as e:
            print(f"   ❌ FALHOU: {e}")
        
        print()
    
    # Resumo
    print("🎯 RESUMO:")
    print("=" * 30)
    
    if working_models:
        print(f"✅ {len(working_models)} modelos funcionaram:")
        for model_name, dimensions in working_models:
            print(f"   🤖 {model_name} - {dimensions} dimensões")
        
        print()
        print("💡 Use o primeiro modelo funcionando no ingest.py:")
        print(f"   model=\"{working_models[0][0]}\"")
        
    else:
        print("❌ Nenhum modelo funcionou!")
        print("💡 Sugestões:")
        print("   - Verifique se a API Key está correta")
        print("   - Use o modo estudo (fallback)")
        print("   - Considere usar OpenAI embeddings")

if __name__ == "__main__":
    check_gemini_models()
