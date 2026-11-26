"""Modelo para administrar los permisos del sistema."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin, UUIDMixin

# ─────────────────────────────────────────────
# IMPORTACIONES DE TIPOS
# ─────────────────────────────────────────────

if TYPE_CHECKING:
    from app.models.role_permission import RolePermission


# ─────────────────────────────────────────────
# MODELO: PERMISSION
# ─────────────────────────────────────────────

class Permission(UUIDMixin, TimestampMixin, db.Model):
    """Representa una acción autorizable dentro del sistema."""

    __tablename__ = "permissions"

    # ─────────────────────────────────────────
    # ATRIBUTOS
    # ─────────────────────────────────────────

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    resource: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    # ─────────────────────────────────────────
    # RELACIONES
    # ─────────────────────────────────────────

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="permission",
    )

    # ─────────────────────────────────────────
    # REPRESENTACIÓN
    # ─────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"<Permission id={self.id} "
            f"name={self.name!r}>"
        )
