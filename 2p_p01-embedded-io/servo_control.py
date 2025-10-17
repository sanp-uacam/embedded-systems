
import time

def set_servo_angle(angle, pwm):
    duty = 2.5 + (angle + 90) / 180 * 10
    pwm.ChangeDutyCycle(duty)   
    time.sleep(0.5) 
    pwm.ChangeDutyCycle(0)


# try:
#     print("Iniciando secuencia del servomotor. Presiona CTRL+C para detener.")
#     while True:
#         print("Moviendo a 90 grados...")
#         set_servo_angle(90)
#         time.sleep(3)
#         print("Moviendo a -90 grados...")
#         set_servo_angle(-90)
#         time.sleep(3)

# except KeyboardInterrupt:
#     print("Programa detenido por el usuario.")

# finally:
#     pwm.stop()          
#     GPIO.cleanup()      
#     print("GPIO limpiado y programa finalizado.")