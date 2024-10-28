#!/usr/bin/env python3

from flask import Flask

import sample.blueprints
from sample.service import Service


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['service'] = Service()
    app.register_blueprint(sample.blueprints.sample_api)
    return app


if __name__ == '__main__':
    create_app().run()
