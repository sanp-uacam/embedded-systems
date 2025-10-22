
import RPi.GPIO as GPIO
import time

# Configuración

def read_potentiometer(POT_PIN):
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

# Calibrar para potenciómetro de 5K
def calibrate(POT_PIN):
    print("Calibrando para potenciómetro 5K...")
    print("Gira completamente a la izquierda (mínimo)")
    time.sleep(3)
    min_val = read_potentiometer(POT_PIN)
    
    print("Gira completamente a la derecha (máximo)")
    time.sleep(3)
    max_val = read_potentiometer(POT_PIN)
    
    print(f"Calibración: Mínimo={min_val}, Máximo={max_val}")
    return min_val, max_val

def get_pot_data(min_value, max_value,POT_PIN):
    try:
        # Calibrar
        min_value, max_value = calibrate()
        
        print("Leyendo potenciómetro de 5K... (Ctrl+C para detener)")
        while True:
            value = read_potentiometer(POT_PIN)
            
            # Normalizar el valor para potenciómetro de 5K
            if max_value - min_value > 0:
                normalized = (value - min_value) / (max_value - min_value) * 100.0
                normalized = max(0, min(100, normalized))  # Limitar entre 0-100%
            else:
                normalized = 50  # Valor por defecto
                
            # También calcular resistencia aproximada
            resistance_approx = (value / max_value) * 5000  # Aproximación para 5K
            
            print(f"Valor crudo: {value:4d} -> {normalized:5.1f}% -> ~{resistance_approx:4.0f}Ω")
            
            return (value,normalized, resistance_approx)

    except KeyboardInterrupt:
        print("\nDetenido por el usuario")
    finally:
        GPIO.cleanup()
