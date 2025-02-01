from flask import Flask
from .routes import inventory_routes, order_routes

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(inventory_routes.inventory_bp)
    app.register_blueprint(order_routes.order_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
