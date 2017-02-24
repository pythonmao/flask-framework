from bmc.api.v1 import server


def register_blueprints(app, url_prefix):
    """Register the endpoints with a Flask application

    This function will take a Flask application object and register all
    the v2 endpoints. Register blueprints here when adding new endpoint
    modules.

    :param app: A Flask application object to register blueprints on
    :param url_prefix: The url prefix for the blueprints
    """
    app.register_blueprint(server.rest, url_prefix=url_prefix)