"""Pruebas de configuración y conexión de la base de datos."""

from sqlalchemy import text

from app.extensions import db


def test_database_connection(app):
    """Comprueba que la aplicación conecta con la base de pruebas."""

    with app.app_context():
        result = db.session.execute(
            text("SELECT current_database()")
        ).scalar_one()

        assert result == "sistema_usuarios_test"


def test_database_tables_exist(app):
    """Comprueba que las tablas principales están disponibles."""

    expected_tables = {
        "users",
        "user_profiles",
        "roles",
        "permissions",
        "user_roles",
        "role_permissions",
        "user_sessions",
        "email_verification_tokens",
        "password_reset_tokens",
        "audit_logs",
        "notifications",
        "security_events",
    }

    with app.app_context():
        existing_tables = set(
            db.metadata.tables.keys()
        )

        assert expected_tables.issubset(existing_tables)
