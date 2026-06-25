# Laboratorio 01

## Construcción del Weather Simulator

### Objetivo

Desarrollar el primer componente del sistema de monitoreo basado en MQTT, capaz de generar
datos meteorológicos simulados y publicarlos en formato JSON, de manera continua.

---

## Cómo trabajaremos hoy

Esta práctica no explica Python línea por línea — explica la **responsabilidad de cada
bloque** del programa. Antes de cada bloque el asesor te explicará qué hace y por qué,
después tú lo escribes, y antes de continuar al siguiente bloque preguntas lo que no haya
quedado claro. La sintaxis se aprende poco a poco; lo importante hoy es entender cómo se
construye un componente de un sistema distribuido.

---

## Antes de comenzar

Verifica que tienes listo:

- [ ] El repositorio actualizado (`git pull`)
- [ ] El entorno virtual (`.venv`) activado
- [ ] VS Code abierto en el proyecto
- [ ] El Broker MQTT en ejecución
- [ ] MQTT Explorer abierto y conectado al Broker

---

## Bloque 1 — Crear el simulador y conectarlo al Broker

### Objetivo

Crear el archivo del simulador, importar lo necesario, y establecer la conexión con el
Broker.

### Crear el archivo

```text
simulators/weather_simulator.py
```

### Explicación

Este programa simulará una estación meteorológica. En lugar de leer sensores reales,
generará valores ficticios y los enviará mediante MQTT. La conexión al Broker se hace
**una sola vez**, al inicio del programa — no en cada lectura.

### Código

```python
import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "oan/weather"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
```

### Verificación

- Guarda el archivo.
- Compara el código con el del asesor.
- Espera las indicaciones para continuar.

> **Nota:** El programa aún no debe ejecutarse.

---

## Bloque 2 — El ciclo de publicación continua

### Objetivo

Establecer, desde el inicio, que este simulador **nunca termina por sí solo** — al igual
que una estación meteorológica real, que nunca deja de medir.

### Explicación

Una estación meteorológica no publica una sola medición y se detiene; mide y publica de
forma continua, indefinidamente. Por eso construimos el programa con esta forma desde el
principio, en lugar de empezar con una sola publicación y modificarla después.

`while True:` repite el bloque de código indentado debajo para siempre. `time.sleep(1)`
pausa la ejecución un segundo en cada vuelta, para no saturar al Broker con miles de
mensajes por segundo.

### Agrega el siguiente código

```python
while True:
    # Aquí generaremos y publicaremos cada lectura
    time.sleep(1)
```

### Verificación

Si ejecutas el programa en este punto, no va a hacer nada visible — pero tampoco va a
terminar. Coméntalo con el asesor:

> ¿Cómo se detiene un programa que nunca termina por sí solo?

> **Nota:** El programa aún no debe ejecutarse — primero vamos a llenar el ciclo con
> contenido útil. Pero ya sabes, desde este bloque, que cuando lo ejecutemos en el
> Bloque 6 tendrás que detenerlo manualmente.

---

## Bloque 3 — Generar datos simulados

### Objetivo

Crear información meteorológica ficticia en cada vuelta del ciclo.

### Explicación

Como aún no contamos con una estación meteorológica real, utilizaremos números aleatorios
para simular sus mediciones. Cada vuelta del `while True` generará una lectura distinta.

Además de temperatura, humedad y viento, agregamos dos variables más:

- **`pressure`** — presión atmosférica, en hectopascales (hPa). A nivel del mar suele
  rondar los 1013 hPa; usamos un rango realista alrededor de ese valor.
- **`dewPoint`** — punto de rocío, en °C. Es la temperatura a la que el aire tendría que
  enfriarse para saturarse de humedad y comenzar a condensarse (rocío, niebla). Está
  relacionado con la humedad: entre más alto es el punto de rocío respecto a la
  temperatura, más húmedo se siente el ambiente.

### Agrega el siguiente código (dentro del `while True`)

