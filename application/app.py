# -*- coding: utf-8 -*-

from flask import Flask
from .controllers import blueprints
from .configs import config
from .extensions import db


def create_app(config_name=None, config_overrides=None):
    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if config_overrides:
        app.config.update(config_overrides)

    # db
    db.init_app(app)

    # blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
