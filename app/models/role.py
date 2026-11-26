
"""Modelo para administrar los roles del sistema."""

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
    from app.models.user_role import UserRole


# ─────────────────────────────────────────────
# MODELO: ROLE
# ─────────────────────────────────────────────

class Role(UUIDMixin, TimestampMixin, db.Model):
    """Representa un rol que agrupa permisos del sistema."""

    __tablename__ = "roles"

    # ─────────────────────────────────────────
    # ATRIBUTOS
    # ─────────────────────────────────────────

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
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

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="role",
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
    )

    # ─────────────────────────────────────────
    # REPRESENTACIÓN
    # ─────────────────────────────────────────

    def __repr__(self) -> str:
        return f"<Role id={self.id} name={self.name!r}>"
