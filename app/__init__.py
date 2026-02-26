from flask import Flask
from app.routes.sales_routes import sales_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(sales_bp, url_prefix="/api")

    return app
