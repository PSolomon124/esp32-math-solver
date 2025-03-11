from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Setting the port dynamically from the environment variable or defaulting to 3000
port = int(os.getenv("PORT", 5000))

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

@app.route("/api/math", methods=["POST"])
def math():
    try:
        data = request.json
        expression = data.get("expression")
        if not expression:
            return jsonify({"error": "No mathematical expression provided"}), 400
        
        # Example of simple evaluation (you can replace this with your math logic)
        result = eval(expression)  # Note: Be cautious with eval in production
        return jsonify({"expression": expression, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name_ == "__main__":
    # Running the server on 0.0.0.0 to be accessible from Railway
    app.run(host="0.0.0.0", port=port)
