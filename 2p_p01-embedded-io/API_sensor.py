from flask import Flask, jsonify
import json
import time
from datetime import datetime

app = Flask(__name__)

# Datos de ejemplo (pueden venir de tu sensor)
datos_sensor = {
    "temperatura": 25.5,
    "humedad": 60,
    "estado": "activo",
    "ultima_actualizacion": datetime.now().isoformat()
}

@app.route('/')
def home():
    return jsonify({"mensaje": "API del Sensor", "endpoints": ["/api/sensor", "/api/estado"]})

@app.route('/api/sensor')
def get_sensor_data():
    # Actualizar timestamp
    datos_sensor["ultima_actualizacion"] = datetime.now().isoformat()
    return jsonify(datos_sensor)

@app.route('/api/estado')
def get_status():
    return jsonify({"estado": "sistema funcionando", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)