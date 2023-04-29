from quart import Quart, Config
from quart.typing import RouteCallable

from typing import Sequence, Optional, List

from ..app_config import AppConfig
from ..firestore import Firestore
from ..routes import health, persons, users


class AppWrapper:
    app: Quart

    def __init__(self, test_config: Optional[Config] = None):
        self.app = Quart(__name__)
        self._configs(test_config)

        # blueprints
        self.app.register_blueprint(health.bp, url_prefix="/health")
        self.app.register_blueprint(users.bp, url_prefix="/users")
        self.app.register_blueprint(persons.bp, url_prefix="/persons")

    # load configs into quart app
    def _configs(self, config: Optional[Config] = None) -> None:
        if config is not None:
            self.app.config.from_object(config)

        else:
            new_config = AppConfig()
            self.app.config.from_object(new_config)

    def add_endpoint(
        self,
        endpoint: List[str] = None,
        endpoint_name: str = None,
        handler: Optional[RouteCallable] = None,
        methods: Optional[Sequence[str]] = ["GET"],
        *args,
        **kwargs,
    ) -> None:
        self.app.add_url_rule(
            rule=endpoint_name,
            endpoint=endpoint,
            view_func=handler,
            **kwargs,
        )

    def run(self, **kwargs) -> None:
        self.app.run(**kwargs)
