from flask import Blueprint, request, jsonify
from ..models import Product
from .. import db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/api/inventory/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@inventory_bp.route('/api/inventory/search', methods=['POST'])
def search_products():
    data = request.json
    keyword = data.get('keyword', '').lower()
    category = data.get('category')
    subcategory = data.get('subcategory')
    
    query = Product.query.filter(
        Product.name.ilike(f'%{keyword}%'),
        Product.category == category if category else True,
        Product.subcategory == subcategory if subcategory else True
    )
    
    products = query.all()
    return jsonify([product.to_dict() for product in products])

@inventory_bp.route('/api/inventory/update', methods=['POST'])
def update_stock():
    data = request.json
    product_id = data.get('product_id')
    new_stock = data.get('stock')
    
    if not product_id or new_stock is None:
        return jsonify({'error': 'Missing product_id or stock'}), 400
        
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
        
    product.current_inventory = new_stock
    db.session.commit()
    
    return jsonify({
        'message': 'Stock updated successfully',
        'product': product.to_dict()
    })
