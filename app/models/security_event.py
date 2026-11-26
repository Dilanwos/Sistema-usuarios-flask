"""Modelo para registrar eventos de seguridad del sistema."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin, UUIDMixin

# ─────────────────────────────────────────────
# IMPORTACIONES DE TIPOS
# ─────────────────────────────────────────────

if TYPE_CHECKING:
    from app.models.user import User


# ─────────────────────────────────────────────
# MODELO: SECURITY EVENT
# ─────────────────────────────────────────────

class SecurityEvent(UUIDMixin, TimestampMixin, db.Model):
    """Representa un evento relacionado con la seguridad."""

    __tablename__ = "security_events"

    # ─────────────────────────────────────────
    # USUARIO RELACIONADO
    # ─────────────────────────────────────────

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ─────────────────────────────────────────
    # INFORMACIÓN DEL EVENTO
    # ─────────────────────────────────────────

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ─────────────────────────────────────────────
    # CONTEXTO DE SEGURIDAD
    # ─────────────────────────────────────────────

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    details = mapped_column(JSONB, nullable=True)

    # ─────────────────────────────────────────────
    # RELACIONES
    # ─────────────────────────────────────────────

    user: Mapped["User | None"] = relationship(
        "User",
    )

    # ─────────────────────────────────────────────
    # ÍNDICES
    # ─────────────────────────────────────────────

    __table_args__ = (
        Index("ix_security_events_event_type", "event_type"),
        Index("ix_security_events_created_at", "created_at"),
    )

    # ─────────────────────────────────────────────
    # REPRESENTACIÓN
    # ─────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"<SecurityEvent id={self.id} "
            f"event_type={self.event_type!r}>"
        )
