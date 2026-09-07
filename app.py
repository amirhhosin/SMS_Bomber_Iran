from flask import Flask, request, jsonify, render_template
import subprocess
import json
import sys
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/send', methods=['POST'])
def send_sms():
    try:
        data = request.get_json()
        phone = data.get('phone')
        count = data.get('count', 1)
        threads = data.get('threads', 10)

        if not phone:
            return jsonify({"error": "Phone number is required"}), 400

        result = subprocess.run(
            [sys.executable, 'main.py', phone, str(count), str(threads)],
            capture_output=True,
            text=True,
            timeout=60
        )

        return jsonify({
            "status": "success",
            "phone": phone,
            "count": count,
            "threads": threads,
            "output": result.stdout,
            "error": result.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Operation timed out"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
