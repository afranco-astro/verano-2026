import json  #nos ayuda para trabajar con el json convertir el de python a jason o al reves
from random import uniform, choice, randint #nos ayuda para crear números aleatorios, variables y angulos aleatorios
import time #muestra el tiempo 

import paho.mqtt.client as mqtt

BROKER= "localhost"
PORT= 1883
TOPIC= ["oan/weather"]
unidades = ["C", "F", "K"]


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

while True: #se utiliza mucho el true para hacer ciclos infinito
    weather_data = {
            "temperature": {
                "value": round(uniform(10.0, 38.0), 1),
                "unit":choice(unidades),
            },
            "rainRate": round(uniform(10.0, 25.0), 1),
            "cloudCover":round(uniform(10.0, 100.0), 1),
            "humidity": randint(20, 80),
            "windSpeed": round(uniform(0.0, 15.0), 1),
            "pressure": round(uniform(990.0, 1025.0), 1),
            "dewPoint": {
                "value2": round(uniform(10.0, 25.0), 1),
                "unit2":choice(unidades),
            }
    }
    payload = json.dumps(weather_data) #te ayuda a transformar a Json

    topico_aleatorio = choice(TOPIC)

    client.publish(
        topic=topico_aleatorio,
        payload=payload,
        qos=0,
        retain=False
    )
    
    print(f"Enviado a {topico_aleatorio}") #Imprimimos en consola a qué tópico se envió para poder rastrearlo bien
    print(payload)
    time.sleep(3) #aqui nos indica cuanto tiempo se utiliza para pubicar el proximo mensaje

