# Importar las bibliotecas necesarias
from geopy.geocoders import Nominatim
from geopy.distance import distance

# Función para calcular la distancia y duración del viaje
def calcular_distancia_duracion(ciudad_origen, ciudad_destino, medio_transporte):
    # Geocodificar las ciudades
    geolocator = Nominatim(user_agent="distance_calculator")
    location_origen = geolocator.geocode(ciudad_origen)
    location_destino = geolocator.geocode(ciudad_destino)

    # Verificar si las ciudades fueron encontradas
    if not location_origen:
        return "Ciudad de origen no encontrada."
    if not location_destino:
        return "Ciudad de destino no encontrada."

    # Calcular la distancia entre las ciudades
    dist = distance((location_origen.latitude, location_origen.longitude),
                    (location_destino.latitude, location_destino.longitude))

    # Definir la velocidad promedio según el medio de transporte
    if medio_transporte.lower() == 'avion':
        velocidad_promedio_kmh = 800  # Velocidad promedio de un avión comercial
    elif medio_transporte.lower() == 'auto':
        velocidad_promedio_kmh = 100  # Velocidad promedio de un automóvil
    elif medio_transporte.lower() == 'bus':
        velocidad_promedio_kmh = 80   # Velocidad promedio de un autobús
    else:
        return "Medio de transporte no válido."

    # Calcular la duración del viaje en horas
    duracion_horas = dist.km / velocidad_promedio_kmh

    # Mostrar la distancia y la duración del viaje en diferentes unidades
    resultado = f"La distancia entre {ciudad_origen} y {ciudad_destino} es de:\n"
    resultado += f"- Millas: {dist.miles:.2f}\n"
    resultado += f"- Kilómetros: {dist.km:.2f}\n"
    resultado += f"La duración del viaje en {medio_transporte} sería aproximadamente de {duracion_horas:.2f} horas.\n"

    # Narrativa del viaje
    resultado += f"Un viaje desde {ciudad_origen} hasta {ciudad_destino} en {medio_transporte}."

    return resultado

# Programa principal
if __name__ == "__main__":
    while True:
        # Solicitar ciudad de origen y destino
        ciudad_origen = input("Ingrese la ciudad de origen (en español): ")
        if ciudad_origen.lower() == 's':
            break  # Salir si se ingresa 's'
        
        ciudad_destino = input("Ingrese la ciudad de destino (en español): ")
        if ciudad_destino.lower() == 's':
            break  # Salir si se ingresa 's'

        # Solicitar medio de transporte
        medio_transporte = input("Ingrese el medio de transporte (avion/auto/bus): ")

        # Calcular y mostrar resultados
        resultado = calcular_distancia_duracion(ciudad_origen, ciudad_destino, medio_transporte)
        print(resultado)
        print()  # Línea en blanco para separar resultados

    print("¡Gracias por usar el servicio de cálculo de distancias y duración de viaje!")

