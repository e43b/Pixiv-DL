import os
import requests
from datetime import datetime
from fake_useragent import UserAgent
from time import sleep
import json

# Função para converter data e hora
def convert_datetime(datetime_str):
    dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Função para obter dados da API
def get_data(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Verifica se houve erro na requisição
    return response.json()

# Função para baixar uma imagem
def download_image(url, path, headers):
    # Simular um comportamento mais humano
    headers = {
        'User-Agent': ua.random,
        'Referer': 'https://www.pixiv.net/',
    }

    # Lidar com redirecionamentos
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Verifica se houve erro na requisição
        with open(path, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.HTTPError as e:
        print(f"Erro ao baixar a imagem: {e}")

# Configuração do user agent
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'Referer': 'https://www.pixiv.net/',
}

# Carregar configurações do arquivo JSON
def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# Função para processar e baixar posts do Pixiv
def process_pixiv_posts(post_urls, config):
    for url in post_urls:
        illust_id = url.split('/')[-1]

        # URLs da API
        info_url = f"https://www.pixiv.net/ajax/illust/{illust_id}"
        pages_url = f"https://www.pixiv.net/ajax/illust/{illust_id}/pages"

        try:
            # Obter informações da ilustração
            info_data = get_data(info_url, headers)
            info_body = info_data['body']
            tags_data = info_body['tags']

            # Criar diretórios
            author_name = info_body['userName']
            author_account = info_body['userAccount']
            post_id = info_body['illustId']
            base_dir = os.path.join('pixiv', author_account, post_id)
            os.makedirs(base_dir, exist_ok=True)

            # Salvar informações em um arquivo de texto
            if config['salvar_txt']:
                info_txt_path = os.path.join(base_dir, 'info.txt')
                with open(info_txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"ID: {info_body['illustId']}\n")
                    f.write(f"Título: {info_body['illustTitle']}\n")
                    f.write(f"Descrição: {info_body['illustComment']}\n")
                    f.write(f"Data de Upload: {convert_datetime(info_body['uploadDate'])}\n\n")
                    f.write("Tags:\n")
                    for tag in tags_data['tags']:
                        translation = tag['translation']['en'] if 'translation' in tag else tag['tag']
                        f.write(f"- {translation} (JP: {tag['tag']})\n")
                    f.write(f"\nID do Autor: {tags_data['authorId']}\n")
                    f.write(f"Nome do Autor: {info_body['userName']}\n")
                    f.write(f"Conta do Autor: {info_body['userAccount']}\n")

            # Obter links das imagens
            pages_data = get_data(pages_url, headers)['body']

            # Baixar e salvar imagens
            for index, page in enumerate(pages_data):
                urls = page['urls']
                if config['qualidade_imagem'] == 'ambas' or config['qualidade_imagem'] == 'original':
                    image_url = urls['original']
                    image_extension = image_url.split('.')[-1]
                    image_path = os.path.join(base_dir, f'image_{index + 1}_original.{image_extension}')
                    download_image(image_url, image_path, headers)
                    if config['salvar_txt']:
                        with open(info_txt_path, 'a', encoding='utf-8') as f:
                            f.write(f"\nImagem {index + 1} (Original):\n")
                            f.write(f"  Original: {urls['original']}\n")
                if config['qualidade_imagem'] == 'ambas' or config['qualidade_imagem'] == 'regular':
                    image_url = urls['regular']
                    image_extension = image_url.split('.')[-1]
                    image_path = os.path.join(base_dir, f'image_{index + 1}_regular.{image_extension}')
                    download_image(image_url, image_path, headers)
                    if config['salvar_txt']:
                        with open(info_txt_path, 'a', encoding='utf-8') as f:
                            f.write(f"\nImagem {index + 1} (Regular):\n")
                            f.write(f"  Regular: {urls['regular']}\n")

                # Cooldown entre cada download de imagem
                sleep(config['cooldown_entre_imagens'])

            print(f"Informações e imagens salvas em: {base_dir}")

            # Cooldown entre cada post
            sleep(config['cooldown_entre_posts'])

        except Exception as e:
            print(f"Erro ao processar o post {url}: {e}")

# Função principal para interação com o usuário
def main():
    config = load_config('config.json')

    while True:
        pixiv_urls = input("Insira o(s) link(s) do Pixiv (separados por vírgula se mais de um): ").strip().split(',')
        pixiv_urls = [url.strip() for url in pixiv_urls]

        process_pixiv_posts(pixiv_urls, config)

        choice = input("Deseja baixar outro post do Pixiv? (s/n): ").strip().lower()
        if choice != 's':
            break

if __name__ == "__main__":
    main()
