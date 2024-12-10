GoodbyeDPI — Deep Packet Inspection circumvention utility
=========================

This software designed to bypass Deep Packet Inspection systems found in many Internet Service Providers which block access to certain websites.

It handles DPI connected using optical splitter or port mirroring (**Passive DPI**) which do not block any data but just replying faster than requested destination, and **Active DPI** connected in sequence.

**Windows 7, 8, 8.1, 10 or 11** with administrator privileges required.

# Quick start

Download the latest version and unzip it to any folder. Create a shortcut for the main.exe file and place it on your desktop for easy usage.
You need to use main.exe to start the program in the tray, and then you can select the desired .cmd to run it.
You can learn about how to run it in the service from the repo fork.
You don't need config.json anymore, just throw the cmd you need in the folder with main.exe, if you need to change some flag  - just change it inside confs.

Tray icon when the application is off:
![Off](src_Tray/icons/icon-off.jpg) <br>
Tray icon when the application is on:
![On](src_Tray/icons/icon-on.png)

```
Usage:
Run the exe file in the folder to run the program (do not rename it, as reruns are caught by the file name!!!).
Then in the OS tray select the desired mode and run, if you need to change some flag, go to confs and change it.
```

To check if your ISP's DPI could be circumvented, first make sure that your provider does not poison DNS answers by enabling "Secure DNS (DNS over HTTPS)" option in your browser.

* **Chrome**: Settings → [Privacy and security](chrome://settings/security) → Use secure DNS → With: NextDNS
* **Firefox**: [Settings](about:preferences) → Network Settings → Enable DNS over HTTPS → Use provider: NextDNS

Then run the `goodbyedpi.exe` executable without any options. If it works — congratulations! 

If your provider intercepts DNS requests, you may want to use `--dns-addr` option to a public DNS resolver running on non-standard port (such as Yandex DNS `77.88.8.8:1253`) or configure DNS over HTTPS/TLS using third-party applications.

## Links
- **[GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI/)** by @ValdikSS
- **[Zapret](https://github.com/Flowseal/zapret-discord-youtube)** by Flowseal

