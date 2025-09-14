import os, qrcode, base64, secrets, io
from pathlib import Path
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
import pyotp
REQUIRE_2FA = os.getenv("REQUIRE_2FA", "True").lower() == "true"

from .database import Base, engine, get_db
from .models import User, VaultItem
from .security import (
    hash_password, verify_password, set_session, get_session, clear_session,
    generate_csrf, csp_headers
)
from .crypto import derive_user_key, encrypt_blob, decrypt_blob


app = FastAPI(title="PassManager")

# Signed-cookie session for CSRF + pre-auth 2FA staging
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "change-me"),
    same_site=os.getenv("COOKIE_SAMESITE", "Lax"),
    https_only=os.getenv("COOKIE_SECURE", "False").lower() == "true",
)

templates = Jinja2Templates(directory="app/templates")

if Path("app/static").exists():
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)


def current_user(request: Request, db: Session) -> User | None:
    """Return logged-in user only when FULLY authenticated (i.e., after 2FA)."""
    sess = get_session(request)
    if not sess or "uid" not in sess:
        return None
    return db.get(User, sess["uid"])


@app.middleware("http")
async def add_security_headers(request, call_next):
    resp = await call_next(request)
    return csp_headers(resp)


def _assert_csrf(request: Request, csrf_token: str):
    if not csrf_token or request.session.get("csrf") != csrf_token:
        raise HTTPException(status_code=403, detail="Bad CSRF")

def _qr_data_url(text: str) -> str:
    img = qrcode.make(text, box_size=6, border=1)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ---------------------- Auth ----------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    if current_user(request, db):
        return RedirectResponse(url="/vault", status_code=302)
    csrf = generate_csrf()
    request.session["csrf"] = csrf
    return templates.TemplateResponse("login.html", {"request": request, "csrf": csrf, "message": ""})


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    _assert_csrf(request, csrf_token)
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        csrf = generate_csrf(); request.session["csrf"] = csrf
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "csrf": csrf, "message": "Invalid username or password."},
            status_code=400,
        )

    if user.totp_enabled:
        # 2FA already set → pre-auth session, then challenge
        resp = RedirectResponse(url="/verify-2fa", status_code=302)
        set_session(resp, {"pre_uid": str(user.id), "tfa": False})
    else:
        # 2FA not set
        # We must allow access to /setup-2fa, but block /vault until enabled.
        next_url = "/setup-2fa" if REQUIRE_2FA else "/vault"
        resp = RedirectResponse(url=next_url, status_code=302)
        set_session(resp, {"uid": str(user.id), "tfa": True})  # full session so /setup-2fa works
    return resp



@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    csrf = generate_csrf()
    request.session["csrf"] = csrf
    return templates.TemplateResponse("register.html", {"request": request, "csrf": csrf, "message": ""})


@app.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    _assert_csrf(request, csrf_token)
    if db.query(User).filter(User.username == username).first():
        csrf = generate_csrf()
        request.session["csrf"] = csrf
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "csrf": csrf, "message": "Username already exists."},
            status_code=400,
        )
    if len(username) > 64 or len(password) > 256:
        csrf = generate_csrf()
        request.session["csrf"] = csrf
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "csrf": csrf, "message": "Input too long."},
            status_code=400,
        )

    enc_salt = secrets.token_bytes(16)
    user = User(username=username, password_hash=hash_password(password), enc_salt=enc_salt)
    db.add(user); db.commit()
    return RedirectResponse(url="/", status_code=302)


@app.get("/logout")
def logout():
    resp = RedirectResponse(url="/", status_code=302)
    clear_session(resp)
    # Nudge browsers to dump caches/storage
    resp.headers["Clear-Site-Data"] = '"cache","cookies","storage"'
    return resp


@app.get("/session-check")
def session_check(request: Request, db: Session = Depends(get_db)):
    sess = get_session(request)
    uid = (sess or {}).get("uid")
    pre_uid = (sess or {}).get("pre_uid")

    if not uid and not pre_uid:
        raise HTTPException(status_code=401)

    # Fully logged-in user
    if uid:
        user = db.get(User, uid)
        if not user:
            raise HTTPException(status_code=401)
        if REQUIRE_2FA and not user.totp_enabled:
            return Response(status_code=403)  # will push to /setup-2fa
        if user.totp_enabled and not (sess or {}).get("tfa", False):
            return Response(status_code=403)  # will push to /verify-2fa
        return Response(status_code=204)

    # Pre-auth (after password, before 2FA)
    if pre_uid:
        return Response(status_code=403)



# ---------------------- 2FA ----------------------
@app.get("/verify-2fa", response_class=HTMLResponse)
def verify_2fa_page(request: Request):
    # Only if we have a pre-auth session
    sess = get_session(request)
    if not sess or "pre_uid" not in sess:
        return RedirectResponse(url="/", status_code=302)
    csrf = generate_csrf()
    request.session["csrf"] = csrf
    return templates.TemplateResponse("verify_2fa.html", {"request": request, "csrf": csrf})


