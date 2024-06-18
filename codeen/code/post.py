import os
import requests
from datetime import datetime
from fake_useragent import UserAgent
from time import sleep
import json

# Function to convert date and time
def convert_datetime(datetime_str):
    dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Function to get data from the API
def get_data(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for request errors
    return response.json()

# Function to download an image
def download_image(url, path, headers):
    # Simulate more human-like behavior
    headers = {
        'User-Agent': ua.random,
        'Referer': 'https://www.pixiv.net/',
    }

    # Handle redirects
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Check for request errors
        with open(path, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.HTTPError as e:
        print(f"Error downloading image: {e}")

# User agent configuration
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'Referer': 'https://www.pixiv.net/',
}

# Load configuration from JSON file
def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# Function to process and download Pixiv posts
def process_pixiv_posts(post_urls, config):
    for url in post_urls:
        illust_id = url.split('/')[-1]

        # API URLs
        info_url = f"https://www.pixiv.net/ajax/illust/{illust_id}"
        pages_url = f"https://www.pixiv.net/ajax/illust/{illust_id}/pages"

        try:
            # Get illustration information
            info_data = get_data(info_url, headers)
            info_body = info_data['body']
            tags_data = info_body['tags']

            # Create directories
            author_name = info_body['userName']
            author_account = info_body['userAccount']
            post_id = info_body['illustId']
            base_dir = os.path.join('pixiv', author_account, post_id)
            os.makedirs(base_dir, exist_ok=True)

            # Save information to a text file
            if config['save_txt']:
                info_txt_path = os.path.join(base_dir, 'info.txt')
                with open(info_txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"ID: {info_body['illustId']}\n")
                    f.write(f"Title: {info_body['illustTitle']}\n")
                    f.write(f"Description: {info_body['illustComment']}\n")
                    f.write(f"Upload Date: {convert_datetime(info_body['uploadDate'])}\n\n")
                    f.write("Tags:\n")
                    for tag in tags_data['tags']:
                        translation = tag['translation']['en'] if 'translation' in tag else tag['tag']
                        f.write(f"- {translation} (JP: {tag['tag']})\n")
                    f.write(f"\nAuthor ID: {tags_data['authorId']}\n")
                    f.write(f"Author Name: {info_body['userName']}\n")
                    f.write(f"Author Account: {info_body['userAccount']}\n")

            # Get image links
            pages_data = get_data(pages_url, headers)['body']

            # Download and save images
            for index, page in enumerate(pages_data):
                urls = page['urls']
                if config['image_quality'] == 'both' or config['image_quality'] == 'original':
                    image_url = urls['original']
                    image_extension = image_url.split('.')[-1]
                    image_path = os.path.join(base_dir, f'image_{index + 1}_original.{image_extension}')
                    download_image(image_url, image_path, headers)
                    if config['save_txt']:
                        with open(info_txt_path, 'a', encoding='utf-8') as f:
                            f.write(f"\nImage {index + 1} (Original):\n")
                            f.write(f"  Original: {urls['original']}\n")
                if config['image_quality'] == 'both' or config['image_quality'] == 'regular':
                    image_url = urls['regular']
                    image_extension = image_url.split('.')[-1]
                    image_path = os.path.join(base_dir, f'image_{index + 1}_regular.{image_extension}')
                    download_image(image_url, image_path, headers)
                    if config['save_txt']:
                        with open(info_txt_path, 'a', encoding='utf-8') as f:
                            f.write(f"\nImage {index + 1} (Regular):\n")
                            f.write(f"  Regular: {urls['regular']}\n")

                # Cooldown between each image download
                sleep(config['cooldown_between_images'])

            print(f"Information and images saved in: {base_dir}")

            # Cooldown between each post
            sleep(config['cooldown_between_posts'])

        except Exception as e:
            print(f"Error processing post {url}: {e}")

# Main function for user interaction
def main():
    config = load_config('codeen/code/config.json')

    while True:
        pixiv_urls = input("Enter Pixiv link(s) (separated by comma if multiple): ").strip().split(',')
        pixiv_urls = [url.strip() for url in pixiv_urls]

        process_pixiv_posts(pixiv_urls, config)

        choice = input("Do you want to download another Pixiv post? (y/n): ").strip().lower()
        if choice != 'y':
            break

if __name__ == "__main__":
    main()
