start "zapret: http,https,quic" /min "%~dp0winws.exe" ^
--wf-tcp=80,443 ^
--wf-udp=443,50000-65535 ^
--filter-udp=443 --hostlist="%~dp0list-youtube.txt" --dpi-desync=fake,tamper --dpi-desync-repeats=11 --dpi-desync-fake-quic="%~dp0quic_initial_www_google_com.bin" --new ^
--filter-udp=443 --dpi-desync=fake,tamper --dpi-desync-autottl=2 --dpi-desync-repeats=11 --new ^
--filter-udp=50000-65535 --dpi-desync=fake,tamper --dpi-desync-any-protocol --dpi-desync-autottl=2 --dpi-desync-repeats=11 --new ^
--filter-tcp=80 --dpi-desync=fake,disorder2 --dpi-desync-autottl=2 --dpi-desync-fooling=badseq --new ^
--filter-tcp=443 --hostlist="%~dp0list-youtube.txt" --dpi-desync=fake,disorder2 --dpi-desync-autottl=2 --dpi-desync-fooling=badseq --dpi-desync-fake-tls="%~dp0tls_clienthello_www_google_com.bin" --new ^
--dpi-desync=fake,tamper --dpi-desync-any-protocol --dpi-desync-autottl=2 --dpi-desync-fooling=badseq --dpi-desync-fake-tls="%~dp0tls_clienthello_www_google_com.bin"
