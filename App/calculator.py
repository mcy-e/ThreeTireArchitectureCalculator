from sympy import symbols, diff, integrate, limit, Eq, solve, sympify

x = symbols('x')

def calculate_derivative(expr_str):
    expr = sympify(expr_str)    #*make the string as a symbolic expression
    return str(diff(expr, x))

def calculate_integral(expr_str):
    expr = sympify(expr_str)
    return str(integrate(expr, x))

def calculate_limit(expr_str, x_val):
    expr = sympify(expr_str)
    return str(limit(expr, x, x_val))

def solve_equation(equation_str):
    left, right = equation_str.split('=')#*find the delimiter
    eq = Eq(sympify(left), sympify(right))#*make it symbolic equation
    solutions = solve(eq, x)
    return [str(sol) for sol in solutions]#*for more then one solution
