from flask import Flask, request, jsonify
import math

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

def numerical_integration(func, lower, upper, n):
    step = (upper - lower) / n
    total_area = 0.0

    for i in range(n):
        x = lower + i * step
        total_area += func(x) * step

    return total_area

def abs_sin(x):
    return abs(math.sin(x))

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.after_request
def after_request(response):
    # CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins (modify as needed)
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/numericalintegralservice/<lower>/<upper>', methods=['GET'])
def calculate_integral(lower, upper):
    print(f"Received request: lower={lower}, upper={upper}")
    try:
        # Convert lower and upper to float
        lower = float(lower)
        upper = float(upper)

        n = request.args.get('n', None)
       
        # if 'n' is provided, make sure it's a valid integer
        if n:
            try:
                n = int(n)
                if n <= 0:
                    return jsonify({"error": "'n' must be a positive integer."}), 400
            except ValueError:
                return jsonify({"error": "Invalid value for 'n'. It must be an integer."}), 400
           
            # calculate the integral for the given 'n'
            result = numerical_integration(abs_sin, lower, upper, n)
            return jsonify({
                "lower": lower,
                "upper": upper,
                "n": n,
                "integral": result
            })

        n_values = [10, 100, 1000, 10000, 100000, 1000000]
        results = []
        for n in n_values:
            result = numerical_integration(abs_sin, lower, upper, n)
            results.append({
                "n": n,
                "integral": result
            })
       
        return jsonify({
            "lower": lower,
            "upper": upper,
            "results": results
        })
   
    except Exception as e:
        return jsonify({"error": f"an error occurred: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)