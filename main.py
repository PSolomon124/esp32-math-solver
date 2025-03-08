from flask import Flask, request, jsonify
import sympy as sp

app = Flask(_name_)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Railway API is running. Use /solve with POST method."})

@app.route("/solve", methods=["POST"])
def solve_equation():
    try:
        # Get JSON data from ESP32
        data = request.get_json()
        equation_str = data.get("equation", "")

        if not equation_str:
            return jsonify({"error": "No equation provided"}), 400

        # Convert equation string to SymPy expression
        x = sp.Symbol("x")
        try:
            equation = sp.sympify(equation_str)
        except Exception as e:
            return jsonify({"error": f"Invalid equation: {str(e)}"}), 400

        # Solve the equation based on the type of request
        if "diff" in equation_str:
            solution = sp.diff(equation, x)
        elif "integrate" in equation_str:
            solution = sp.integrate(equation, x)
        elif "limit" in equation_str:
            solution = sp.limit(equation, x, 0)
        elif "solve" in equation_str:
            solution = sp.solve(equation, x)
        else:
            return jsonify({"error": "Unknown operation"}), 400

        return jsonify({"solution": str(solution)})

    except Exception as e:
        return
