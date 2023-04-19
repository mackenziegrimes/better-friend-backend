from flask import Flask, Config, logging

from .config import AppConfig
from .health import bp as health_bp
from .persons import bp as persons_bp

def create_app(test_config: Config = AppConfig()):
        app = Flask(__name__)
        app.config.from_object(test_config)
        
        app.register_blueprint(health_bp)
        app.register_blueprint(persons_bp, url_prefix="/persons")
    
        return app
        

if __name__ == "__main__":
    config = AppConfig()
    app = create_app(test_config=config)
    app.run(host="0.0.0.0", port=config.PORT)
