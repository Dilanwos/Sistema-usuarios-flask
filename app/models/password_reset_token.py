"""Modelo para gestionar tokens de recuperación de contraseñas."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin, UUIDMixin

# ─────────────────────────────────────────────
# IMPORTACIONES DE TIPOS
# ─────────────────────────────────────────────

if TYPE_CHECKING:
    from app.models.user import User


# ─────────────────────────────────────────────
# MODELO: PASSWORD RESET TOKEN
# ─────────────────────────────────────────────

class PasswordResetToken(UUIDMixin, TimestampMixin, db.Model):
    """Representa un token para recuperar la contraseña de un usuario."""

    __tablename__ = "password_reset_tokens"

    # ─────────────────────────────────────────
    # ATRIBUTOS
    # ─────────────────────────────────────────

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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
            f"<PasswordResetToken id={self.id} "
            f"user_id={self.user_id}>"
        )
