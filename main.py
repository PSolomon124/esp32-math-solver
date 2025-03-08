from flask import Flask, request, jsonify
from sympy import symbols, Eq, solve, diff, integrate, factor, expand, apart, together, simplify, limit
from sympy.solvers import solveset
from sympy.series.sequences import RecursiveSeq
from sympy.series.fourier import fourier_series

app = Flask(__name__)

x, y, z = symbols("x y z")  # Define symbols for calculations

@app.route("/")
def home():
    return "Math Solver API is running!"

@app.route("/solve", methods=["POST"])
def solve_math():
    data = request.json
    operation = data.get("operation")

    try:
        if operation == "quadratic":
            a, b, c = data["a"], data["b"], data["c"]
            eq = Eq(a*x**2 + b*x + c, 0)
            solution = solve(eq, x)

        elif operation == "derivative":
            expr = data["expression"]
            derivative = diff(expr, x)

        elif operation == "integral":
            expr = data["expression"]
            integral = integrate(expr, x)

        elif operation == "factor":
            expr = data["expression"]
            result = factor(expr)

        elif operation == "expand":
            expr = data["expression"]
            result = expand(expr)

        elif operation == "simplify":
            expr = data["expression"]
            result = simplify(expr)

        elif operation == "partial_fraction":
            expr = data["expression"]
            result = apart(expr)

        elif operation == "combine_fractions":
            expr = data["expression"]
            result = together(expr)

        elif operation == "limit":
            expr = data["expression"]
            point = data["point"]
            result = limit(expr, x, point)

        elif operation == "equation_solver":
            expr = data["expression"]
            result = solveset(Eq(expr, 0), x)

        elif operation == "fourier_series":
            expr = data["expression"]
            terms = int(data.get("terms", 5))
            result = fourier_series(expr, (x, -3.14, 3.14)).truncate(terms)

        elif operation == "recursive_sequence":
            expr = data["expression"]
            result = RecursiveSeq(expr, x)

        elif operation == "matrix_operations":
            from sympy.matrices import Matrix
            matrix_data = data["matrix"]
            matrix = Matrix(matrix_data)
            result = {
                "determinant": matrix.det(),
                "inverse": matrix.inv() if matrix.det() != 0 else "Singular Matrix"
            }

        elif operation == "logarithm":
            from sympy import log
            base = data["base"]
            number = data["number"]
            result = log(number, base)

        elif operation == "trigonometry":
            from sympy import sin, cos, tan
            func = data["function"]
            angle = data["angle"]
            if func == "sin":
                result = sin(angle)
            elif func == "cos":
                result = cos(angle)
            elif func == "tan":
                result = tan(angle)
            else:
                return jsonify({"error": "Invalid trig function"})

        elif operation == "series_expansion":
            from sympy import series
            expr = data["expression"]
            order = data.get("order", 6)
            result = series(expr, x, n=order)

        elif operation == "definite_integral":
            expr = data["expression"]
            lower = data["lower"]
            upper = data["upper"]
            result = integrate(expr, (x, lower, upper))

        elif operation == "double_integral":
            expr = data["expression"]
            x_range = data["x_range"]
            y_range = data["y_range"]
            result = integrate(integrate(expr, (x, x_range[0], x_range[1])), (y, y_range[0], y_range[1]))

        elif operation == "summation":
            from sympy import summation
            expr = data["expression"]
            lower = data["lower"]
            upper = data["upper"]
            result = summation(expr, (x, lower, upper))

        elif operation == "product":
            from sympy import product
            expr = data["expression"]
            lower = data["lower"]
            upper = data["upper"]
            result = product(expr, (x, lower, upper))

        else:
            return jsonify({"error": "Invalid operation"})

        return jsonify({"operation": operation, "result": str(result)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
