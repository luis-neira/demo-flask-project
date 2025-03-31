from flask import Flask


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    from resources import bp_rentals, bp_tenants, bp_root

    app.register_blueprint(bp_root)
    app.register_blueprint(bp_rentals, url_prefix="/rentals")
    app.register_blueprint(bp_tenants, url_prefix="/tenants")

    return app
