# This script rewrites the TLS ClientHello to mimic Chrome or another browser.
# Comments in English as requested.

from mitmproxy import tls
from mitmproxy import ctx

def tls_clienthello(flow: tls.ClientHelloData):
    """
    Modify the outgoing TLS handshake so the CDN sees a normal Chrome-like client.
    """

    ch = flow.client_hello

    # ----- 1. Force SNI -----
    ch.sni = flow.server_conn.address[0]

    # ----- 2. Custom cipher suite ordering -----
    # Example: mimic Chrome TLS 1.3 + 1.2 suites
    ch.cipher_suites = [
        0x1301,  # TLS_AES_128_GCM_SHA256
        0x1302,  # TLS_AES_256_GCM_SHA384
        0x1303,  # TLS_CHACHA20_POLY1305_SHA256
        0xCCA8,  # ECDHE_RSA_CHACHA20_POLY1305
        0xC02F,  # TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
        0xC02B,  # TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
    ]

    # ----- 3. Force ALPN -----
    ch.alpn_protocols = [b"h2", b"http/1.1"]

    # ----- 4. Add GREASE to appear natural -----
    ch.grease = True

    # ----- 5. Randomize some fingerprint details -----
    ch.randomize_ext_order = True

    ctx.log.info(f"[TLS] Modified ClientHello for {flow.server_conn.address}")
