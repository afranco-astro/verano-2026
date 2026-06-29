# Laboratorio 05

## Simulador de Cámara CCD

### Objetivo

Desarrollar un simulador que represente el ciclo de operación de una cámara CCD
astronómica: enfriamiento, toma de exposición, lectura del detector y cambio de filtro.

---

## Antes de comenzar

- [ ] Broker MQTT en ejecución
- [ ] Entorno virtual (`.venv`) activado
- [ ] MQTT Explorer abierto y conectado

---

## Contexto

Una cámara CCD astronómica no funciona como una cámara fotográfica ordinaria. Tiene
tres características que la hacen especial:

1. **Enfriamiento activo:** el sensor se enfría hasta −25 °C para reducir el ruido
   electrónico. Un sistema Peltier mantiene esa temperatura durante toda la noche.

2. **Ciclo de exposición:** el obturador se abre, el sensor acumula luz durante un
   tiempo definido (segundos o minutos), y al terminar el sensor se lee electrónicamente
   — la imagen se transfiere a la computadora.

3. **Filtros intercambiables:** una rueda de filtros permite seleccionar qué longitudes
   de onda captura el sensor. Los filtros estándar astronómicos son U, B, V, R e I
   (ultravioleta, azul, visual, rojo e infrarrojo cercano).

El simulador reproducirá este ciclo completo: enfriamiento → exposición → lectura →
nueva exposición con el siguiente filtro.

---

## Bloque 1 — Base del simulador

### Crear el archivo

```text
simulators/camera_simulator.py
```

### Explicación

`EXPOSURE_STEPS` define cuántos segundos dura una exposición completa (de 0 a 100%).
`READOUT_STEPS` define cuántos segundos toma leer el sensor después de cada exposición.
Estos valores son cortos para que el ciclo sea visible en la sesión — en una noche real
una exposición puede durar varios minutos.

### Código

```python
import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883
TOPIC  = "oan/camera"

FILTERS        = ["U", "B", "V", "R", "I"]
EXPOSURE_STEPS = 15   # segundos por exposición completa
READOUT_STEPS  = 3    # segundos de lectura del sensor

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
```

### Verificación

- Guarda el archivo.
- El programa aún no debe ejecutarse.

---

## Bloque 2 — Variables de estado

### Explicación

Este simulador tiene **estado interno** — a diferencia del simulador de clima que genera
cada valor de forma completamente independiente, la cámara "recuerda" en qué etapa del
ciclo se encuentra y avanza de una a otra.

Las variables de estado son:

| Variable    | Significado inicial                                     |
|-------------|--------------------------------------------------------|
| `status`    | `"cooling"` — arranca enfriando el sensor              |
| `temp`      | `15.0` °C — temperatura ambiente, irá bajando a −25 °C |
| `target_t`  | `−25.0` °C — temperatura objetivo del sensor           |
| `cooler`    | `0` % — potencia del sistema Peltier                   |
| `filter_i`  | `2` — índice en la lista FILTERS (empieza en "V")      |
| `progress`  | `0` % — progreso de la exposición actual               |
| `readout_t` | `0` — contador regresivo de lectura del sensor         |

### Agrega el siguiente código

```python
status    = "cooling"
temp      = 15.0
target_t  = -25.0
cooler    = 0
filter_i  = 2
progress  = 0
readout_t = 0
```

---

## Bloque 3 — Ciclo principal

### Explicación

El ciclo tiene dos partes independientes que se ejecutan cada segundo:

**Control de temperatura:** si el sensor está por encima de la temperatura objetivo, el
cooler trabaja al máximo y la temperatura baja. Al alcanzar −25 °C el cooler solo
mantiene esa temperatura con ruido pequeño.

**Máquina de estados:** el simulador avanza por cuatro estados en secuencia:
`cooling → idle → exposing → readout → idle → exposing → ...`

> **Nota:** al ejecutar el simulador, el primer ciclo de enfriamiento tarda
> aproximadamente 30–50 segundos antes de que aparezca la primera exposición.
> Eso es intencional — así se ve cómo el sistema se prepara.

### Agrega el siguiente código

```python
while True:
    # --- Control de temperatura ---
    if temp > target_t + 0.5:
        cooler = min(100, int((temp - target_t) * 3 + 40))
        temp   = round(temp - random.uniform(0.3, 0.8), 1)
    else:
        cooler = int(75 + random.uniform(-5, 5))
        temp   = round(target_t + random.uniform(-0.3, 0.3), 1)

    # --- Máquina de estados ---
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
```

---

## Bloque 4 — Ejecutar y verificar

```bash
python simulators/camera_simulator.py
```

En MQTT Explorer verifica el Topic `oan/camera`. Observa la secuencia:

1. `status: "cooling"` — temperatura bajando desde 15 °C, coolerPower alto.
2. `status: "idle"` — durante un segundo (transición).
3. `status: "exposing"` — `exposureProgress` sube de 0 a 100, filtro visible.
4. `status: "readout"` — 3 segundos sin progreso.
5. Nuevo ciclo con el siguiente filtro en la lista.

Detén el simulador con `Ctrl + C` cuando termines de verificar.

---

## Código completo — `camera_simulator.py`

```python
import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883
TOPIC  = "oan/camera"

FILTERS        = ["U", "B", "V", "R", "I"]
EXPOSURE_STEPS = 15
READOUT_STEPS  = 3

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

status    = "cooling"
temp      = 15.0
target_t  = -25.0
cooler    = 0
filter_i  = 2
progress  = 0
readout_t = 0

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
```

---

## Registrar cambios

```bash
git add simulators/camera_simulator.py
git commit -m "Add CCD camera simulator"
git push
```
