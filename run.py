"""Punto de entrada de Sistema de Gestión de Usuarios 2.0."""

from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run()
