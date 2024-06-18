import os
import json
from time import sleep

# Função para carregar as configurações de um arquivo JSON
def carregar_configuracoes(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            configuracoes = json.load(arquivo)
    except FileNotFoundError:
        configuracoes = {}
    return configuracoes

# Função para salvar as configurações em um arquivo JSON
def salvar_configuracoes(configuracoes, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(configuracoes, arquivo, indent=4)

# Função para exibir o menu principal e obter a escolha do usuário
def exibir_menu_principal():
    limpar_console()
    print("Configurar o Sistema\n")
    print("Digite 1 para configurar as variáveis de download de posts")
    print("Digite 2 para voltar para o menu principal e executar main.py")
    print("Digite 3 para sair do programa")

    escolha = input("\nDigite sua escolha: ")
    return escolha

# Função para limpar a tela do console de forma multiplataforma
def limpar_console():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

# Função para configurar o sistema de baixar posts (opção 1)
def configurar_sistema_download():
    configuracoes = carregar_configuracoes('code/config.json')

    while True:
        limpar_console()
        print("Configuração do Sistema de Baixar Posts:\n")
        print("1. Salvar Informações em TXT:", "Sim" if configuracoes.get('salvar_txt', False) else "Não")
        print("2. Qualidade da Imagem:", configuracoes.get('qualidade_imagem', 'ambas'))
        print("3. Cooldown entre Imagens:", configuracoes.get('cooldown_entre_imagens', 1), "segundos")
        print("4. Cooldown entre Posts:", configuracoes.get('cooldown_entre_posts', 4), "segundos")
        print("5. Voltar")

        opcao = input("\nDigite o número da opção que deseja configurar: ")

        if opcao == '1':
            configuracoes['salvar_txt'] = not configuracoes.get('salvar_txt', False)
        elif opcao == '2':
            nova_qualidade = input("Digite a nova qualidade da imagem ('original', 'regular', 'ambas'): ")
            if nova_qualidade in ['original', 'regular', 'ambas']:
                configuracoes['qualidade_imagem'] = nova_qualidade
            else:
                print("Opção inválida. Tente novamente.")
                sleep(2)
                continue
        elif opcao == '3':
            novo_cooldown_imagens = input("Digite o novo cooldown entre imagens (em segundos): ")
            try:
                configuracoes['cooldown_entre_imagens'] = int(novo_cooldown_imagens)
            except ValueError:
                print("Valor inválido. Deve ser um número inteiro.")
                sleep(2)
                continue
        elif opcao == '4':
            novo_cooldown_posts = input("Digite o novo cooldown entre posts (em segundos): ")
            try:
                configuracoes['cooldown_entre_posts'] = int(novo_cooldown_posts)
            except ValueError:
                print("Valor inválido. Deve ser um número inteiro.")
                sleep(2)
                continue
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            sleep(2)
            continue

        salvar_configuracoes(configuracoes, 'config.json')

# Função principal que controla o fluxo do programa
def main():
    while True:
        escolha = exibir_menu_principal()

        if escolha == '1':
            configurar_sistema_download()
        elif escolha == '2':
            print("\nVoltando para o menu principal...")
            os.system('python main.py')
        elif escolha == '3':
            print("\nSaindo do programa...")
            break
        else:
            print("\nOpção inválida. Por favor, escolha uma opção válida.")
            sleep(2)

if __name__ == "__main__":
    main()
