import json  #nos ayuda para trabajar con el json convertir el de python a jason o al reves
import random #nos ayuda para crear números aleatorios 
import time #

import paho.mqtt.client as mqtt

BROKER= "localhost"
PORT= 1883
TOPIC= "oan/weather"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

while True: #se utiliza mucho el true para hacer ciclos infinito
    weather_data = {
            "temperature": {
                "value": round(random.uniform(10.0, 25.0), 1),
                "unit": "C"
            },
            "humidity": random.randint(20, 80),
            "windSpeed": round(random.uniform(0.0, 15.0), 1),
            "pressure": round(random.uniform(990.0, 1025.0), 1),
            "dewPoint": round(random.uniform(0.0, 15.0), 1)
    }
    payload = json.dumps(weather_data) #te ayuda a transformar a Json

    client.publish(
        topic=TOPIC,
        payload=payload,
        qos=0,
        retain=False
    )
    print(payload)

    time.sleep(1) #aqui nos indica cuanto tiempo se utiliza para pubicar el proximo mensaje

