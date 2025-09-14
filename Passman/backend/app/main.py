import os, secrets, base64
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pyotp

from .database import Base, engine, get_db
from .models import User, VaultItem
from .security import hash_password, verify_password, set_session, get_session, clear_session, generate_csrf, csp_headers
from .crypto import derive_user_key, encrypt_blob, decrypt_blob

app = FastAPI(title="PassManager")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create tables
Base.metadata.create_all(bind=engine)

def current_user(request: Request, db: Session) -> User | None:
    sess = get_session(request)
    if not sess or "uid" not in sess:
        return None
    return db.get(User, sess["uid"])

@app.middleware("http")
async def add_security_headers(request, call_next):
    resp = await call_next(request)
    return csp_headers(resp)

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if user:
        return RedirectResponse(url="/vault", status_code=302)
    csrf = generate_csrf()
    request.session = {"csrf": csrf}
    return templates.TemplateResponse("login.html", {"request": request, "csrf": csrf, "message": ""})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # If 2FA enabled, redirect to verify
    resp = RedirectResponse(url="/verify-2fa", status_code=302) if user.totp_enabled else RedirectResponse(url="/vault", status_code=302)
    set_session(resp, {"uid": str(user.id), "tfa": not user.totp_enabled})
    return resp

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    csrf = generate_csrf()
    request.session = {"csrf": csrf}
    return templates.TemplateResponse("register.html", {"request": request, "csrf": csrf})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username exists")
    enc_salt = secrets.token_bytes(16)
    user = User(username=username, password_hash=hash_password(password), enc_salt=enc_salt)
    db.add(user); db.commit()
    return RedirectResponse(url="/setup-2fa", status_code=302)

@app.get("/logout")
def logout():
    resp = RedirectResponse(url="/", status_code=302)
    clear_session(resp)
    return resp

@app.get("/setup-2fa", response_class=HTMLResponse)
def setup_2fa(request: Request, db: Session = Depends(get_db)):
    # Require login ideally; keep simple: generate for latest registered user if not logged
    sess = get_session(request)
    user = None
    if sess:
        user = db.get(User, sess.get("uid"))
    # In real system, enforce auth
    secret = pyotp.random_base32()
    uri_example = pyotp.totp.TOTP(secret).provisioning_uri(name="PassManager", issuer_name="PassManager")
    return templates.TemplateResponse("setup_2fa.html", {"request": request, "secret": secret, "otpauth": uri_example})

@app.post("/enable-2fa")
def enable_2fa(request: Request, username: str = Form(...), secret: str = Form(...), token: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    totp = pyotp.TOTP(secret)
    if not totp.verify(token):
        raise HTTPException(status_code=400, detail="Invalid TOTP")
    user.totp_secret = secret.encode()
    user.totp_enabled = True
    db.commit()
    return RedirectResponse(url="/", status_code=302)

@app.get("/verify-2fa", response_class=HTMLResponse)
def verify_2fa_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("verify_2fa.html", {"request": request})

@app.post("/verify-2fa")
def verify_2fa(request: Request, token: str = Form(...), db: Session = Depends(get_db)):
    sess = get_session(request)
    if not sess or "uid" not in sess:
        return RedirectResponse(url="/", status_code=302)
    user = db.get(User, sess["uid"])
    if not user or not user.totp_enabled or not user.totp_secret:
        return RedirectResponse(url="/vault", status_code=302)
    totp = pyotp.TOTP(user.totp_secret.decode())
    if not totp.verify(token):
        raise HTTPException(status_code=400, detail="Invalid TOTP")
    resp = RedirectResponse(url="/vault", status_code=302)
    set_session(resp, {"uid": str(user.id), "tfa": True})
    return resp

@app.get("/vault", response_class=HTMLResponse)
def vault_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if not get_session(request).get("tfa", False) and user.totp_enabled:
        return RedirectResponse(url="/verify-2fa", status_code=302)
    key = derive_user_key(user.enc_salt)
    items = []
    for item in user.items:
        try:
            plaintext = decrypt_blob(item.nonce, item.ciphertext, key).decode()
        except Exception:
            plaintext = "*** decryption error ***"
        items.append({"id": str(item.id), "title": item.title, "url": item.url or "", "username": item.username or "", "secret": plaintext})
    return templates.TemplateResponse("vault.html", {"request": request, "items": items, "username": user.username})

@app.post("/vault/add")
def vault_add(request: Request, title: str = Form(...), url: str = Form(""), vusername: str = Form(""), secret: str = Form(...), db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    key = derive_user_key(user.enc_salt)
    nonce, ct = encrypt_blob(secret.encode(), key)
    item = VaultItem(user_id=user.id, title=title, url=url, username=vusername, nonce=nonce, ciphertext=ct)
    db.add(item); db.commit()
    return RedirectResponse(url="/vault", status_code=302)

@app.post("/vault/delete")
def vault_delete(request: Request, item_id: str = Form(...), db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    item = db.query(VaultItem).filter(VaultItem.id == item_id, VaultItem.user_id == user.id).first()
    if item:
        db.delete(item); db.commit()
    return RedirectResponse(url="/vault", status_code=302)
