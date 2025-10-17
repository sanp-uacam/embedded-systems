import requests
import json

# Leer API simple
def leer_api_simple(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza error si hay problema HTTP
        
        datos = respuesta.json()
        return datos
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

# Uso
url = "http://localhost:8000/api/sensor"
datos = leer_api_simple(url)

if datos:
    print("Datos recibidos:")
    print(json.dumps(datos, indent=2))