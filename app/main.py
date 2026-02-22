from flask import Flask, request, jsonify
from model import load_model
import logging
import boto3

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
model = load_model()

# CloudWatch client for custom metrics
cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')

def log_5xx_error():
    cloudwatch.put_metric_data(
        Namespace='AnalyticsApp',
        MetricData=[{
            'MetricName': 'HTTP5xxErrors',
            'Value': 1,
            'Unit': 'Count'
        }]
    )

@app.route('/health')
def health(): return jsonify({'status': 'healthy'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['features']
    prediction = model.predict([data])[0]
    app.logger.info(f'Prediction: {prediction}')
    return jsonify({'prediction': int(prediction)})

# This catches all 500 errors and logs to CloudWatch
@app.errorhandler(500)
def handle_500(e):
    log_5xx_error()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
