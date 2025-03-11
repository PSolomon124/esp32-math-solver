from flask import Flask, request, jsonify
from sympy import sympify, simplify

app = Flask(__name__)

# Defaulting to port 5000 directly
port = 3000

@app.route("/", methods=["GET"])
def home():
    return "Hello, Railway! Your server is up and running."

@app.route("/api/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        return jsonify({"message": "GET request received"})
    elif request.method == "POST":
        data = request.json  # Get JSON data from the POST request
        return jsonify({"message": "POST request received", "data": data})

@app.route("/api/math", methods=["GET", "POST"])
def math():
    if request.method == "GET":
        return jsonify({"message": "Use POST to send a mathematical expression."})

    try:
        data = request.json
        expression = data.get("expression")
        if not expression:
            return jsonify({"error": "No mathematical expression provided"}), 400
        
        # Use SymPy to evaluate and simplify the expression
        expr = sympify(expression)
        result = simplify(expr)
        return jsonify({"expression": str(expression), "result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Running the server on 0.0.0.0 to be accessible from Railway
    app.run(host="0.0.0.0", port=port)
