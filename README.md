# TLS Camouflage with mitmproxy + Burp Suite
A practical setup to rewrite the TLS **ClientHello** and force browser-like fingerprints during your web application assessments.

---

## 🚀 1. Start the TLS-camouflage proxy

Run mitmproxy with your custom script:
```bash
mitmproxy --listen-port 8085 -s chameleon.py

alias chameleon="mitmproxy --listen-port 8085 -s ~/repos/Chameleon-TLS/chameleon.py"
```
This proxy will rewrite:

- SNI  
- Cipher suite ordering  
- ALPN  
- TLS extensions  
- TLS version preferences  

so the outbound fingerprint resembles a real browser (e.g., Chrome), helping bypass simple WAF/CDN TLS fingerprinting.

---

## 🧰 2. Configure Burp Suite to send traffic through mitmproxy

### Step 2.1 — Add an upstream proxy

Navigate to:

User Options → Connections → Upstream Proxy Servers

Add a rule:

| Match | Proxy        | Port |
|-------|--------------|------|
| *     | 127.0.0.1    | 8085 |

This forces *all* outbound Burp traffic through mitmproxy.

---

## 🔧 3. Disable HTTP/2 negotiation in Burp

To allow mitmproxy to control ALPN and TLS parameters, Burp **must not** negotiate HTTP/2 by itself.

If Burp attempts to use HTTP/2 directly with the server, mitmproxy cannot fully rewrite the handshake.

---

## 🧩 Burp Suite 2023+ (most installations today)

Go to:

Project Options → HTTP → HTTP/2

Disable:

Use HTTP/2 where possible

This ensures Burp only uses HTTP/1.1 toward the server, leaving ALPN negotiation and all TLS fingerprinting to mitmproxy:

- ALPN selection  
- TLS ClientHello structuring  
- Cipher ordering  
- Extensions (JA3-like fields)

---

## 🧩 Burp Suite 2021–2022 (older versions)

Menu labels vary slightly.

Go to:

User Options → Connections → HTTP/2

Disable:

- Use HTTP/2 when making requests to the server  
or  
- Enable HTTP/2 where supported

Result: Burp stops negotiating HTTP/2, enabling mitmproxy to masquerade as a browser.

---

## ✔️ Summary

When configured correctly:

- Burp → sends HTTP/1.1 → into mitmproxy  
- mitmproxy → performs a **browser-like TLS handshake**  
- Target sees a normal browser rather than a security tool  
- TLS fingerprinting defences are weakened  
- CDNs/WAFs behave closer to how they treat real users  

Ideal for bypassing bot detection or behavioural filtering based on TLS metadata.

---

## 🛡️ Notes

- Ensure `chameleon.py` uses realistic, modern fingerprints (Chrome/Edge/Firefox).  
- If chaining proxies, mitmproxy must be the component negotiating TLS with the target.  
- Validate fingerprints using JA3/JA3S monitoring tools.
