from flask import Flask

from .config import Config
from .health import bp as health_bp
from .persons import bp as persons_bp

def create_app(test_config: Config = Config):
        app = Flask(__name__)
        app.config.from_object(test_config)
        
        app.logger.info(f"Loaded config: {str(test_config)}")
        app.register_blueprint(health_bp)
        app.register_blueprint(persons_bp, url_prefix="/persons")
    
        return app
        

if __name__ == "__main__":
    app = create_app()
    # app.logger.info(f"Loaded config: {str(config)}")
    app.run(host="0.0.0.0", port=config.PORT)
