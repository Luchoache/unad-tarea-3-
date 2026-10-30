import time
import json
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

ciudades = ['Bogota', 'Medellin', 'Cali', 'Barranquilla', 'Bucaramanga']

while True:
    data = {
        "sensor_id": random.randint(1, 5),
        "ciudad": random.choice(ciudades),
        "pm25": round(random.uniform(5.0, 75.0), 2),
        "co2": round(random.uniform(300.0, 600.0), 2),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    producer.send('sensor_data', value=data)
    print(f"Sent: {data}")
    time.sleep(1)
