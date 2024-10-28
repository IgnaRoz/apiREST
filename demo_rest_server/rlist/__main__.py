#!/usr/bin/env python3

from flask import Flask

import rlist.blueprints
import rlist.service


def create_app():
    app = Flask(__name__)
    service = rlist.service.ListService()
    app.config['service'] = service
    app.register_blueprint(rlist.blueprints.api)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
