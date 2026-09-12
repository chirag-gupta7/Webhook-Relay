from flask import Flask
from app.config import Config
from app.extensions import db
from app.routes.webhooks import webhooks_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(webhooks_bp)
    @app.route('/')
    def index():
        return "Hello World!"
    return app
