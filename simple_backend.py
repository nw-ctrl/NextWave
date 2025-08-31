from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'message': 'NextWave Backend is running!'
    })

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({
        'message': 'NextWave API is working!',
        'features': [
            'PDF Processing',
            'Image Analysis', 
            'Workflow Automation',
            'Admin Panel',
            'AI Vision'
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting NextWave Backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)
