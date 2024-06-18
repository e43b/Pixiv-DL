import os
import json
from time import sleep

# Function to load settings from a JSON file
def load_settings(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {}
    return settings

# Function to save settings to a JSON file
def save_settings(settings, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(settings, file, indent=4)

# Function to display the main menu and get user choice
def display_main_menu():
    clear_console()
    print("Configure the System\n")
    print("Type 1 to configure the post download variables")
    print("Type 2 to return to the main menu and run main.py")
    print("Type 3 to exit the program")

    choice = input("\nEnter your choice: ")
    return choice

# Function to clear the console screen in a cross-platform way
def clear_console():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

# Function to configure the post download system (option 1)
def configure_download_system():
    settings = load_settings('codeen/code/config.json')

    while True:
        clear_console()
        print("Configure Post Download System:\n")
        print("1. Save Information to TXT:", "Yes" if settings.get('save_txt', False) else "No")
        print("2. Image Quality:", settings.get('image_quality', 'both'))
        print("3. Cooldown Between Images:", settings.get('cooldown_between_images', 1), "seconds")
        print("4. Cooldown Between Posts:", settings.get('cooldown_between_posts', 4), "seconds")
        print("5. Back")

        option = input("\nEnter the option number you want to configure: ")

        if option == '1':
            settings['save_txt'] = not settings.get('save_txt', False)
        elif option == '2':
            new_quality = input("Enter the new image quality ('original', 'regular', 'both'): ")
            if new_quality in ['original', 'regular', 'both']:
                settings['image_quality'] = new_quality
            else:
                print("Invalid option. Please try again.")
                sleep(2)
                continue
        elif option == '3':
            new_cooldown_images = input("Enter the new cooldown between images (in seconds): ")
            try:
                settings['cooldown_between_images'] = int(new_cooldown_images)
            except ValueError:
                print("Invalid value. It must be an integer.")
                sleep(2)
                continue
        elif option == '4':
            new_cooldown_posts = input("Enter the new cooldown between posts (in seconds): ")
            try:
                settings['cooldown_between_posts'] = int(new_cooldown_posts)
            except ValueError:
                print("Invalid value. It must be an integer.")
                sleep(2)
                continue
        elif option == '5':
            break
        else:
            print("Invalid option. Please choose a valid option.")
            sleep(2)
            continue

        save_settings(settings, 'codeen/code/config.json')

# Main function controlling the program flow
def main():
    while True:
        choice = display_main_menu()

        if choice == '1':
            configure_download_system()
        elif choice == '2':
            print("\nReturning to the main menu...")
            os.system('python main.py')
        elif choice == '3':
            print("\nExiting the program...")
            break
        else:
            print("\nInvalid option. Please choose a valid option.")
            sleep(2)

if __name__ == "__main__":
    main()
