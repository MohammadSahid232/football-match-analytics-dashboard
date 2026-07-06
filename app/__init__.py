from flask import Flask

def create_app():
    """
    Application Factory for creating the Flask app instance.
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Import and register blueprints/routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
