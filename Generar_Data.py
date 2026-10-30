import csv
import random
from datetime import datetime, timedelta

ciudades = ['Bogota', 'Medellin', 'Cali', 'Barranquilla', 'Bucaramanga']
estaciones = ['Norte', 'Sur', 'Centro', 'Oriente', 'Occidente']

with open('datos_contaminacion.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Fecha', 'Ciudad', 'Estacion', 'PM25', 'CO2', 'Temperatura'])
    
    fecha_base = datetime(2026, 1, 1)
    for i in range(1, 10001):
        fecha = fecha_base + timedelta(minutes=random.randint(1, 50000))
        # Introducción intencional de nulos para la etapa de limpieza
        pm25 = round(random.uniform(5.0, 75.0), 2) if random.random() > 0.05 else ""
        co2 = round(random.uniform(300.0, 600.0), 2)
        temp = round(random.uniform(12.0, 32.0), 1)
        writer.writerow([i, fecha.strftime('%Y-%m-%d %H:%M:%S'), random.choice(ciudades), random.choice(estaciones), pm25, co2, temp])

print("Dataset creado exitosamente")
