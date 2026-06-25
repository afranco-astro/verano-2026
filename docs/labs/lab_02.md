# Laboratorio 02

## Construcción del Weather Monitor

### Objetivo

Desarrollar una aplicación capaz de recibir mensajes MQTT publicados por el simulador
meteorológico, interpretar su contenido JSON y mostrar la información en pantalla.

---

## Cómo trabajaremos hoy

Igual que en el Laboratorio 01: el asesor explica un bloque, tú lo implementas y preguntas
tus dudas, y entonces avanzamos al siguiente. No es necesario memorizar la sintaxis — lo
importante es entender la responsabilidad de cada bloque.

---

## Antes de comenzar

Verifica que tienes listo:

- [ ] El repositorio actualizado (`git pull`)
- [ ] El entorno virtual (`.venv`) activado
- [ ] VS Code abierto en el proyecto
- [ ] El Broker MQTT en ejecución
- [ ] El `weather_simulator.py` funcionando correctamente

---

## Bloque 1 — Crear el monitor

### Objetivo

Crear la estructura base del programa.

### Crear el archivo

```text
monitors/weather_monitor.py
```

### Explicación

El monitor será el encargado de escuchar los mensajes publicados por el simulador y
mostrar la información al usuario. Como en el `subscriber.py` de la sesión anterior, el
cliente se conecta y se queda esperando — nunca termina por sí solo.

### Código

```python
import json
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "oan/weather"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
```

### Verificación

- Guarda el archivo.
- Compáralo con el del asesor.

> El programa aún no debe ejecutarse.

---

## Bloque 2 — Crear el callback

### Objetivo

Implementar la función que será ejecutada cada vez que llegue un mensaje.

### Explicación

Igual que en `subscriber.py`, el Broker llama automáticamente a esta función cuando llega
un mensaje al Topic al que estamos suscritos. No volvemos a explicar el mecanismo —ya lo
viste la sesión pasada— aquí cambia lo que hacemos *dentro* de la función.

### Código

```python
def on_message(client, userdata, message):

    print(message.payload.decode())
```

### Código adicional

```python
client.on_message = on_message
```

### Verificación

Pregunta para discutir:

> ¿Quién llama realmente a `on_message()`?

---

## Bloque 3 — Interpretar el JSON

### Objetivo

Convertir el texto recibido nuevamente en un objeto de Python.

### Explicación

El simulador envía texto en formato JSON. Necesitamos convertir ese texto en una
estructura que Python pueda utilizar — un diccionario.

### Código (reemplaza el `print()` del Bloque 2)

```python
def on_message(client, userdata, message):

    data = json.loads(message.payload.decode())
    print(data)
```

### Verificación

Discutir:

- ¿Qué hace `json.loads()`?
- ¿Es lo opuesto de qué función que usamos en el simulador?

---

## Bloque 4 — Mostrar la información

### Objetivo

Presentar la información de forma clara, incluyendo cuándo se recibió.

### Explicación

Vamos a mostrar las cinco variables que envía el simulador, y a agregar un timestamp
generado por el propio monitor en el momento en que el mensaje llega.

> **Para reflexionar:** este timestamp lo genera el *monitor*, no el simulador. Marca el
> momento en que el mensaje fue **recibido**, no el momento en que fue **medido**. ¿En qué
> casos sería importante la diferencia? ¿Convendría que el simulador incluyera su propio
> timestamp dentro del payload?

### Reemplazar el cuerpo de `on_message`

```python
def on_message(client, userdata, message):

    data = json.loads(message.payload.decode())
    timestamp = datetime.now().strftime("%H:%M:%S")

    print("--------------------------------")
    print(f"Received at : {timestamp}")
    print(f"Temperature : {data['temperature']} °C")
    print(f"Humidity    : {data['humidity']} %")
    print(f"Wind Speed  : {data['windSpeed']} m/s")
    print(f"Pressure    : {data['pressure']} hPa")
    print(f"Dew Point   : {data['dewPoint']} °C")
```

### Verificación

Ejecutar el simulador. Observar cómo cambian los datos.

---

## Bloque 5 — Conectarse al Broker

### Objetivo

Suscribirse al Topic del simulador y quedar esperando mensajes.

### Código

```python
client.connect(BROKER, PORT)

client.subscribe(TOPIC)

client.loop_forever()
```

### Explicación

`loop_forever()` mantiene la aplicación ejecutándose mientras espera mensajes del Broker
— igual que en `subscriber.py`. Se detiene con `Ctrl + C`.

---

## Ejecutar

En una terminal:

```bash
python simulators/weather_simulator.py
```

En otra:

```bash
python monitors/weather_monitor.py
```

Verificar que los datos aparecen correctamente, una lectura nueva por segundo.

---

## Experimenta

Prueba las siguientes modificaciones:

- Cambia el Topic del simulador.
- Agrega al monitor la variable nueva que hayas creado en el simulador (por ejemplo
  `cloudCover`).
- Modifica el formato de impresión.
- Cambia el QoS de la suscripción.

---

## Registrar cambios

```bash
git status
```

```bash
git add monitors/weather_monitor.py
```

```bash
git commit -m "Add weather monitor"
```

```bash
git push
```

---

## ¿Qué aprendimos hoy?

Al finalizar este laboratorio deberías comprender que:

- Un Subscriber puede recibir información de manera continua.
- JSON permite transportar varios datos en un solo mensaje.
- El callback `on_message()` procesa automáticamente cada mensaje recibido.
- Un monitor puede interpretar y presentar la información generada por otros componentes
  del sistema, y enriquecerla con datos propios (como el timestamp de recepción).

---

## Arquitectura del proyecto hasta ahora

```text
Weather Simulator (Python)
          │
          ▼
      MQTT Broker
      ├──────────────┐
      ▼              ▼
Weather Monitor   Node-RED Dashboard
     (Python)        (próximamente)
```

Cada nuevo componente del proyecto (cámara, domo, telescopio) se agregará a este mismo
diagrama, conectado siempre a través del Broker.
