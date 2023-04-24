from flask import Flask, Config, logging
from typing import Sequence, Optional
from .app_wrapper import AppWrapper, AppConfig
from .routes import (
    health,
    persons,
    connections,
)


wrapper = AppWrapper()
flask_app: Flask = wrapper.app

# blueprints
flask_app.register_blueprint(health.bp, url_prefix="/health")
flask_app.register_blueprint(persons.bp, url_prefix="/persons")
flask_app.register_blueprint(connections.bp, url_prefix="/connections")

if __name__ == "__main__":
    flask_app.run(host="127.0.0.1", port=flask_app.config.PORT, use_evalex=False)
    # app.run(host="0.0.0.0", port=config.PORT)
