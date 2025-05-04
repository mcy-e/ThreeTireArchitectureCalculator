# app/routes.py
from flask import Blueprint, request, jsonify, session
from .calculator import *
from .authentication import login_required, add_to_history

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/calculate', methods=['POST'])
@login_required
def calculate():
    data = request.get_json()
    expr = data.get('expression')
    operation = data.get('operation')
    username = session.get('username')

    try:
        result = None
        
        if operation == 'derivative':
            result = calculate_derivative(expr)
        elif operation == 'integral':
            result = calculate_integral(expr)
        elif operation == 'limit':
            x_val = data.get('x_value')
            result = calculate_limit(expr, float(x_val))
        elif operation == 'solve':
            result = solve_equation(expr)
        elif operation == 'function':
            result = apply_function(expr)
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        # Add to user history
        add_to_history(username, operation, expr, result)
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500