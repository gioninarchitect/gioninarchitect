from flask import Blueprint, request, jsonify
from ..models import Order, Product
from .. import db

order_bp = Blueprint('orders', __name__)

@order_bp.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@order_bp.route('/api/orders/create', methods=['POST'])
def create_order():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if not product_id or not quantity:
        return jsonify({'error': 'Missing product_id or quantity'}), 400
        
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
        
    if product.current_inventory < quantity:
        return jsonify({
            'error': 'Insufficient stock',
            'available': product.current_inventory
        }), 400
        
    # Create new order
    order = Order(
        product_id=product_id,
        quantity=quantity,
        status='Pending'
    )
    
    # Update inventory
    product.current_inventory -= quantity
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order.to_dict()
    })

@order_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.to_dict())

@order_bp.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Missing status'}), 400
        
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
        
    order.status = status
    db.session.commit()
    
    return jsonify({
        'message': 'Order status updated',
        'order': order.to_dict()
    })
