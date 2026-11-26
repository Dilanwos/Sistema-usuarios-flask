"""Modelo para relacionar roles con permisos."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin, UUIDMixin

# ─────────────────────────────────────────────
# IMPORTACIONES DE TIPOS
# ─────────────────────────────────────────────

if TYPE_CHECKING:
    from app.models.permission import Permission
    from app.models.role import Role


# ─────────────────────────────────────────────
# MODELO: ROLE PERMISSION
# ─────────────────────────────────────────────

class RolePermission(UUIDMixin, TimestampMixin, db.Model):
    """Representa la asignación de un permiso a un rol."""

    __tablename__ = "role_permissions"

    # ─────────────────────────────────────────
    # ATRIBUTOS
    # ─────────────────────────────────────────

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("permissions.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # ─────────────────────────────────────────
    # RELACIONES
    # ─────────────────────────────────────────

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="role_permissions",
    )

    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="role_permissions",
    )

    # ─────────────────────────────────────────
    # RESTRICCIONES
    # ─────────────────────────────────────────

    __table_args__ = (
        Index(
            "uq_role_permissions_role_permission",
            "role_id",
            "permission_id",
            unique=True,
        ),
    )

    # ─────────────────────────────────────────
    # REPRESENTACIÓN
    # ─────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"<RolePermission role_id={self.role_id} "
            f"permission_id={self.permission_id}>"
        )
