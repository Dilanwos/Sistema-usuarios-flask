"""Modelo para gestionar las notificaciones de los usuarios."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.enums import NotificationType
from app.models.mixins import TimestampMixin, UUIDMixin

# ─────────────────────────────────────────────
# IMPORTACIONES DE TIPOS
# ─────────────────────────────────────────────

if TYPE_CHECKING:
    from app.models.user import User


# ─────────────────────────────────────────────
# MODELO: NOTIFICATION
# ─────────────────────────────────────────────

class Notification(UUIDMixin, TimestampMixin, db.Model):
    """Representa una notificación dirigida a un usuario."""

    __tablename__ = "notifications"

    # ─────────────────────────────────────────
    # DESTINATARIO
    # ─────────────────────────────────────────

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ─────────────────────────────────────────
    # CONTENIDO
    # ─────────────────────────────────────────

    type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=NotificationType.INFO.value,
        server_default=NotificationType.INFO.value,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ─────────────────────────────────────────
    # ESTADO DE LECTURA
    # ─────────────────────────────────────────

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ─────────────────────────────────────────────
    # INFORMACIÓN ADICIONAL
    # ─────────────────────────────────────────────

    data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # ─────────────────────────────────────────
    # RELACIONES
    # ─────────────────────────────────────────

    user: Mapped["User"] = relationship(
        "User",
    )

    # ─────────────────────────────────────────
    # REPRESENTACIÓN
    # ─────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"<Notification id={self.id} "
            f"user_id={self.user_id} "
            f"type={self.type!r}>"
        )
