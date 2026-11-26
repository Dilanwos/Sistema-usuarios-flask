"""Modelo para asignar roles a los usuarios."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.user import User


class UserRole(UUIDMixin, TimestampMixin, db.Model):
    """Representa la asignación de un rol a un usuario."""

    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
    )

    assigned_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_roles",
        foreign_keys=[user_id],
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_roles",
    )

    assigner: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[assigned_by],
    )

    __table_args__ = (
        Index(
            "uq_user_roles_user_role",
            "user_id",
            "role_id",
            unique=True,
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<UserRole user_id={self.user_id} "
            f"role_id={self.role_id}>"
        )
