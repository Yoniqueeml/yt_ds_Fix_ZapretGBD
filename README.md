GoodbyeDPI — Deep Packet Inspection circumvention utility
=========================

This software designed to bypass Deep Packet Inspection systems found in many Internet Service Providers which block access to certain websites.

It handles DPI connected using optical splitter or port mirroring (**Passive DPI**) which do not block any data but just replying faster than requested destination, and **Active DPI** connected in sequence.

**Windows 7, 8, 8.1, 10 or 11** with administrator privileges required.

# Quick start

Download the latest version and unzip it to any folder. Create a shortcut for the main.exe file and place it on your desktop for easy usage.
You need to use main.exe to start the program in the tray, and then you can select the desired .cmd to run it.
You can learn about how to run it in the service from the repo fork.
You don't need config.json anymore, just throw the cmd you need in the folder with main.exe, if you need to change some flag in some cmd - just change it inside cmd. Added working version after 22.09

Tray icon when the application is off:
![Off](src_Tray/icons/icon-off.jpg) <br>
Tray icon when the application is on:
![On](src_Tray/icons/icon-on.png)

```
Usage:
Run the exe file in the folder to run the program (do not rename it, as reruns are caught by the file name!!!).
Then in the OS tray select the desired mode and run, if you need to change some flag, go to config.json and change it.
Usage: goodbyedpi.exe [OPTION...]
-p          block passive DPI
 -q          block QUIC/HTTP3
 -r          replace Host with hoSt
 -s          remove space between host header and its value
 -m          mix Host header case (test.com -> tEsT.cOm)
 -f <value>  set HTTP fragmentation to value
 -k <value>  enable HTTP persistent (keep-alive) fragmentation and set it to value
 -n          do not wait for first segment ACK when -k is enabled
 -e <value>  set HTTPS fragmentation to value
 -a          additional space between Method and Request-URI (enables -s, may break sites)
 -w          try to find and parse HTTP traffic on all processed ports (not only on port 80)
 --port        <value>    additional TCP port to perform fragmentation on (and HTTP tricks with -w)
 --ip-id       <value>    handle additional IP ID (decimal, drop redirects and TCP RSTs with this ID).
                          This option can be supplied multiple times.
 --dns-addr    <value>    redirect UDP DNS requests to the supplied IP address (experimental)
 --dns-port    <value>    redirect UDP DNS requests to the supplied port (53 by default)
 --dnsv6-addr  <value>    redirect UDPv6 DNS requests to the supplied IPv6 address (experimental)
 --dnsv6-port  <value>    redirect UDPv6 DNS requests to the supplied port (53 by default)
 --dns-verb               print verbose DNS redirection messages
 --blacklist   <txtfile>  perform circumvention tricks only to host names and subdomains from
                          supplied text file (HTTP Host/TLS SNI).
                          This option can be supplied multiple times.
 --allow-no-sni           perform circumvention if TLS SNI can't be detected with --blacklist enabled.
 --frag-by-sni            if SNI is detected in TLS packet, fragment the packet right before SNI value.
 --set-ttl     <value>    activate Fake Request Mode and send it with supplied TTL value.
                          DANGEROUS! May break websites in unexpected ways. Use with care (or --blacklist).
 --auto-ttl    [a1-a2-m]  activate Fake Request Mode, automatically detect TTL and decrease
                          it based on a distance. If the distance is shorter than a2, TTL is decreased
                          by a2. If it's longer, (a1; a2) scale is used with the distance as a weight.
                          If the resulting TTL is more than m(ax), set it to m.
                          Default (if set): --auto-ttl 1-4-10. Also sets --min-ttl 3.
                          DANGEROUS! May break websites in unexpected ways. Use with care (or --blacklist).
 --min-ttl     <value>    minimum TTL distance (128/64 - TTL) for which to send Fake Request
                          in --set-ttl and --auto-ttl modes.
 --wrong-chksum           activate Fake Request Mode and send it with incorrect TCP checksum.
                          May not work in a VM or with some routers, but is safer than set-ttl.
 --wrong-seq              activate Fake Request Mode and send it with TCP SEQ/ACK in the past.
 --native-frag            fragment (split) the packets by sending them in smaller packets, without
                          shrinking the Window Size. Works faster (does not slow down the connection)
                          and better.
 --reverse-frag           fragment (split) the packets just as --native-frag, but send them in the
                          reversed order. Works with the websites which could not handle segmented
                          HTTPS TLS ClientHello (because they receive the TCP flow "combined").
 --fake-from-hex <value>  Load fake packets for Fake Request Mode from HEX values (like 1234abcDEF).
                          This option can be supplied multiple times, in this case each fake packet
                          would be sent on every request in the command line argument order.
 --fake-gen <value>       Generate random-filled fake packets for Fake Request Mode, value of them
                          (up to 30).
 --fake-resend <value>    Send each fake packet value number of times.
                          Default: 1 (send each packet once).
 --max-payload [value]    packets with TCP payload data more than [value] won't be processed.
                          Use this option to reduce CPU usage by skipping huge amount of data
                          (like file transfers) in already established sessions.
                          May skip some huge HTTP requests from being processed.
                          Default (if set): --max-payload 1200.


LEGACY modesets:
 -1          -p -r -s -f 2 -k 2 -n -e 2 (most compatible mode)
 -2          -p -r -s -f 2 -k 2 -n -e 40 (better speed for HTTPS yet still compatible)
 -3          -p -r -s -e 40 (better speed for HTTP and HTTPS)
 -4          -p -r -s (best speed)

Modern modesets (more stable, more compatible, faster):
 -5          -f 2 -e 2 --auto-ttl --reverse-frag --max-payload
 -6          -f 2 -e 2 --wrong-seq --reverse-frag --max-payload
 -7          -f 2 -e 2 --wrong-chksum --reverse-frag --max-payload
 -8          -f 2 -e 2 --wrong-seq --wrong-chksum --reverse-frag --max-payload
 -9          -f 2 -e 2 --wrong-seq --wrong-chksum --reverse-frag --max-payload -q (this is the default)

 Note: combination of --wrong-seq and --wrong-chksum generates two different fake packets.
```

To check if your ISP's DPI could be circumvented, first make sure that your provider does not poison DNS answers by enabling "Secure DNS (DNS over HTTPS)" option in your browser.

* **Chrome**: Settings → [Privacy and security](chrome://settings/security) → Use secure DNS → With: NextDNS
* **Firefox**: [Settings](about:preferences) → Network Settings → Enable DNS over HTTPS → Use provider: NextDNS

Then run the `goodbyedpi.exe` executable without any options. If it works — congratulations! You can use it as-is or configure further, for example by using `--blacklist` option if the list of blocked websites is known and available for your country.

If your provider intercepts DNS requests, you may want to use `--dns-addr` option to a public DNS resolver running on non-standard port (such as Yandex DNS `77.88.8.8:1253`) or configure DNS over HTTPS/TLS using third-party applications.

Check the .cmd scripts and modify it according to your preference and network conditions.

## Links
- **[GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI/)** by @ValdikSS

