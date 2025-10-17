import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from servo_control import set_servo_angle

DHT11_PIN = 17      # GPIO para DHT11 (pin 11)
DHT_SENSOR = Adafruit_DHT.DHT11
SERVO_PIN = 18
pwm = None

def read_dht11():
    """Lee los datos del sensor DHT11"""
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT11_PIN)
    
    if humidity is not None and temperature is not None:
        print(f"Temp: {temperature:.1f}°C  Humedad: {humidity:.1f}%")
        return temperature, humidity
    else:
        print("Error leyendo sensor DHT11")
        return None, None

def setup():
    global pwm
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0) 

def loop():
    read_dht11()
    time.sleep(2)
    
    # print("Moviendo a 90 grados...")
    # set_servo_angle(90, pwm)
    # time.sleep(3)
    # print("Moviendo a -90 grados...")
    # set_servo_angle(-90, pwm)
    # time.sleep(3)
    
def cleanup():
    global pwm
    
    if pwm:
        pwm.stop()
    GPIO.cleanup()
    
if __name__ == "__main__": 
    
    setup()
    
    try:
        while True:
            loop()
            
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")

    finally:         
        cleanup()      