import os
import shlex
import subprocess
import logging
import sys
import pystray
from PIL import Image
import psutil

ICONS_DIR = "icons"
ICON_OFF_PATH = os.path.join(ICONS_DIR, "icon-off.jpg")
ICON_ON_PATH = os.path.join(ICONS_DIR, "icon-on.png")
LOG_FILE_PATH = "app.log"
LOCK_FILE_PATH = "app.lock"

process = None
icon = None
PARSED_COMMAND = []

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def join_bat_command_lines(lines):
    commands = []
    current_line = ""
    for line in lines:
        if not line or line.lower().startswith('rem'):
            continue
        if line.endswith('^'):
            current_line += line[:-1].rstrip() + " "
        else:
            current_line += line
            commands.append(current_line.strip())
            current_line = ""
    if current_line:
        commands.append(current_line.strip())
    return commands


def find_winws_command(lines):
    commands = join_bat_command_lines(lines)

    full_args = []

    def replace_vars(s):
        s = s.replace('%BIN%', os.path.join(os.getcwd(), "bin") + "\\")
        s = s.replace('%LISTS%', os.path.join(os.getcwd(), "lists") + "\\")
        game_filter_path = os.path.join(os.getcwd(), "bin", "game_filter.enabled")
        GameFilter = "1024-65535" if os.path.exists(game_filter_path) else "0"
        s = s.replace('%GameFilter%', GameFilter)
        return s

    capture = False

    for line in commands:
        line = replace_vars(line)

        if 'winws.exe' in line.lower():
            capture = True

        if capture:
            try:
                parts = shlex.split(line, posix=False)
            except Exception as e:
                logging.error(f"Ошибка разбора строки: {line}: {e}")
                continue

            if not full_args:
                for i, part in enumerate(parts):
                    if 'winws.exe' in part.lower():
                        if part.startswith('"') and part.endswith('"'):
                            part = part[1:-1]
                        full_args.append(part)
                        full_args.extend(parts[i + 1:])
                        break
            else:
                for p in parts:
                    if p not in full_args:
                        full_args.append(p)

    if not full_args:
        return None

    cleaned_args = []
    for arg in full_args:
        if '=' in arg:
            key, val = arg.split('=', 1)
            val = val.strip('"')
            cleaned_args.append(f"{key}={val}")
        else:
            cleaned_args.append(arg.strip('"'))

    return cleaned_args


def read_bat_file(bat_path):
    with open(bat_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\r\n') for line in f if line.strip() and not line.strip().lower().startswith('rem')]
    return lines


def check_if_running():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in ('goodbyedpi.exe', 'winws.exe'):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def start_process(icon=None, item=None):
    global process, PARSED_COMMAND
    if process:
        stop_process(icon)
    print("Запускаем команду:", PARSED_COMMAND)
    try:
        logging.info(f"Запускаю процесс: {PARSED_COMMAND}")
        with open("winws_stdout.log", "w", encoding='utf-8') as out, open("winws_stderr.log", "w", encoding='utf-8') as err:
            process = subprocess.Popen(
                PARSED_COMMAND,
                stdout=out,
                stderr=err,
                creationflags=subprocess.CREATE_NO_WINDOW,
                shell=False
            )
        logging.info("Процесс запущен")
        if icon:
            icon.icon = Image.open(ICON_ON_PATH)
            update_menu_for_running(icon)
    except Exception as e:
        logging.error(f"Ошибка запуска процесса: {e}")
        print(f"Ошибка запуска процесса: {e}")


def stop_process(icon=None, item=None):
    global process
    if process:
        process.terminate()
        process.wait()
        process = None
        logging.info("Процесс остановлен")
    if icon:
        icon.icon = Image.open(ICON_OFF_PATH)
        update_menu_for_stopped(icon)


def exit_program(icon=None, item=None):
    global process
    if process:
        process.terminate()
        process.wait()
        logging.info("Процесс остановлен при выходе")
    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)
    if icon:
        icon.stop()
    sys.exit(0)


def update_menu_for_running(icon):
    menu = pystray.Menu(
        pystray.MenuItem('Stop', stop_process),
        pystray.MenuItem('Exit', exit_program)
    )
    icon.menu = menu
    icon.update_menu()


def update_menu_for_stopped(icon):
    menu = pystray.Menu(
        pystray.MenuItem('Start', start_process),
        pystray.MenuItem('Exit', exit_program)
    )
    icon.menu = menu
    icon.update_menu()


def create_icon():
    icon_image = Image.open(ICON_OFF_PATH)
    menu = pystray.Menu(
        pystray.MenuItem('Start', start_process),
        pystray.MenuItem('Exit', exit_program)
    )
    global icon
    icon = pystray.Icon("goodbyedpi", icon_image, "GoodByeDPI", menu=menu)
    return icon


if __name__ == "__main__":
    bat_file_path = os.path.join(os.getcwd(), "run_zapret.bat")
    if not os.path.exists(bat_file_path):
        print(f"Файл {bat_file_path} не найден")
        sys.exit(1)

    lines = read_bat_file(bat_file_path)
    PARSED_COMMAND = find_winws_command(lines)
    print(f"Найденная команда запуска: {PARSED_COMMAND}")

    if PARSED_COMMAND is None:
        print("Не удалось найти команду запуска winws.exe в батнике.")
        sys.exit(1)

    if check_if_running():
        print("Процесс уже запущен. Завершите его перед повторным запуском.")
        sys.exit(1)

    print("Запуск приложения...")
    logging.info("Запуск приложения...")
    start_process(None)
    tray_icon = create_icon()
    tray_icon.run()

    print("Приложение остановлено.")
    logging.info("Приложение остановлено.")

    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)
