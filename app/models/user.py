from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_profile import UserProfile

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.enums import UserStatus
from app.models.mixins import (
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)


class User(UUIDMixin, TimestampMixin, SoftDeleteMixin, db.Model):
    """Representa una cuenta de usuario del sistema."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=UserStatus.PENDING_VERIFICATION.value,
        server_default=UserStatus.PENDING_VERIFICATION.value,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relaciones: se conectarán al implementar los modelos correspondientes.
    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )

    user_roles = relationship(
        "UserRole",
        back_populates="user",
        foreign_keys="UserRole.user_id",
    )

    sessions = relationship(
        "UserSession",
        back_populates="user",
    )

    __table_args__ = (
        Index("ix_users_status", "status"),
        Index("ix_users_deleted_at", "deleted_at"),
        Index("ix_users_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
