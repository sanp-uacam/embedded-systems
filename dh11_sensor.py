import time
import RPi.GPIO as GPIO

def read_dht11(pin):
    """Lectura simple del DHT11"""
    try:
        # Inicializar comunicación
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.018)
        GPIO.output(pin, GPIO.HIGH)
        
        # Cambiar a entrada
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Esperar respuesta del sensor
        count = 0
        while GPIO.input(pin) == GPIO.LOW:
            count += 1
            if count > 1000:
                return None, None
        
        count = 0
        while GPIO.input(pin) == GPIO.HIGH:
            count += 1
            if count > 1000:
                return None, None
        
        # Leer datos (simplificado)
        data = []
        for i in range(40):
            count = 0
            while GPIO.input(pin) == GPIO.LOW:
                count += 1
                if count > 100:
                    break
            
            count = 0
            start = time.time()
            while GPIO.input(pin) == GPIO.HIGH:
                count += 1
                if count > 100:
                    break
            
            end = time.time()
            if (end - start) > 0.0001:  # Más de 100us = 1
                data.append(1)
            else:
                data.append(0)
        
        # Interpretar datos
        if len(data) >= 40:
            humidity = data[0:8]
            temperature = data[16:24]
            
            hum = sum([humidity[i] << (7-i) for i in range(8)])
            temp = sum([temperature[i] << (7-i) for i in range(8)])
            
            return temp, hum
        else:
            return None, None
            
    except Exception as e:
        return None, None

def main():
    GPIO.setmode(GPIO.BCM)
    DHT_PIN = 17
    
    print("Monitor DHT11 - Solo RPi.GPIO")
    print("GPIO: 17 - Ctrl+C para salir\n")
    
    try:
        while True:
            temp, hum = read_dht11(DHT_PIN)
            
            if temp is not None and hum is not None:
                print(f"Temperatura: {temp}°C, Humedad: {hum}%")
            else:
                print("Error en lectura")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()