# Laboratorio 04

## Simulador de Montura del Telescopio

### Objetivo

Desarrollar un simulador que represente el estado de la montura ecuatorial del
telescopio: coordenadas de apuntado, altitud, azimut y estado de seguimiento.

---

## Antes de comenzar

- [ ] Broker MQTT en ejecución
- [ ] Entorno virtual (`.venv`) activado
- [ ] MQTT Explorer abierto y conectado

---

## Contexto

La montura es el componente más importante del observatorio: determina a dónde apunta el
telescopio. Una montura ecuatorial sigue el movimiento aparente del cielo girando sobre
un eje alineado con el polo norte celeste — por eso el azimut y la altitud cambian
continuamente incluso cuando el telescopio apunta al mismo objeto.

El simulador publicará coordenadas en dos sistemas, más el Ángulo Horario:

- **RA / Dec** (coordenadas ecuatoriales) — definen la posición del objeto en el cielo.
  Permanecen casi fijas mientras el telescopio sigue a un objeto.
- **Alt / Az** (coordenadas horizontales) — posición relativa al horizonte del
  observatorio. Cambian continuamente aunque el objeto sea el mismo.
- **HA — Ángulo Horario** — mide cuántas horas al este (negativo) o al oeste (positivo)
  del meridiano está apuntando la montura. El telescopio 2.1m del OAN-SPM tiene límites
  de ±5.5h; si se supera ese límite la montura debe detenerse. El simulador incluirá una
  advertencia cuando el HA se acerque a ese límite (> 4.5h en cualquier dirección).

---

## Bloque 1 — Base del simulador

### Crear el archivo

```text
simulators/mount_simulator.py
```

### Explicación

Además de las importaciones habituales, este simulador define tres funciones de utilidad
que convierten coordenadas numéricas al formato legible que usan los astrónomos:
`12h 34m 56.7s` para Ascensión Recta, `+45° 23' 12.4"` para Declinación, y
`E 02h 00m 00.0s` / `W 02h 00m 00.0s` para el Ángulo Horario (E = este del meridiano,
W = oeste).

`TARGET_RA_H` y `TARGET_DEC` representan las coordenadas ecuatoriales de un objeto
ficticio que el telescopio está siguiendo durante la sesión de observación.

### Código

```python
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

def format_ra(hours):
    h = int(hours)
    m = int((hours - h) * 60)
    s = ((hours - h) * 60 - m) * 60
    return f"{h:02d}h {m:02d}m {s:04.1f}s"

def format_dec(deg):
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
```

### Verificación

- Guarda el archivo.
- El programa aún no debe ejecutarse.

---

## Bloque 2 — Variables de estado y ciclo principal

### Explicación

El ciclo simula tres comportamientos:

1. **Tracking normal:** `az` avanza 0.05° por segundo (movimiento aparente del cielo).
   `alt` oscila levemente. RA y Dec se mantienen cerca del objeto con ruido mínimo.
   El Ángulo Horario avanza a razón de 1/3600 horas por segundo — la tasa real sidérea.

2. **Slewing ocasional:** con muy baja probabilidad, el telescopio simula moverse
   (`slewing: true`) durante 8 segundos — como si apuntara a un nuevo objeto.
   Mientras hay slew, `tracking` es `false`.

3. **Advertencia de límite:** cuando `ha` supera ±4.5h (acercándose al límite real de
   ±5.5h del telescopio 2.1m), `limitWarning` cambia a `true`. En el dashboard esto
   puede mostrarse como un indicador de color.

### Agrega el siguiente código

```python
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
```

---

## Bloque 3 — Ejecutar y verificar

```bash
python simulators/mount_simulator.py
```

En MQTT Explorer verifica el Topic `oan/mount`. Observa:

- `az` cambia lentamente cada segundo.
- `ha` avanza de valores negativos (Este) hacia positivos (Oeste) — muy lento, pero
  visible si esperas unos minutos o miras el valor con precisión decimal.
- `ra` y `dec` se mantienen prácticamente fijos.
- `limitWarning` será `true` cuando el simulador lleve suficiente tiempo corriendo y
  `ha` supere 4.5h (tarda varias horas en llegar a ese punto en tiempo real).
- Ocasionalmente `slewing: true` aparece por unos segundos.

Detén el simulador con `Ctrl + C` cuando termines de verificar.

---

## Código completo — `mount_simulator.py`

```python
import json
import random
import time

import paho.mqtt.client as mqtt

BROKER   = "localhost"
PORT     = 1883
TOPIC    = "oan/mount"

TARGET_RA_H = 12.582
TARGET_DEC  = 45.387
HA_LIMIT    = 5.5

def format_ra(hours):
    h = int(hours)
    m = int((hours - h) * 60)
    s = ((hours - h) * 60 - m) * 60
    return f"{h:02d}h {m:02d}m {s:04.1f}s"

def format_dec(deg):
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
ha         = -2.0
slew_timer = 0

while True:
    az  = (az + 0.05 + random.uniform(-0.01, 0.01)) % 360
    alt = max(20.0, min(80.0, alt + random.uniform(-0.02, 0.02)))
    ha  = ha + 1 / 3600

    ra  = TARGET_RA_H + random.uniform(-0.0001, 0.0001)
    dec = TARGET_DEC  + random.uniform(-0.001,  0.001)

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
```

---

## Registrar cambios

```bash
git add simulators/mount_simulator.py
git commit -m "Add telescope mount simulator"
git push
```
