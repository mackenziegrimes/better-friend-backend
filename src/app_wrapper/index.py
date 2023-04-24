from flask import Flask, Config, logging
from flask.typing import RouteCallable
from typing import Sequence, Optional


class AppWrapper:
    app: Flask

    def __init__(self, test_config: Optional[Config] = None):
        self.app = Flask(__name__)
        self._configs(test_config)

    # load configs into flask app
    def _configs(self, config: Optional[Config] = None) -> None:
        print(f"Received config {config}")
        if config is None:
            self.app.config.from_file("../.env")

        for config, value in config:
            self.app.config[config.upper()] = value

    def add_endpoint(
        self,
        endpoint: [str] = None,
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
