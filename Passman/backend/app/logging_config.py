import os, json, time, uuid, re, logging, logging.config, contextvars
from pythonjsonlogger import jsonlogger

# context for correlation id
request_id_var = contextvars.ContextVar("request_id", default=None)

# --------- redaction filter ----------
_REDACT_KEYS = set(
    (os.getenv("LOG_REDACT_FIELDS") or "password,secret,token,csrf,csrf_token,totp,otp").split(",")
)
_REDACT_RX = re.compile(r"(" + "|".join(map(re.escape, _REDACT_KEYS)) + r")", re.I)

class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # redact known fields in JSON dict-like messages
        try:
            if isinstance(record.msg, dict):
                for k in list(record.msg.keys()):
                    if k.lower() in _REDACT_KEYS:
                        record.msg[k] = "[REDACTED]"
            else:
                # scrub in string payloads
                s = str(record.getMessage())
                if _REDACT_RX.search(s):
                    record.msg = _REDACT_RX.sub(lambda m: m.group(1) + "=***", s)
        except Exception:
            pass
        # always attach request_id if present
        rid = request_id_var.get()
        if rid:
            setattr(record, "request_id", rid)
        return True

# --------- JSON formatter that includes contextual fields ----------
class JsonFmt(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("level", record.levelname)
        log_record.setdefault("logger", record.name)
        log_record.setdefault("request_id", getattr(record, "request_id", request_id_var.get()))
        log_record.setdefault("ts", int(time.time()*1000))

def _rot_handler(path, level):
    return {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": level,
        "filename": path,
        "when": "D",
        "interval": 1,
        "backupCount": int(os.getenv("LOG_RETENTION_DAYS", "30")),
        "encoding": "utf-8",
        "formatter": "json",
        "filters": ["redact"],
    }

def setup_logging():
    log_dir = os.getenv("LOG_DIR", "/var/log/passman")
    os.makedirs(log_dir, exist_ok=True)
    lvl = os.getenv("LOG_LEVEL", "INFO").upper()
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"redact": {"()": RedactFilter}},
        "formatters": {
            "json": {"()": JsonFmt, "fmt": "%(message)s"},
            "plain": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"},
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "level": lvl, "formatter": "plain", "filters": ["redact"]},
            "app_file": _rot_handler(f"{log_dir}/app.log", lvl),
            "access_file": _rot_handler(f"{log_dir}/access.log", "INFO"),
            "audit_file": _rot_handler(f"{log_dir}/audit.log", "INFO"),
        },
        "loggers": {
            # application logs
            "passman": {"handlers": ["console", "app_file"], "level": lvl, "propagate": False},
            # access (request) logs
            "access": {"handlers": ["console", "access_file"], "level": "INFO", "propagate": False},
            # security audit logs
            "audit": {"handlers": ["console", "audit_file"], "level": "INFO", "propagate": False},
            # uvicorn -> route to our files too
            "uvicorn.error": {"handlers": ["console", "app_file"], "level": "INFO", "propagate": False},
            "uvicorn.access": {"handlers": ["console", "access_file"], "level": "INFO", "propagate": False},
        },
        "root": {"handlers": ["console", "app_file"], "level": lvl},
    }
    logging.config.dictConfig(cfg)

# helpers
def new_request_id() -> str:
    rid = uuid.uuid4().hex
    request_id_var.set(rid)
    return rid

def client_ip(scope_headers) -> str:
    h = {k.decode().lower(): v.decode() for k, v in scope_headers}
    xff = h.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return h.get("x-real-ip") or "0.0.0.0"