@app.post("/verify-2fa")
def verify_2fa(request: Request, token: str = Form(...), csrf_token: str = Form(...), db: Session = Depends(get_db)):
    _assert_csrf(request, csrf_token)
    sess = get_session(request); uid = (sess or {}).get("pre_uid")
    if not uid: return RedirectResponse(url="/", status_code=302)
    user = db.get(User, uid)
    if not user or not user.totp_enabled or not user.totp_secret:
        return RedirectResponse(url="/", status_code=302)

    totp = pyotp.TOTP(user.totp_secret.decode())
    if not totp.verify(token, valid_window=1):     # tolerate ±1 step
        csrf = generate_csrf(); request.session["csrf"] = csrf
        return templates.TemplateResponse("verify_2fa.html",
            {"request": request, "csrf": csrf, "message": "Invalid code."},
            status_code=400)

    resp = RedirectResponse(url="/vault", status_code=302)
    set_session(resp, {"uid": str(user.id), "tfa": True})   # rotate session to fully authed
    return resp



@app.get("/setup-2fa", response_class=HTMLResponse)
def setup_2fa(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)      # must be fully authed (has uid)
    if not user:
        return RedirectResponse(url="/", status_code=302)

    secret = pyotp.random_base32()
    request.session["pending_tfa_secret"] = secret
    uri = pyotp.TOTP(secret).provisioning_uri(name=user.username, issuer_name="PassManager")
    qr = _qr_data_url(uri)

    csrf = generate_csrf()
    request.session["csrf"] = csrf
    return templates.TemplateResponse(
        "setup_2fa.html",
        {"request": request, "secret": secret, "otpauth": uri, "qr": qr, "csrf": csrf}
    )



@app.post("/enable-2fa")
def enable_2fa(request: Request,
               token: str = Form(...),
               csrf_token: str = Form(...),
               db: Session = Depends(get_db)):
    _assert_csrf(request, csrf_token)
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)

    secret = request.session.get("pending_tfa_secret")
    if not secret:
        raise HTTPException(status_code=400, detail="No 2FA setup in progress")

    totp = pyotp.TOTP(secret)
    if not totp.verify(token, valid_window=1):  # tolerate ±1 step
        csrf = generate_csrf(); request.session["csrf"] = csrf
        uri = pyotp.TOTP(secret).provisioning_uri(name=user.username, issuer_name="PassManager")
        qr = _qr_data_url(uri)
        return templates.TemplateResponse(
            "setup_2fa.html",
            {"request": request, "secret": secret, "otpauth": uri, "qr": qr, "csrf": csrf, "message": "Invalid code."},
            status_code=400,
        )

    user.totp_secret = secret.encode()
    user.totp_enabled = True
    db.commit()
    request.session.pop("pending_tfa_secret", None)
    return RedirectResponse(url="/", status_code=302)



# ---------------------- Vault ----------------------
@app.get("/vault", response_class=HTMLResponse)
def vault_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)

    # If policy requires 2FA and user hasn’t set it up yet → force setup
    if REQUIRE_2FA and not user.totp_enabled:
        return RedirectResponse(url="/setup-2fa", status_code=302)

    # If user has 2FA enabled but this session hasn’t passed the challenge → verify now
    sess = get_session(request)
    if user.totp_enabled and not (sess or {}).get("tfa", False):
        return RedirectResponse(url="/verify-2fa", status_code=302)

    items = [
        {"id": str(i.id), "title": i.title, "url": i.url or "", "username": i.username or ""}
        for i in user.items
    ]
    csrf = generate_csrf(); request.session["csrf"] = csrf
    return templates.TemplateResponse(
        "vault.html",
        {"request": request, "items": items, "username": user.username, "csrf": csrf, "tfa_enabled": user.totp_enabled},
    )



@app.post("/vault/add")
def vault_add(
    request: Request,
    title: str = Form(...), url: str = Form(""), vusername: str = Form(""),
    secret: str = Form(...), csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    _assert_csrf(request, csrf_token)

    key = derive_user_key(user.enc_salt)
    nonce, ct = encrypt_blob(secret.encode(), key)
    item = VaultItem(user_id=user.id, title=title, url=url, username=vusername, nonce=nonce, ciphertext=ct)
    db.add(item); db.commit()
    return RedirectResponse(url="/vault", status_code=302)


@app.post("/vault/delete")
def vault_delete(
    request: Request,
    item_id: str = Form(...), csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    _assert_csrf(request, csrf_token)

    item = db.query(VaultItem).filter(VaultItem.id == item_id, VaultItem.user_id == user.id).first()
    if item:
        db.delete(item); db.commit()
    return RedirectResponse(url="/vault", status_code=302)


@app.post("/vault/reveal")
def vault_reveal(
    request: Request,
    item_id: str = Form(...), csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    user = current_user(request, db)
    if not user:
        raise HTTPException(status_code=401)
    _assert_csrf(request, csrf_token)

    item = db.query(VaultItem).filter(VaultItem.id == item_id, VaultItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404)

    key = derive_user_key(user.enc_salt)
    plaintext = decrypt_blob(item.nonce, item.ciphertext, key).decode()

    resp = PlainTextResponse(plaintext)
    resp.headers["Cache-Control"] = "no-store"
    return resp
