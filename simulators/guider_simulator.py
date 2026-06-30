import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883
TOPIC  = "oan/guider"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

guiding     = False
star_locked = False
corrections = 0
lock_timer  = 6
pause_timer = 0

while True:
    if lock_timer > 0:
        lock_timer -= 1
        if lock_timer == 0:
            star_locked = True
            guiding     = True
        rms_ra  = 0.0
        rms_dec = 0.0

    elif pause_timer > 0:
        pause_timer -= 1
        guiding = False
        rms_ra  = 0.0
        rms_dec = 0.0
        if pause_timer == 0:
            guiding = True

    else:
        guiding = True
        rms_ra  = round(random.uniform(0.15, 0.65), 2)
        rms_dec = round(random.uniform(0.12, 0.55), 2)
        corrections += random.randint(1, 3)

        if random.random() < 0.06:
            pause_timer = 3
            guiding     = False

    payload = json.dumps({
        "rmsRA":       rms_ra,
        "rmsDec":      rms_dec,
        "guiding":     guiding,
        "starLocked":  star_locked,
        "corrections": corrections
    })

    client.publish(TOPIC, payload, qos=0, retain=False)
    print(payload)
    time.sleep(1)