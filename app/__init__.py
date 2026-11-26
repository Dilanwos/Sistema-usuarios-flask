"""Inicialización y configuración de la aplicación Flask."""

import os

from flask import Flask

from app.config import config_by_name
from app.extensions import (
    csrf,
    db,
    limiter,
    login_manager,
    migrate,
)

# ─────────────────────────────────────────────
# FÁBRICA DE APLICACIONES
# ─────────────────────────────────────────────

def create_app(config_name=None):
    """Crea y configura una instancia de la aplicación Flask."""

    # ─────────────────────────────────────────
    # CREACIÓN DE LA APLICACIÓN
    # ─────────────────────────────────────────

    app = Flask(
        __name__,
        instance_relative_config=True,
    )

    # ─────────────────────────────────────────
    # SELECCIÓN DEL ENTORNO
    # ─────────────────────────────────────────

    config_name = config_name or os.getenv(
        "APP_ENV",
        "development",
    )

    config_class = config_by_name.get(config_name)

    if config_class is None:
        raise ValueError(
            f"Configuración no válida: {config_name}"
        )

    # ─────────────────────────────────────────
    # CARGA DE CONFIGURACIÓN
    # ─────────────────────────────────────────

    app.config.from_object(config_class)

    # ─────────────────────────────────────────
    # VALIDACIÓN DE CONFIGURACIÓN CRÍTICA
    # ─────────────────────────────────────────

    required_settings = [
        "SECRET_KEY",
        "WTF_CSRF_SECRET_KEY",
        "SQLALCHEMY_DATABASE_URI",
    ]

    for setting in required_settings:
        if not app.config.get(setting):
            raise RuntimeError(
                f"La configuración {setting} es obligatoria."
            )

    # ─────────────────────────────────────────
    # INICIALIZACIÓN DE EXTENSIONES
    # ─────────────────────────────────────────

    db.init_app(app)

    # ─────────────────────────────────────────
    # REGISTRO CENTRALIZADO DE MODELOS
    # ─────────────────────────────────────────

    from app.models import registry  # noqa: F401

    # ─────────────────────────────────────────
    # INICIALIZACIÓN DE MIGRACIONES
    # ─────────────────────────────────────────

    migrate.init_app(app, db)

    # ─────────────────────────────────────────
    # AUTENTICACIÓN Y SEGURIDAD
    # ─────────────────────────────────────────

    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # ─────────────────────────────────────────
    # CONFIGURACIÓN DEL LOGIN
    # ─────────────────────────────────────────

    login_manager.login_view = "auth.login"

    login_manager.login_message = (
        "Debes iniciar sesión para acceder a esta página."
    )

    login_manager.login_message_category = "warning"

    # ─────────────────────────────────────────
    # RETORNO DE LA APLICACIÓN
    # ─────────────────────────────────────────

    return app
