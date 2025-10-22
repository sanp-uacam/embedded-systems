from flask import Flask, jsonify
import json
import time
from datetime import datetime

app = Flask(__name__)

# Datos de ejemplo (pueden venir de tu sensor)
datos_potenciometro = {
    "Valor crudo": 1000,
    "porcentaje (%)": 20,
    "resistance_approx": "10KΩ",
}

@app.route('/')
def home():
    return jsonify({"mensaje": "API del Sensor", "endpoints": ["/api/sensor", "/api/estado"]})

@app.route('/api/sensor')
def get_sensor_data():
    # Actualizar timestamp
    datos_potenciometro["ultima_actualizacion"] = datetime.now().isoformat()
    return jsonify(datos_potenciometro)

@app.route('/api/estado')
def get_status():
    return jsonify({"estado": "sistema funcionando", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)