import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, DateTime, Boolean, LargeBinary, ForeignKey, Text, func, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # 2FA
    totp_secret: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    totp_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    # per-user salt for encryption KDF
    enc_salt: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    items: Mapped[list["VaultItem"]] = relationship("VaultItem", back_populates="owner", cascade="all, delete-orphan")

class VaultItem(Base):
    __tablename__ = "vault_items"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=True)
    username: Mapped[str] = mapped_column(String(200), nullable=True)
    # AES-GCM stored fields
    nonce: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    ciphertext: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner: Mapped["User"] = relationship("User", back_populates="items")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    # keep audit PK as integer (no FK), or make it UUID if you prefer.
    # Using integer here is fine even in a UUID world:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # FK to users.id (UUID)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                         server_default=func.now(), index=True)

    ip: Mapped[str | None] = mapped_column(String(64))
    ua: Mapped[str | None] = mapped_column(String(256))

    action: Mapped[str] = mapped_column(String(64), index=True)     # e.g., login, verify_2fa, vault_add
    target_type: Mapped[str | None] = mapped_column(String(32))     # e.g., item
    # if you want to link to VaultItem, make this UUID; otherwise keep as string.
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

    success: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    detail: Mapped[str | None] = mapped_column(Text)

Index("ix_audit_user_ts", AuditEvent.user_id, AuditEvent.ts)
