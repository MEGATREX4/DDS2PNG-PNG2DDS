from flask import Flask, render_template, request
from PIL import Image
import os
from datetime import datetime
import shutil
from colorama import init, Fore
import threading
import time

init(autoreset=True)

app = Flask(__name__)

UPLOAD_FOLDER = 'input'
ALLOWED_EXTENSIONS = {'png', 'dds'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = 'converted'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_output_format(filename):
    # Determine the output format based on the file extension
    _, ext = os.path.splitext(filename)
    return 'DDS' if ext.lower() == '.png' else 'PNG'

def convert_image(input_path, output_path, output_format):
    try:
        img = Image.open(input_path)
        img.save(output_path, format=output_format)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error converting image: {e}{Fore.RESET}")
        return False

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"{Fore.GREEN}Created folder: {folder_path}{Fore.RESET}")

def watch_folder():
    while True:
        convert_files_in_input_folder()
        time.sleep(1)

def convert_files_in_input_folder():
    input_folder = app.config['UPLOAD_FOLDER']
    output_folder = app.config['CONVERTED_FOLDER']

    create_folder_if_not_exists(input_folder)
    create_folder_if_not_exists(output_folder)

    print(f"{Fore.CYAN}=== Conversion Started ==={Fore.RESET}")

    for root, _, files in os.walk(input_folder):
        for filename in files:
            input_path = os.path.join(root, filename)

            relative_path = os.path.relpath(input_path, input_folder)
            output_folder_path = os.path.join(output_folder, datetime.now().strftime('%d.%m.%Y'), os.path.dirname(relative_path))
            output_path = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.{get_output_format(filename).lower()}")

            create_folder_if_not_exists(output_folder_path)

            print(f"{Fore.BLUE}Processing {filename}...{Fore.RESET}")

            if allowed_file(filename):
                if convert_image(input_path, output_path, get_output_format(filename)):
                    print(f"{Fore.GREEN}Converted {filename}: {input_path} -> {output_path}{Fore.RESET}")
                    os.remove(input_path)
                    print(f"{Fore.YELLOW}Removed {filename} from {input_folder}{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Failed to convert {filename}{Fore.RESET}")
            else:
                # If the file doesn't match the format, copy it to the output folder
                shutil.copy2(input_path, output_folder_path)
                print(f"{Fore.BLUE}Copied {filename} to {output_folder_path}{Fore.RESET}")

    print(f"{Fore.CYAN}=== Conversion Completed ==={Fore.RESET}")

    # Clean up empty input folders
    for root, dirs, _ in os.walk(input_folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"{Fore.YELLOW}Removed empty folder: {dir_path}{Fore.RESET}")

if __name__ == '__main__':
    app_thread = threading.Thread(target=app.run, kwargs={'debug': True})
    watcher_thread = threading.Thread(target=watch_folder)

    app_thread.start()
    watcher_thread.start()

    app_thread.join()
    watcher_thread.join()
