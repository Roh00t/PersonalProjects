# PassManager (starter)

## Website (W.I.P)

A deployable, free-to-run password manager starter built with **FastAPI** + **PostgreSQL** + **Docker Compose**.
Focus is on pragmatic security: Argon2id password hashing, TOTP 2FA, AES-256-GCM encryption at rest, signed cookies, CSRF protections, and strict HTTP security headers.

> Trust model: server-side encryption using a per-user key derived from a server master key + per-user salt.
This is **not** "zero-knowledge". For true client-side/zero-knowledge crypto, see the _Upgrades_ section.

## Stack
- Backend: FastAPI (Python 3.11), SQLAlchemy
- DB: PostgreSQL (Docker)
- Crypto: argon2-cffi, cryptography (AESGCM), pyotp
- Templating: Jinja2
- Reverse proxy: none by default (add Caddy/Traefik for TLS in production)

## Quick start (Docker)
```bash
# 1) copy env template and set strong secrets
cp backend/.env.example backend/.env

# 2) start services
docker compose up --build

# 3) open
http://localhost:8000
```

## Admin notes
- Change **all** secrets in `.env` (SESSION_SECRET, MASTER_KEY, DB password).
- Create regular backups of the `postgres` volume.
- Consider adding Caddy/Traefik for Let's Encrypt TLS.

## Upgrades (later)
- Client-side, zero-knowledge encryption (WebCrypto/wasm Argon2)
- Encrypted search (blind index)
- Hardware keys (WebAuthn)
- Proper migrations (Alembic)
- Rate limiting via Redis
