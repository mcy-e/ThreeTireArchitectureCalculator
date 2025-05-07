from .db import add_calculation_to_history
from flask import Blueprint, request, jsonify, session
from .authentication import login_required
from .calculator import calculate_derivative,calculate_integral,calculate_limit,solve_equation,apply_function
bp = Blueprint('routes', __name__)

@bp.route('/calculate', methods=['POST'])
@login_required
def calculate():
    data = request.get_json()
    expr = data.get('expression')
    operation = data.get('operation')
    username = session.get('username')
    user_id = session.get('user_id')  # Get user_id from session

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

        # Add to user history using database function
        add_calculation_to_history(user_id, operation, expr, str(result))
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
