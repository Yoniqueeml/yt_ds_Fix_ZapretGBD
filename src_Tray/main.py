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

global CMD_FILES
global PARSED_COMMANDS

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_architecture():
    """Get sys arch"""
    arch = platform.architecture()[0]
    return 'x86_64' if arch == '64bit' else 'x86'


def build_command(cmd_file):
    """Creating a command line"""
    if cmd_file.startswith('zapret'):
        for i, v in enumerate(CMD_FILES):
            if v == cmd_file:
                command_temp = PARSED_COMMANDS[i]
                break
        return command_temp
    architecture = get_architecture()
    exe_path = f'{architecture}\\goodbyedpi.exe'

    command_temp = ''
    for i, v in enumerate(CMD_FILES):
        if v == cmd_file:
            command_temp = PARSED_COMMANDS[i]
            break
    command = exe_path + ' ' + command_temp
    command = f''.join(command)
    return command


def start_process(file_name):
    global process
    command = build_command(file_name)
    print(f'Executing command: {command}')
    logging.info(f'Executing command: {command}')

    if process:
        process.terminate()
        process.wait()

    try:
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
    menu_items = CMD_FILES + ['Exit']

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

    menu_items = cmd_files + ['Exit']

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
    start_pattern = re.compile(r'start\s+""\s+goodbyedpi\.exe\s+(.*)')

    files = []
    commands = []

    for filename in os.listdir(directory):
        if filename.endswith('.cmd'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if start_pattern.search(line):
                        files.append(filename)
                        commands.append(line.strip())

    commands = clean_blacklist_paths(commands)
    files.append('zapret_preset_my.cmd')
    command = [
        "winws.exe",
        "--wf-tcp=80,443",
        "--wf-udp=443,50000-65535",
        "--filter-udp=443",
        "--hostlist={}".format(os.path.join(os.path.dirname(__file__), "list-youtube.txt")),
        "--dpi-desync=fake,tamper",
        "--dpi-desync-repeats=11",
        "--dpi-desync-fake-quic={}".format(os.path.join(os.path.dirname(__file__), "quic_initial_www_google_com.bin")),
        "--new",
        "--filter-udp=443",
        "--dpi-desync=fake,tamper",
        "--dpi-desync-autottl=2",
        "--dpi-desync-repeats=11",
        "--new",
        "--filter-udp=50000-65535",
        "--dpi-desync=fake,tamper",
        "--dpi-desync-any-protocol",
        "--dpi-desync-autottl=2",
        "--dpi-desync-repeats=11",
        "--new",
        "--filter-tcp=80",
        "--dpi-desync=fake,disorder2",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=badseq",
        "--new",
        "--filter-tcp=443",
        "--hostlist={}".format(os.path.join(os.path.dirname(__file__), "list-youtube.txt")),
        "--dpi-desync=fake,disorder2",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=badseq",
        "--dpi-desync-fake-tls={}".format(
            os.path.join(os.path.dirname(__file__), "tls_clienthello_www_google_com.bin")),
        "--new",
        "--dpi-desync=fake,tamper",
        "--dpi-desync-any-protocol",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=badseq",
        "--dpi-desync-fake-tls={}".format(
            os.path.join(os.path.dirname(__file__), "tls_clienthello_www_google_com.bin")),
    ]
    commands.append(command)

    files.append('zapret_preset_russia.cmd')
    command = [
        os.path.join(os.path.dirname(__file__), "winws.exe"),
        "--wf-tcp=80,443",
        "--wf-udp=443",
        "--filter-udp=443",
        "--hostlist={}".format(os.path.join(os.path.dirname(__file__), "list-youtube.txt")),
        "--dpi-desync=fake",
        "--dpi-desync-repeats=11",
        "--dpi-desync-fake-quic={}".format(os.path.join(os.path.dirname(__file__), "quic_initial_www_google_com.bin")),
        "--new",
        "--filter-udp=443",
        "--dpi-desync=fake",
        "--dpi-desync-repeats=11",
        "--new",
        "--filter-tcp=80",
        "--dpi-desync=fake,split2",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=md5sig",
        "--new",
        "--filter-tcp=443",
        "--hostlist={}".format(os.path.join(os.path.dirname(__file__), "list-youtube.txt")),
        "--dpi-desync=fake,split2",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=md5sig",
        "--dpi-desync-fake-tls={}".format(
            os.path.join(os.path.dirname(__file__), "tls_clienthello_www_google_com.bin")),
        "--new",
        "--dpi-desync=fake,disorder2",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=md5sig",
    ]
    commands.append(command)
    return files, commands


if __name__ == "__main__":
    directory_path = os.getcwd()
    CMD_FILES, PARSED_COMMANDS = parse_cmd_files(directory_path)

    if check_if_running():
        print("Another instance of goodbyedpi.exe is already running.")
        logging.error("Another instance of goodbyedpi.exe is already running.")
        sys.exit(1)

    print("Starting the application...")
    logging.info('Application started.')

    icon = create_icon(CMD_FILES)
    icon.run()

    print("Application has stopped.")
    logging.info('Application has stopped.')

    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)
