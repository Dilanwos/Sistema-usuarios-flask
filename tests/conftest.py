"""Configuración y fixtures para las pruebas automatizadas."""

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    """Crea una aplicación aislada para las pruebas."""

    application = create_app("testing")

    database_url = make_url(
        application.config["SQLALCHEMY_DATABASE_URI"]
    )

    if database_url.database != "sistema_usuarios_test":
        pytest.fail(
            "Las pruebas deben utilizar exclusivamente "
            "la base de datos sistema_usuarios_test."
        )

    with application.app_context():
        yield application

        db.session.remove()


@pytest.fixture
def client(app):
    """Proporciona un cliente de pruebas de Flask."""

    return app.test_client()


@pytest.fixture
def clean_database(app):
    """Limpia las tablas antes de cada prueba."""

    db.session.execute(
        text(
            """
            TRUNCATE TABLE
                audit_logs,
                email_verification_tokens,
                notifications,
                password_reset_tokens,
                permissions,
                role_permissions,
                roles,
                security_events,
                user_profiles,
                user_roles,
                user_sessions,
                users
            RESTART IDENTITY CASCADE
            """
        )
    )

    db.session.commit()