```python
    weather_data = {
        "temperature": round(random.uniform(10.0, 25.0), 1),
        "humidity": random.randint(20, 80),
        "windSpeed": round(random.uniform(0.0, 15.0), 1),
        "pressure": round(random.uniform(990.0, 1025.0), 1),
        "dewPoint": round(random.uniform(0.0, 15.0), 1)
    }
```

### Verificación

Revisa junto con el asesor:

- ¿Qué representa cada variable?
- ¿Qué tipo de dato almacena cada campo?

> **Para reflexionar (no hay que corregirlo hoy):** en una estación real, el `dewPoint`
> nunca debería ser mayor que la `temperature` — físicamente no tiene sentido que el aire
> se sature a una temperatura más alta que la temperatura actual. Como aquí generamos cada
> valor de forma independiente y aleatoria, esa relación no se respeta. ¿Te parece que
> valdría la pena corregirlo? ¿Cómo lo harías?

---

## Bloque 4 — Convertir los datos a JSON

### Objetivo

Preparar la información para ser enviada mediante MQTT.

### Explicación

MQTT puede transportar cualquier tipo de texto. Nosotros utilizaremos JSON porque permite
organizar varios datos dentro de un mismo mensaje.

### Agrega el siguiente código (dentro del `while True`)

```python
    payload = json.dumps(weather_data)
```

### Verificación

Pregunta para discutir:

> ¿Qué ventaja tiene enviar un solo mensaje JSON en lugar de cinco mensajes
> independientes (uno por cada variable)?

---

## Bloque 5 — Publicar el mensaje

### Objetivo

Enviar la información al Broker MQTT en cada vuelta del ciclo.

### Explicación

Con la información ya preparada, la publicamos en el Topic elegido. Agregamos también un
`print()` para ver en la terminal, en tiempo real, qué se está publicando — es la única
forma de confirmar que el programa sigue vivo mientras corre indefinidamente.

### Agrega el siguiente código (dentro del `while True`)

```python
    client.publish(
        topic=TOPIC,
        payload=payload,
        qos=0,
        retain=False
    )

    print(payload)
```

### Verificación

Revisa junto con el asesor:

- Broker
- Topic
- QoS
- Retain

El programa, en este punto, ya está completo. Repasa con el asesor el archivo completo
de principio a fin antes de ejecutarlo.

---

## Bloque 6 — Ejecutar el simulador

### Objetivo

Verificar que el mensaje llega correctamente al Broker, de forma continua.

### Ejecuta el programa

```bash
python simulators/weather_simulator.py
```

Vas a ver una nueva línea impresa en la terminal cada segundo — y el programa **no va a
regresar al prompt**, igual que el `subscriber.py` de la sesión pasada. Eso es correcto.

Abre MQTT Explorer y verifica que el Topic:

```text
oan/weather
```

recibe un mensaje JSON nuevo cada segundo.

Para detener el simulador usa `Ctrl + C` en la terminal.

---

## Experimenta

Una vez que el simulador funcione:

- Cambia los rangos de temperatura, presión o punto de rocío.
- Agrega una nueva variable, por ejemplo `cloudCover` (porcentaje de nubosidad).
- Modifica el Topic utilizado.
- Cambia el QoS entre 0 y 1.
- Cambia el `time.sleep(1)` por otro valor. ¿Qué pasa con la cantidad de mensajes en MQTT
  Explorer?
- Observa los cambios en MQTT Explorer.

---

## Registrar cambios

Verifica el estado del repositorio:

```bash
git status
```

Agrega el nuevo archivo:

```bash
git add simulators/weather_simulator.py
```

Crea el commit:

```bash
git commit -m "Add weather simulator"
```

Envía los cambios:

```bash
git push
```

---

## ¿Qué aprendimos hoy?

Al finalizar este laboratorio deberías comprender que:

- Un simulador permite desarrollar aplicaciones sin depender de hardware real.
- JSON facilita el intercambio de información estructurada en un solo mensaje.
- MQTT transporta mensajes, independientemente de su contenido.
- Un componente de software puede simular el comportamiento de un instrumento físico, y
  ese comportamiento incluye no terminar nunca por sí solo.
