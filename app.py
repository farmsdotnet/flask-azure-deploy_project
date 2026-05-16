from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/health')
def health():
    return {'status': 'healthy'}, 200


@app.route('/api/message')
def get_message():
    return {'message': 'Hello from Flask API!'}, 200


if __name__ == '__main__':
    debug_mode = app.config['ENV'] == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
