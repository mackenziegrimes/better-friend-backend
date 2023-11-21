"""Wrapper to create, and setup, new Quart server instance"""
from typing import Sequence, Optional, List

from quart import Quart, Config
from quart.typing import RouteCallable

from src.app_config import AppConfig
from src.firestore import Firestore
from src.routes import health, persons, users, connections


class AppWrapper:
    """Module wrapping Quart app that creates new Quart app and auto-wires all routes"""
    def __init__(self, test_config: Optional[Config] = None):
        self.app = Quart(__name__)
        self._configs(test_config)

        # define blueprints and their base url paths
        self.app.register_blueprint(health.bp, url_prefix="/health")
        self.app.register_blueprint(users.bp, url_prefix="/users")
        self.app.register_blueprint(
            persons.bp, url_prefix="/users/<string:user_id>/persons"
        )
        self.app.register_blueprint(
            connections.bp,
            url_prefix="/users/<string:user_id>/persons/<string:person_id>/connections",
        )

    # load configs into quart app
    def _configs(self, config: Optional[Config] = None) -> None:
        if config is not None:
            self.app.config.from_object(config)

        else:
            new_config = AppConfig()
            self.app.config.from_object(new_config)

    def run(self, **kwargs) -> None:
        """Start Quart app"""
        self.app.run(**kwargs)
