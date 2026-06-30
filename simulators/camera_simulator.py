import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883
TOPIC  = "oan/camera"

FILTERS        = ["U", "B", "V", "R", "I"] #filtros que utiliza
EXPOSURE_STEPS = 15 #tiempo de exposición de la foto
READOUT_STEPS  = 3 #tiempo de descarga

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

status    = "cooling" #la cámara inicia en estado e enfriamiento
temp      = 15.0 #la temperatura inicial 
target_t  = -25.0 #temperatura optima que debe alcanzar
cooler    = 0 #petencia del enfriador con la que inicia
filter_i  = 2 #nos indic en que filtro inicia la cámara 
progress  = 0 #proceso de la exposición 
readout_t = 0 #proceso de la descarga

while True:
    if temp > target_t + 0.5:
        cooler = min(100, int((temp - target_t) * 3 + 40))
        temp   = round(temp - random.uniform(0.3, 0.8), 1)
    else:
        cooler = int(75 + random.uniform(-5, 5))
        temp   = round(target_t + random.uniform(-0.3, 0.3), 1)

    if status == "cooling" and temp <= target_t + 1.0:
        status = "idle"

    elif status == "idle":
        filter_i = (filter_i + 1) % len(FILTERS)
        progress = 0
        status   = "exposing"

    elif status == "exposing":
        progress = min(100, progress + round(100 / EXPOSURE_STEPS))
        if progress >= 100:
            status    = "readout"
            readout_t = READOUT_STEPS

    elif status == "readout":
        readout_t -= 1
        if readout_t <= 0:
            status = "idle"

    payload = json.dumps({
        "temperature":      temp,
        "coolerPower":      cooler,
        "exposing":         status == "exposing",
        "exposureProgress": progress if status == "exposing" else 0,
        "filter":           FILTERS[filter_i],
        "status":           status
    })

    client.publish(TOPIC, payload, qos=0, retain=False)
    print(payload)
    time.sleep(1)