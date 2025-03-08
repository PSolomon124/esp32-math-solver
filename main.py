from flask import Flask, request, jsonify
from sympy import symbols, solve, diff, integrate, limit, Eq, sin

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_math():
    try:
        data = request.get_json()
        equation = data.get("equation")
        x = symbols('x')  # Define x as a symbol

        if equation.startswith("diff"):
            expr = equation.replace("diff(", "").replace(")", "")
            result = str(diff(eval(expr)))

        elif equation.startswith("integrate"):
            expr = equation.replace("integrate(", "").replace(")", "")
            result = str(integrate(eval(expr)))

        elif equation.startswith("limit"):
            expr = equation.replace("limit(", "").replace(")", "")
            result = str(limit(eval(expr), x, 0))

        elif equation.startswith("solve"):
            expr = equation.replace("solve(", "").replace(")", "")
            lhs, rhs = expr.split("=")
            result = str(solve(Eq(eval(lhs), eval(rhs)), x))

        else:
            return jsonify({"error": "Unsupported operation"}), 400

        return jsonify({"solution": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
