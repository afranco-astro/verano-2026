import json  # nos ayuda para trabajar con el json convertir el de python a jason o al reves
from random import uniform, choice, randint # nos ayuda para crear números aleatorios, variables y angulos aleatorios
import time # muestra el tiempo 

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "oan/dome"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
state = ["tracking", "parked", "slewing"]
cupula = [True, False] 

while True: # se utiliza mucho el true para hacer ciclos infinito
    
    estado_aleatorio = choice(cupula)
    
    if estado_aleatorio == True:
        texto_cupula = "abierto"
    else:
        texto_cupula = "cerrado"
    
    cupula_data = {
            "Azimuth": round(uniform(0.0, 360.0), 1),
            "isOpen": texto_cupula, 
            "Status": choice(state)
    }
    payload = json.dumps(cupula_data) # te ayuda a transformar a Json
    
    client.publish(
        topic=TOPIC,
        payload=payload,
        qos=0,
        retain=False
    )
    
    print(f"Enviado a {TOPIC}") 
    print(payload) 
    time.sleep(3) 