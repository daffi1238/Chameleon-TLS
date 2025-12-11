✔️ Levantar el proxy TLS:
mitmproxy --listen-port 8085 -s tls_camouflage.py

✔️ Configurar Burp

En:

User Options → Connections → Upstream Proxy Servers


Añade:

Match: *
Proxy: 127.0.0.1
Port: 8085

- Y desactiva “Use HTTP/2 when requesting from server” en Burp, para que sea mitmproxy quien gestione ALPN.
```
✅ Burp Suite 2023+ (la mayoría de instalaciones hoy)

Ve a:
Project Options → HTTP

Sección: HTTP/2

Desmarca:
✔ Use HTTP/2 where possible

Esto hace que Burp NO negocie ALPN con HTTP/2 directamente contra el servidor, dejando a tu proxy (mitmproxy) gestionar:

ALPN

TLS ClientHello

Ciphers

Extensiones

✅ Burp Suite 2022.x – 2021.x

En algunas versiones aparece así:

Ruta:
User Options → Connections → HTTP/2

Desmarca:

Use HTTP/2 when making requests to the server
o

Enable HTTP/2 where supported
```