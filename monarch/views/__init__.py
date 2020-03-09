from .internal import bp as internal_bp


def register_internal_app(app):
    app.register_blueprint(internal_bp)
