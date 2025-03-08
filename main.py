from flask import Flask, request, jsonify
from sympy import symbols, solve, diff, integrate, limit, sin, Eq

app = Flask(__name__)

# Define x as a symbol globally
x = symbols('x')

@app.route('/solve', methods=['POST'])
def solve_math():
    try:
        data = request.get_json()
        equation = data.get("equation")

        # Check if the equation is provided
        if not equation:
            return jsonify({"error": "No equation provided"}), 400

        # Handle differentiation
        if equation.startswith("diff"):
            expr = equation.replace("diff(", "").replace(")", "")
            expr = eval(expr, {"x": x})  # Safely evaluate with SymPy
            result = str(diff(expr, x))

        # Handle integration
        elif equation.startswith("integrate"):
            expr = equation.replace("integrate(", "").replace(")", "")
            expr = eval(expr, {"x": x})
            result = str(integrate(expr, x))

        # Handle limits
        elif equation.startswith("limit"):
            expr = equation.replace("limit(", "").replace(")", "")
            func, var, val = expr.split(",")
            func = eval(func, {"x": x})
            val = eval(val)
            result = str(limit(func, x, val))

        # Handle algebraic solving
        elif equation.startswith("solve"):
            expr = equation.replace("solve(", "").replace(")", "")
            lhs, rhs = expr.split("=")
            lhs = eval(lhs, {"x": x})
            rhs = eval(rhs, {"x": x})
            result = str(solve(Eq(lhs, rhs), x))

        else:
            return jsonify({"error": "Unsupported operation"}), 400

        return jsonify({"solution": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
