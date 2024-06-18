import os
import json

# Função para limpar a tela do console
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para baixar posts específicos
def baixar_posts():
    limpar_tela()
    print("Executando script para baixar alguns posts...")
    os.system('python code/post.py')
    input("\nPressione Enter para voltar ao menu...")

# Função para personalizar as configurações de download
def personalizar_configuracoes():
    limpar_tela()
    print("Executando script para personalizar as configurações de download...")
    os.system('python settings.py')
    input("\nPressione Enter para voltar ao menu...")

# Verificar e instalar as dependências necessárias
def verificar_instalar_dependencias():
    try:
        import requests
        from bs4 import BeautifulSoup
        from fake_useragent import UserAgent
    except ImportError:
        print("Bibliotecas necessárias não encontradas.")
        choice = input("Deseja instalar as bibliotecas necessárias? (s/n): ").strip().lower()
        if choice == 's':
            os.system('pip install -r requirements.txt')
        else:
            print("Instalação cancelada. O programa pode não funcionar corretamente.")
            input("\nPressione Enter para continuar...")

# Menu principal
def menu():
    verificar_instalar_dependencias()

    while True:
        limpar_tela()
        print("""
        
 ____  _      _         ____  _     
|  _ \(_)_  _(_)_   __ |  _ \| |    
| |_) | \ \/ / \ \ / / | | | | |    
|  __/| |>  <| |\ V /  | |_| | |___ 
|_|   |_/_/\_\_| \_/   |____/|_____|

 Criado por E43b
 GitHub: https://github.com/e43b
 Discord: https://discord.gg/Q6nQ3vsWTF
 Repositório do Projeto: https://github.com/e43b/Pixiv-DL

 Com este projeto é possível baixar posts do Pixiv:

 Escolha uma opção:
 1 - Baixar alguns posts
 2 - Personalizar as configurações do programa
 3 - Sair do programa
 """)

        opcao = input("Digite sua escolha (1/2/3): ")

        if opcao == '1':
            baixar_posts()
        elif opcao == '2':
            personalizar_configuracoes()
        elif opcao == '3':
            break
        else:
            print("Opção inválida! Digite 1, 2 ou 3.")
            input("Pressione Enter para continuar...")

# Executar o programa
if __name__ == "__main__":
    menu()
