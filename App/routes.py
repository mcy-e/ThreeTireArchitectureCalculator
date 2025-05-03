# app/routes.py
from flask import Blueprint, request, jsonify
from .calculator import *

bp = Blueprint('main', __name__)

@bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get('expression')
    operation = data.get('operation')

    try:
        if operation == 'derivative':
            result = calculate_derivative(expr)
        elif operation == 'integral':
            result = calculate_integral(expr)
        elif operation == 'limit':
            x_val = data.get('x_value')
            result = calculate_limit(expr, float(x_val))
        elif operation == 'solve':
            result = solve_equation(expr)
        elif operation =='function' :
            result = apply_function(expr)
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
