GoodbyeDPI — Deep Packet Inspection circumvention utility
=========================
The current version is based on the flowseal implementation.
To select the desired parameters in conf.txt, look at the bat. files in flowseal release through editing. (Link below)

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

## Links
- **[GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI/)** by @ValdikSS
- **[Zapret](https://github.com/Flowseal/zapret-discord-youtube)** by Flowseal

