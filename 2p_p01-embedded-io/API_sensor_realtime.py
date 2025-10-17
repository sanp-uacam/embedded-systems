from flask import Flask, jsonify
import Adafruit_DHT
import time
from datetime import datetime

app = Flask(__name__)

# Configuración sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def leer_sensor():
    """Leer datos del sensor DHT11"""
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

@app.route('/')
def index():
    return """
    <h1>API Sensor DHT11</h1>
    <ul>
        <li><a href="/api/sensor">/api/sensor</a> - Datos actuales</li>
        <li><a href="/api/historial">/api/historial</a> - Últimas lecturas</li>
    </ul>
    """

@app.route('/api/sensor')
def api_sensor():
    temperature, humidity = leer_sensor()
    
    if humidity is not None and temperature is not None:
        datos = {
            "sensor": "DHT11",
            "temperatura": temperature,
            "humedad": humidity,
            "unidad_temperatura": "Celsius",
            "unidad_humedad": "%",
            "timestamp": datetime.now().isoformat(),
            "estado": "exitoso"
        }
    else:
        datos = {
            "sensor": "DHT11",
            "error": "No se pudo leer el sensor",
            "timestamp": datetime.now().isoformat(),
            "estado": "error"
        }
    
    return jsonify(datos)

@app.route('/api/historial')
def api_historial():
    # Simular historial (en un caso real leerías de una base de datos)
    historial = [
        {"temperatura": 24.5, "humedad": 58, "timestamp": "2024-01-15T10:30:00"},
        {"temperatura": 25.1, "humedad": 62, "timestamp": "2024-01-15T10:35:00"},
        {"temperatura": 24.8, "humedad": 59, "timestamp": "2024-01-15T10:40:00"}
    ]
    return jsonify({"lecturas": historial, "total": len(historial)})

if __name__ == '__main__':
    print("Servidor API iniciado en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)