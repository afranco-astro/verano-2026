import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883
TOPIC  = "oan/mount"

TARGET_RA_H = 12.582   # 12h 34m 56s  — objeto que seguimos esta noche
TARGET_DEC  = 45.387   # +45° 23' 12" — Declinación fija durante la sesión
HA_LIMIT    = 5.5      # límite real del telescopio 2.1m OAN-SPM

def format_ra(hours): #convierte a horas formato
    h = int(hours)
    m = int((hours - h) * 60)
    s = ((hours - h) * 60 - m) * 60
    return f"{h:02d}h {m:02d}m {s:04.1f}s"

def format_dec(deg): #convierte a grados formato
    sign = "+" if deg >= 0 else "-"
    d = int(abs(deg))
    m = int((abs(deg) - d) * 60)
    s = ((abs(deg) - d) * 60 - m) * 60
    return f"{sign}{d:02d}° {m:02d}' {s:04.1f}\""

def format_ha(hours): 
    side = "E" if hours < 0 else "W"
    h = int(abs(hours))
    m = int((abs(hours) - h) * 60)
    s = ((abs(hours) - h) * 60 - m) * 60
    return f"{side} {h:02d}h {m:02d}m {s:04.1f}s"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
az         = 187.3
alt        = 62.4
ha         = -2.0      # empieza 2 horas al este del meridiano
slew_timer = 0

while True:
    # Tracking: az avanza, HA avanza a tasa sidérea real
    az  = (az + 0.05 + random.uniform(-0.01, 0.01)) % 360
    alt = max(20.0, min(80.0, alt + random.uniform(-0.02, 0.02)))
    ha  = ha + 1 / 3600

    # RA/Dec casi fijos — la montura compensa la rotación terrestre
    ra  = TARGET_RA_H + random.uniform(-0.0001, 0.0001)
    dec = TARGET_DEC  + random.uniform(-0.001,  0.001)

    # Slew ocasional
    if slew_timer > 0:
        slew_timer -= 1
    elif random.random() < 0.003:
        slew_timer = 8

    slewing = slew_timer > 0

    payload = json.dumps({
        "ra":           format_ra(ra),
        "dec":          format_dec(dec),
        "ha":           format_ha(ha),
        "alt":          round(alt, 1),
        "az":           round(az, 1),
        "tracking":     not slewing,
        "slewing":      slewing,
        "limitWarning": abs(ha) > 4.5,
        "parkStatus":   "unparked"
    })

    client.publish(TOPIC, payload, qos=0, retain=False)
    print(payload)
    time.sleep(1)