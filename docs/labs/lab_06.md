# Laboratorio 06

## Simulador del Sistema de Guiado

### Objetivo

Desarrollar un simulador que represente el comportamiento del sistema de guiado
automático del telescopio: adquisición de la estrella guía, correcciones continuas y
pausas sincronizadas con la lectura del sensor de la cámara.

---

## Antes de comenzar

- [ ] Broker MQTT en ejecución
- [ ] Entorno virtual (`.venv`) activado
- [ ] MQTT Explorer abierto y conectado

---

## Contexto

Ninguna montura de telescopio es perfectamente precisa. Incluso en modo de seguimiento,
el telescopio deriva lentamente — los objetos se mueven en el campo de visión. Para
exposiciones largas, esta deriva arruinaría la imagen.

El **sistema de guiado** usa un sensor secundario para observar una estrella brillante
cercana al objeto de interés. Un algoritmo compara continuamente la posición de esa
estrella con su posición de referencia y envía pequeñas correcciones a la montura para
mantenerla fija. Esto sucede varias veces por segundo.

Las métricas clave del guiado son **rmsRA** y **rmsDec**: el error cuadrático medio de
la posición de la estrella en Ascensión Recta y Declinación, medido en segundos de arco
(arcsec). En condiciones normales de SPM, valores por debajo de 0.8 arcsec son buenos.

---

## Bloque 1 — Base del simulador

### Crear el archivo

```text
simulators/guider_simulator.py
```

### Código

```python
import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883
TOPIC  = "oan/guider"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
```

### Verificación

- Guarda el archivo.
- El programa aún no debe ejecutarse.

---

## Bloque 2 — Variables de estado

### Explicación

| Variable      | Significado                                                    |
|---------------|----------------------------------------------------------------|
| `guiding`     | `True` cuando el sistema está enviando correcciones activamente|
| `star_locked` | `True` cuando la estrella guía fue adquirida                   |
| `corrections` | Contador total de correcciones enviadas a la montura           |
| `lock_timer`  | Segundos que tarda en adquirir la estrella al inicio           |
| `pause_timer` | Segundos de pausa breve (simula la lectura del sensor CCD)     |

El guiador arranca buscando la estrella guía (`lock_timer = 6`). Después de 6 segundos
la adquiere y empieza a corregir. Ocasionalmente hace pausas cortas — simulando que la
cámara CCD está en modo de lectura y el guiador espera antes de reanudar.

### Agrega el siguiente código

```python
guiding     = False
star_locked = False
corrections = 0
lock_timer  = 6
pause_timer = 0
```

---

## Bloque 3 — Ciclo principal

### Explicación

El ciclo tiene tres fases posibles en cada iteración:

1. **Adquisición inicial** (`lock_timer > 0`): el guiador busca la estrella. rmsRA y
   rmsDec son 0 — no hay correcciones todavía.

2. **Pausa breve** (`pause_timer > 0`): simula una interrupción breve. guiding pasa a
   `False` momentáneamente.

3. **Guiando** (estado normal): rmsRA y rmsDec toman valores aleatorios pequeños
   representando el error residual. El contador de correcciones sube. Con probabilidad
   baja (6% por ciclo) se activa una pausa.

### Agrega el siguiente código

```python
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
```

---

## Bloque 4 — Ejecutar y verificar

```bash
python simulators/guider_simulator.py
```

En MQTT Explorer verifica el Topic `oan/guider`. Observa:

1. Los primeros 6 segundos: `starLocked: false`, `guiding: false`, rms en 0.
2. Al segundo 6: `starLocked: true`, `guiding: true`, rmsRA y rmsDec aparecen.
3. `corrections` sube continuamente mientras el guiador trabaja.
4. Ocasionalmente `guiding` baja a `false` por 3 segundos y sube de nuevo.

Detén el simulador con `Ctrl + C` cuando termines de verificar.

---

## Código completo — `guider_simulator.py`

```python
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
```

---

## Registrar cambios

```bash
git add simulators/guider_simulator.py
git commit -m "Add guider simulator"
git push
```
