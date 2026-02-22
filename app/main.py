from flask import Flask, request, jsonify
from model import load_model
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
model = load_model()

@app.route('/health')
def health(): return jsonify({'status': 'healthy'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['features']
    prediction = model.predict([data])[0]
    app.logger.info(f'Prediction: {prediction}')
    return jsonify({'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
