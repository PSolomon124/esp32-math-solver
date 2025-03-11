import sympy as sp
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def differentiate(expression):
    x = sp.symbols('x')
    expr = sp.sympify(expression)
    derivative = sp.diff(expr, x)
    steps = sp.pretty(sp.diff(expr, x, evaluate=False))
    return str(derivative), steps

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    expression = data.get('expression', '')
    if not expression:
        return jsonify({'error': 'No expression provided'}), 400
    
    try:
        result, steps = differentiate(expression)
        return jsonify({'result': result, 'steps': steps})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
