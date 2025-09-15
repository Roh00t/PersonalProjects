# PassManager
A secure, self-hosted password manager with web UI, TOTP 2FA, and comprehensive audit logging. Built with FastAPI, PostgreSQL, and Docker Compose for easy deployment.

## 📺 Demos

[![PassManager Demo](https://img.youtube.com/vi/KMd9PJxJNNA/0.jpg)](https://youtu.be/KMd9PJxJNNA)

**[🎥 Watch the Full Demo on YouTube](https://youtu.be/KMd9PJxJNNA)**

See PassManager in action - from setup to daily usage, including:
- Initial installation and configuration
- User registration and 2FA setup
- Adding and managing passwords
- Security features demonstration

## Credits and Inspiration
Maintainer: [@Roh00t](https://github.com/Roh00t)
Inspiration: [@cyrolite](https://github.com/cyrolite/cyrolite)

## ✨ Features

- **🔐 Strong Security**: AES-GCM encryption at rest, Argon2id password hashing, CSRF protection
- **📱 TOTP 2FA**: Time-based one-time passwords with anti-replay protection
- **🔍 Comprehensive Auditing**: Structured logging for access, application, and security events
- **🐳 Easy Deployment**: Docker Compose stack with PostgreSQL
- **🎯 Simple UI**: Clean web interface with reveal/copy functionality
- **📊 Structured Logging**: JSON logs for monitoring and compliance

## 🏗️ Architecture

**Backend**: FastAPI with Jinja2 templating and minimal JavaScript
**Database**: PostgreSQL with encrypted vault storage
**Security**: Cookie-based sessions, CSRF tokens, CSP headers
**Encryption**: Per-user AES-GCM keys derived from master key + salt
**Logging**: Three-tier logging system (access/app/audit)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 5 minutes of your time

### 1. Configure Environment
```bash
# Copy the template
cp backend/.env.example backend/.env

# Generate a strong secret (example)
python3 -c "import secrets; print('SESSION_SECRET=' + secrets.token_urlsafe(48))"
python3 -c "import secrets; print('MASTER_KEY=' + secrets.token_urlsafe(48))"
```

Edit `backend/.env` with your secrets:
```env
# REQUIRED - Generate strong random values
SESSION_SECRET=your-session-secret-here
MASTER_KEY=your-master-key-here

# Database (already configured for Docker)
DATABASE_URL=postgresql+psycopg://passmanager:passmanager@db:5432/passmanager

# Security settings
COOKIE_SECURE=false  # Set to true in production with HTTPS
REQUIRE_2FA=true     # Enforce 2FA for all users
```

### 2. Start the Stack
```bash
# Build and start services
docker compose up -d --build

# Check status
docker compose ps
docker compose logs api --tail=50
```

### 3. Access the Application
Open http://localhost:8000

1. **Register** a new account
2. **Enable 2FA** (scan QR code with your authenticator app)
3. **Add passwords** to your vault
4. **Enjoy** secure password management!

## 📖 User Guide

### First-Time Setup
1. **Register**: Choose username/password at `/register`
2. **Login**: Enter credentials at `/`
3. **Setup 2FA**: Scan QR code or enter secret manually in your authenticator
4. **Verify**: Enter 6-digit code to enable 2FA

### Daily Usage
- **Add Items**: Title, URL (optional), username (optional), password (required)
- **View Passwords**: Click "Reveal" to decrypt and display
- **Copy to Clipboard**: One-click copy functionality
- **Delete Items**: Remove entries you no longer need
- **Logout**: Secure session termination

## 🔒 Security Model

### Encryption
- **At Rest**: AES-256-GCM with per-user derived keys
- **Key Derivation**: PBKDF2 using master key + per-user salt
- **Storage**: Database stores only ciphertext + nonce

### Authentication
- **Passwords**: Argon2id hashing
- **2FA**: TOTP with ±30s window tolerance
- **Sessions**: Signed cookies with CSRF protection
- **Anti-Replay**: TOTP counter prevents code reuse

### Headers & Protection
- Content Security Policy (CSP)
- X-Frame-Options, X-Content-Type-Options
- Secure cookie settings for production

## 📊 Logging & Auditing

### Log Files (in `logs/` directory)
- **`access.log`**: HTTP requests (method, path, status, timing, IP, User-Agent)
- **`app.log`**: Application events (errors, warnings, info)
- **`audit.log`**: Security events (JSON format)

### Audit Events Tracked
- Login attempts (success/failure)
- 2FA verification (success/failure)  
- 2FA setup/enable actions
- Vault operations (add/delete/reveal)
- All events include: user_id, IP, User-Agent, timestamp, success status

### Example Audit Log Entry
```json
{
  "timestamp": "2024-01-15T10:30:45Z",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "ip": "192.168.1.100",
  "action": "vault_reveal",
  "target_type": "vault_item",
  "target_id": "456e7890-e89b-12d3-a456-426614174111",
  "success": true,
  "detail": "Password revealed for item: Example Site"
}
```

## 🛠️ Operations

### Monitoring
```bash
# View logs
docker compose logs api --tail=100
tail -f logs/{access,app,audit}.log

# Check container health
docker compose ps
```

### Backup & Restore
```bash
# Backup database
docker compose exec db pg_dump -U passmanager -d passmanager -F c -f /tmp/backup.dump
docker compose cp db:/tmp/backup.dump ./backup-$(date +%Y%m%d).dump

# Restore database
docker compose exec -T db pg_restore -U passmanager -d passmanager < backup.dump
```

### Upgrading
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker compose up -d --build

# Check for any schema updates needed
docker compose logs api | grep -i "column.*does not exist"
```

## 🏭 Production Deployment

### Essential Security Checklist
- [ ] Set strong, unique `SESSION_SECRET` and `MASTER_KEY`
- [ ] Enable HTTPS and set `COOKIE_SECURE=true`
- [ ] Deploy behind reverse proxy (Nginx/Caddy/Traefik)
- [ ] Set up automated database backups
- [ ] Configure log rotation and monitoring
- [ ] Restrict network access (firewall rules)
- [ ] Consider read-only container filesystem

### Recommended Docker Compose for Production
```yaml
# Add to your docker-compose.yml
services:
  api:
    # ... existing config ...
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /tmp
    volumes:
      - ./logs:/app/logs  # Only writable mount
    
  db:
    # ... existing config ...
    restart: unless-stopped
    # Consider using a managed database service
```

### Reverse Proxy Example (Caddy)
```caddyfile
passmanager.yourdomain.com {
    reverse_proxy localhost:8000
    encode gzip
    log {
        output file /var/log/caddy/passmanager.log
    }
}
```

## 🔧 Configuration Reference

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `SESSION_SECRET` | *required* | Session signing key (32+ bytes) |
| `MASTER_KEY` | *required* | Encryption master key |
| `DATABASE_URL` | *set by compose* | PostgreSQL connection string |
| `COOKIE_SECURE` | `false` | Enable secure cookies (HTTPS only) |
| `REQUIRE_2FA` | `true` | Enforce 2FA for all users |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `LOG_RETENTION_DAYS` | `30` | Log file retention period |

### API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Login page |
| `POST` | `/login` | Password authentication |
| `GET/POST` | `/register` | User registration |
| `GET/POST` | `/verify-2fa` | TOTP verification |
| `GET/POST` | `/setup-2fa` | 2FA enrollment |
| `GET` | `/vault` | Password vault UI |
| `POST` | `/vault/add` | Add vault item |
| `POST` | `/vault/reveal` | Decrypt and return password |
| `POST` | `/vault/delete` | Remove vault item |
| `GET` | `/logout` | Session termination |

## 🐛 Troubleshooting

### Common Issues

**"Site can't be reached"**
```bash
# Check if containers are running
docker compose ps
docker compose logs api

# Common causes: missing .env values, DB not ready
```

**"Invalid TOTP code"**
```bash
# Check time synchronization (TOTP is time-based)
docker compose exec api date -u
docker compose exec db date -u

# Times should match within seconds
```

**"Column does not exist" after updates**
```bash
# Check for schema changes
docker compose logs api | grep -i column

# For development, reset database:
docker compose down -v
rm -rf docker-data/postgres
docker compose up -d --build
```

**CSRF 403 errors**
- Clear browser cache and cookies
- Ensure forms include CSRF tokens
- Check that session cookies are properly set

### Time Sync for 2FA
TOTP codes are time-sensitive. Ensure your Docker containers have accurate UTC time:
```bash
# Check container times
docker compose exec api date -u
docker compose exec db date -u

# If different, restart containers
docker compose restart
```

## 🚧 Roadmap & Future Enhancements

### Planned Features
- [ ] **Client-side encryption** (zero-knowledge architecture)
- [ ] **Database migrations** (Alembic integration)
- [ ] **Rate limiting** (login/2FA attempts)
- [ ] **User management** (admin panel)
- [ ] **Import/export** (CSV, 1Password, etc.)
- [ ] **Mobile app** (companion authentication)
- [ ] **Hardware key support** (FIDO2/WebAuthn)

### Contributing
Contributions welcome! Focus areas:
- Security enhancements
- UI/UX improvements  
- Additional import formats
- Performance optimizations

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Security Disclaimer

This is a **server-side encrypted** password manager, not zero-knowledge. The server can decrypt your passwords when you're logged in. For maximum security in high-threat environments, consider client-side encryption solutions.

**Trust model**: You trust the server operator (yourself in self-hosted scenarios) with your encrypted data.

## 💬 Support

- 📖 **Documentation**: See the detailed technical manual in your installation
- 🐛 **Issues**: GitHub Issues for bug reports
- 💡 **Discussions**: GitHub Discussions for questions and ideas

---

**Built with ❤️ for self-hosting enthusiasts who value security and simplicity.**