import os
import json

# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to download specific posts
def download_posts():
    clear_screen()
    print("Executing script to download some posts...")
    os.system('python code/post.py')
    input("\nPress Enter to return to the menu...")

# Function to customize download settings
def customize_settings():
    clear_screen()
    print("Executing script to customize download settings...")
    os.system('python settings.py')
    input("\nPress Enter to return to the menu...")

# Check and install necessary dependencies
def check_install_dependencies():
    try:
        import requests
        from bs4 import BeautifulSoup
        from fake_useragent import UserAgent
    except ImportError:
        print("Installing required libraries...")
        os.system('pip install -r requirements.txt')

# Main menu function
def menu():
    check_install_dependencies()

    while True:
        clear_screen()
        print("""

 ____  _      _         ____  _     
|  _ \(_)_  _(_)_   __ |  _ \| |    
| |_) | \ \/ / \ \ / / | | | | |    
|  __/| |>  <| |\ V /  | |_| | |___ 
|_|   |_/_/\_\_| \_/   |____/|_____|

 Created by E43b
 GitHub: https://github.com/e43b
 Discord: https://discord.gg/Q6nQ3vsWTF
 Project Repository: https://github.com/e43b/Pixiv-DL

 With this project, you can download posts from Pixiv:

 Choose an option:
 1 - Download some posts
 2 - Customize program settings
 3 - Exit the program
 """)

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            download_posts()
        elif choice == '2':
            customize_settings()
        elif choice == '3':
            break
        else:
            print("Invalid option! Enter 1, 2, or 3.")
            input("Press Enter to continue...")

# Execute the program
if __name__ == "__main__":
    menu()
