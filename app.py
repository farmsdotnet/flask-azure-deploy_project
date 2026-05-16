from flask import Flask, render_template, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/api/hello', methods=['GET'])
def api_hello():
    """Simple API endpoint."""
    return jsonify({'message': 'Hello from Flask API!'})

@app.route('/health')
def health_check():
    """Health check endpoint for deployment."""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
