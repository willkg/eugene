from types import ModuleType, FunctionType

from flask import Flask

from eugene.errors import register_error_handlers


def create_app(settings):
    """Create a new Flask application"""
    app = Flask(__name__)

    # Import settings from file
    for name in dir(settings):
        value = getattr(settings, name)
        if not (name.startswith('_') or isinstance(value, ModuleType)
                or isinstance(value, FunctionType)):
            app.config[name] = value

    # Register blueprints (i.e. all our apps)
    for blueprint in app.config.get('BLUEPRINTS', []):
        app.register_blueprint(
            getattr(__import__('%s.views' % blueprint,
                               fromlist=['blueprint']),
                    'blueprint'))

    # Register error handlers
    register_error_handlers(app)

    @app.context_processor
    def context_processor():
        return dict(config=app.config)

    @app.teardown_request
    def teardown_request(arg):
        # Remove the database session if it exists
        if hasattr(app, 'db_session'):
            app.db_session.close()

    return app
