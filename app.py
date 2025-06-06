from flask import Flask, jsonify
import random
import time
from prometheus_client import start_http_server, Counter, Gauge

app = Flask(__name__)

# Метрики Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP Errors')
RESPONSE_TIME = Gauge('http_response_time_seconds', 'Response Time in Seconds')

@app.route('/')
def home():
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    # Имитация работы
    time.sleep(random.uniform(0.1, 0.5))
    
    # 10% ошибок
    if random.random() < 0.1:
        ERROR_COUNT.inc()
        return jsonify({"status": "error"}), 500
    
    resp_time = time.time() - start_time
    RESPONSE_TIME.set(resp_time)
    return jsonify({"status": "ok", "response_time": f"{resp_time:.3f}s"})

@app.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    return generate_latest()

if __name__ == '__main__':
    start_http_server(8000)  # Метрики на порту 8000
    app.run(host='0.0.0.0', port=5000)
