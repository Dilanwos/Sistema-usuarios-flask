"""Modelo para registrar las acciones del sistema."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
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
# MODELO: AUDIT LOG
# ─────────────────────────────────────────────

class AuditLog(UUIDMixin, TimestampMixin, db.Model):
    """Registra las acciones relevantes realizadas en el sistema."""

    __tablename__ = "audit_logs"

    # ─────────────────────────────────────────
    # ACTORES Y OBJETIVOS
    # ─────────────────────────────────────────

    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    target_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ─────────────────────────────────────────
    # INFORMACIÓN DE LA ACCIÓN
    # ─────────────────────────────────────────

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ─────────────────────────────────────────
    # CONTEXTO ADICIONAL
    # ─────────────────────────────────────────

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ─────────────────────────────────────────────
    # CONTEXTO ADICIONAL
    # ─────────────────────────────────────────────

    details: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # ─────────────────────────────────────────
    # RELACIONES
    # ─────────────────────────────────────────

    actor: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[actor_id],
    )

    target_user: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[target_user_id],
    )

    # ─────────────────────────────────────────
    # ÍNDICES
    # ─────────────────────────────────────────

    __table_args__ = (
        Index("ix_audit_logs_action", "action"),
        Index("ix_audit_logs_resource", "resource"),
        Index("ix_audit_logs_created_at", "created_at"),
    )

    # ─────────────────────────────────────────
    # REPRESENTACIÓN
    # ─────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"<AuditLog id={self.id} "
            f"action={self.action!r} "
            f"resource={self.resource!r}>"
        )
