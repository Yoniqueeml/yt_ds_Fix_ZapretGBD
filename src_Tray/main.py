import re
import subprocess
import pystray
from PIL import Image
import platform
import os
import logging
import sys
import psutil

process = None
ICONS_DIR = "icons"

ICON_OFF_PATH = os.path.join(ICONS_DIR, "icon-off.jpg")
ICON_ON_PATH = os.path.join(ICONS_DIR, "icon-on.png")

LOG_FILE_PATH = "app.log"
LOCK_FILE_PATH = "app.lock"

global PARSED_COMMANDS

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_architecture():
    """Get sys arch"""
    arch = platform.architecture()[0]
    return 'x86_64' if arch == '64bit' else 'x86'


def build_command(parsed_command):
    """Creating a command line"""
    exe_path = parsed_command[0]
    parsed_command = parsed_command[1:]
    command = [exe_path] + parsed_command
    command = f' '.join(command)
    return command


def start_process(file_name):
    global process

    for command in PARSED_COMMANDS:
        print(f'Executing command: {command}')
        logging.info(f'Executing command: {command}')

    if process:
        process.terminate()
        process.wait()

    try:
        for command in PARSED_COMMANDS:
            process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
            print(f'Executed: {command}')
            logging.info(f'Executed: {command}')
    except Exception as e:
        print(f'Failed to start process: {e}')
        logging.error(f'Failed to start process: {e}')

    icon.icon = Image.open(ICON_ON_PATH)
    update_menu_for_running()


def stop_process(icon):
    global process
    if process:
        process.terminate()
        process.wait()
        print('The process has been successfully completed.')
        logging.info('The process has been successfully completed.')

    icon.icon = Image.open(ICON_OFF_PATH)
    update_menu_for_stopped()


def update_menu_for_running():
    global icon
    menu = pystray.Menu(
        pystray.MenuItem('Stop', stop_process),
        pystray.MenuItem('Exit', exit_program)
    )
    icon.menu = menu
    icon.update_menu()


def update_menu_for_stopped():
    global icon
    menu_items = ['Start'] + ['Exit']

    def create_menu_item(name):
        return pystray.MenuItem(name, lambda icon, item: start_process(name))

    menu = pystray.Menu(*(create_menu_item(name) for name in menu_items))
    icon.menu = menu
    icon.update_menu()


def exit_program(icon):
    if process:
        process.terminate()
        process.wait()
        print('Process terminated on exit.')
        logging.info('Process terminated on exit.')

    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)

    icon.stop()


def create_icon(cmd_files):
    icon_image = Image.open(ICON_OFF_PATH)

    menu_items = ['Start'] + ['Exit']

    def create_menu_item(name):
        return pystray.MenuItem(name, lambda icon, item: start_process(name))

    menu = pystray.Menu(*(create_menu_item(name) for name in menu_items))

    icon = pystray.Icon("goodbyedpi", icon_image, "GoodByeDPI", menu=menu)
    return icon


def check_if_running():
    """Check if goodbyedpi.exe is currently running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'goodbyedpi.exe':
            return True
    return False


def clean_blacklist_paths(lines):
    cleaned_lines = []
    for line in lines:
        cleaned_line = line.replace('--blacklist ..\\', '--blacklist ')
        cleaned_lines.append(cleaned_line)
    return cleaned_lines


def parse_cmd_files(directory):
    """Parse .cmd files to get their names and commands."""
    commands = []
    comm = []
    for filename in os.listdir(directory):
        if filename == 'confs.txt':
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    temp = line.strip()
                    if temp == '--hostlist=':
                        temp = temp + rf'{os.getcwd()}\\hostlists.txt'
                    elif temp == '--dpi-desync-fake-quic=':
                        temp = temp + rf'{os.getcwd()}\\quic_initial_www_google_com.bin'
                    elif temp == '--dpi-desync-fake-tls=':
                        temp = temp +rf'{os.getcwd()}\\tls_clienthello_www_google_com.bin'
                    comm.append(temp.strip())
    commands.append(build_command(comm))
    return commands


if __name__ == "__main__":
    directory_path = os.getcwd()
    PARSED_COMMANDS = parse_cmd_files(directory_path)

    if check_if_running():
        print("Another instance of goodbyedpi.exe is already running.")
        logging.error("Another instance of goodbyedpi.exe is already running.")
        sys.exit(1)

    print("Starting the application...")
    logging.info('Application started.')

    icon = create_icon([''])
    icon.run()

    print("Application has stopped.")
    logging.info('Application has stopped.')

    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)
