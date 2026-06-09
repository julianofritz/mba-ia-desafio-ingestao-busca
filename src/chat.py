from search import search_prompt

def main():
    """Interface interativa de chat RAG"""
    
    print("🤖 Iniciando sistema de chat RAG...")
    print("=" * 50)
    
    # Inicializar sistema de busca
    search_function = search_prompt()
    
    if not search_function:
        print("❌ Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("✅ Sistema RAG pronto!")
    print("💡 Digite 'sair' para encerrar")
    print("💡 Exemplos: 'faturamento', 'clientes', 'relatório'")
    print("=" * 50)
    
    # Loop interativo
    while True:
        try:
            # Capturar pergunta do usuário
            question = input("\n🔍 Sua pergunta: ").strip()
            
            # Verificar se quer sair
            if question.lower() in ['sair', 'exit', 'quit']:
                print("👋 Encerrando chat...")
                break
            
            # Verificar se está vazia
            if not question:
                print("❌ Por favor, digite uma pergunta.")
                continue
            
            print("\n🔄 Processando...")
            
            # Buscar e responder
            response = search_function(question)
            
            print("\n" + "=" * 50)
            print("📝 RESPOSTA:")
            print("=" * 50)
            print(response)
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Chat interrompido. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro no chat: {e}")
            print("💡 Tente novamente ou digite 'sair' para encerrar")

if __name__ == "__main__":
    main()