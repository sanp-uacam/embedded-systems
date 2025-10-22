import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
import RPi.GPIO as GPIO
import time

import analog_in_potentiometer as pot_lib

app = Flask(__name__)

POT_PIN = 4
GPIO.setmode(GPIO.BCM)
min_value, max_value = 0,0
pot_json = {}

def setup():
    global min_value, max_value 
    min_value, max_value = pot_lib.calibrate(POT_PIN)
    
    app.run(host='0.0.0.0', port=8080, debug=True)
    
def loop():
    global min_value, max_value, pot_json
    value,normalized, resistance_approx = pot_lib.get_pot_data(min_value, max_value,POT_PIN)
    pot_json = {
        "value": value,
        "normalized": normalized,
        "resistance_approx": resistance_approx,
    }

if __name__ == "__main__":
    setup()
    
    # try:
    #     while True:
    #         loop()
            
    # except KeyboardInterrupt:
    #     print("Programa detenido por el usuario.")

@app.route('/')
def home():
    value,normalized, resistance_approx = pot_lib.get_pot_data(min_value, max_value,POT_PIN)
    pot_json = {
        "value": value,
        "normalized": normalized,
        "resistance_approx": resistance_approx,
    }
    return jsonify(pot_json)
    # return jsonify({"mensaje": "API del Sensor", "endpoints": ["/api/sensor", "/api/estado"]})

def read_potentiometer():
    # Medir tiempo de carga del capacitor
    count = 0
    
    # Descargar capacitor
    GPIO.setup(POT_PIN, GPIO.OUT)
    GPIO.output(POT_PIN, False)
    time.sleep(0.05)  # Reducido para potenciómetro de 5K
    
    # Cambiar a entrada y medir tiempo hasta que se cargue
    GPIO.setup(POT_PIN, GPIO.IN)
    
    # Contar hasta que el pin sea HIGH
    while GPIO.input(POT_PIN) == GPIO.LOW:
        count += 1
        if count > 50000:  # Timeout reducido para 5K
            break
    
    return count

