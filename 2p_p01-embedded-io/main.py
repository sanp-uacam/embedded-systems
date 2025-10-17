import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import RPi.GPIO as GPIO
import time
from servo_control import set_servo_angle

SERVO_PIN = 18
pwm = None

def setup():
    global pwm
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0) 

def loop():
    print("Moviendo a 90 grados...")
    set_servo_angle(90, pwm)
    time.sleep(3)
    print("Moviendo a -90 grados...")
    set_servo_angle(-90, pwm)
    time.sleep(3)
    
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