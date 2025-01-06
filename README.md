GoodbyeDPI — Deep Packet Inspection circumvention utility
=========================
The current version is based on the flowseal implementation.
To select the desired parameters in confs.txt, look at the bat. files in flowseal release through editing. (Link below)

**Windows 7, 8, 8.1, 10 or 11** with administrator privileges required.

# Quick start

Download the latest version and unzip it to any folder. Create a shortcut for the main.exe file and place it on your desktop for easy usage.
You need to use main.exe to start the program in the tray.
If you need to change some flag  - just change it inside confs.

Tray icon when the application is off:
![Off](src_Tray/icons/icon-off.jpg) <br>
Tray icon when the application is on:
![On](src_Tray/icons/icon-on.png)

```
Usage:
Run the exe file in the folder to run the program 
(do not rename it, as reruns are caught by the file name!!!).
Then in the OS tray select the desired mode and run, if you need to change some flag,
go to confs and change it.
```

To check if your ISP's DPI could be circumvented, first make sure that your provider does not poison DNS answers by enabling "Secure DNS (DNS over HTTPS)" option in your browser.

* **Chrome**: Settings → [Privacy and security](chrome://settings/security) → Use secure DNS → With: NextDNS
* **Firefox**: [Settings](about:preferences) → Network Settings → Enable DNS over HTTPS → Use provider: NextDNS

# Руководство для пользователей, у которых не работает с первой попытки. 
- Удалите/выключите все сервисы gdb/zapret
- Скачайте последний релиз Flowseal (cм. Links) и найдите .bat файл, который будет работать для вас
Как только вы это сделали, вам останется confs.txt, что для этого нужно сделать:  
Нажимаем кнопку "Изменить" по рабочему для вас .bat файлу, у вас откроется блокнот с его содержимым, открываете мой confs.txt  
В confs.txt удаляете все, кроме первой строчки (winws.exe)  
В .bat файле есть строка (start "zapret: general" /min "%BIN%winws.exe") после этой комбинации идет набор параметров запуска, которые нужно скопировать, каждый новый параметр (двойное тире) должнен начинаться с новой строки (см. confs.txt неизмененный), также, в параметрах, где есть путь к файлу (="....."), удаляете все после знака равно.
Новый confs.txt помещается вместо старого - готово! Если столкнулись с какими-либо трудностями, сообщатей в тг/почту/дискорд.  
# Пример.  
## Было:  
start "zapret: general" /min "%BIN%winws.exe" --wf-tcp=80,443 --wf-udp=443,50000-50100 ^  
--filter-udp=443 --hostlist="list-general.txt"  
## Стало:  
winws.exe  
--wf-tcp=80,443  
--wf-udp=443,50000-50100 ^  
--filter-udp=443  
--hostlist=  
## Links
- **[GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI/)** by @ValdikSS
- **[Zapret](https://github.com/Flowseal/zapret-discord-youtube)** by Flowseal

