from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


# setup database
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    __table_args__ = {'schema':'rbac'}

db = SQLAlchemy(model_class=Base)


# initialise app
def create_app(config_name):
    # init with config
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    # ssl
    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        SSLify(app)

    # api
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # cli scripts
    if config_name in ['dev', 'test', 'default']:
        from .scripts import scripts as scripts_blueprint
        app.register_blueprint(scripts_blueprint)

    return app
