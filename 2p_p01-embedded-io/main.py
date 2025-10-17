import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import RPi.GPIO as GPIO
import time

from servo_control import set_servo_angle

SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0) 

try:
    print("Iniciando secuencia del servomotor. Presiona CTRL+C para detener.")
    while True:
        print("Moviendo a 90 grados...")
        set_servo_angle(90, pwm)
        time.sleep(3)
        print("Moviendo a -90 grados...")
        set_servo_angle(-90, pwm)
        time.sleep(3)

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    pwm.stop()          
    GPIO.cleanup()      
    print("GPIO limpiado y programa finalizado.")