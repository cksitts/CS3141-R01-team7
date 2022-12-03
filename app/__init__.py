from flask import Flask
import os

def create_app(config_class):
    # define the flask instance and load the config file
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = os.environ.get('SECRET_KEY')


    with app.app_context():
        #import routes.py
        from . import routes

        # Register blueprints
        app.register_blueprint(routes.error)
        app.register_blueprint(routes.user)
        app.register_blueprint(routes.footer)
        app.register_blueprint(routes.main)

        return app

    
