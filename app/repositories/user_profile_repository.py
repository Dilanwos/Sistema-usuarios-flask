"""Repositorio de acceso a datos de perfiles de usuario."""

import uuid

from sqlalchemy import select

from app.extensions import db
from app.models.user_profile import UserProfile


class UserProfileRepository:
    """Gestiona las operaciones de persistencia de perfiles."""

    @staticmethod
    def get_by_user_id(user_id: uuid.UUID) -> UserProfile | None:
        """Obtiene el perfil asociado a un usuario."""

        statement = select(UserProfile).where(
            UserProfile.user_id == user_id
        )

        return db.session.scalar(statement)

    @staticmethod
    def add(profile: UserProfile) -> UserProfile:
        """Agrega un perfil a la sesión actual."""

        db.session.add(profile)

        return profile
