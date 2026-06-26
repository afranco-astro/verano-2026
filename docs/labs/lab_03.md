# Laboratorio 03

## Integración de Node-RED con el Weather Simulator

### Objetivo

Conectar Node-RED al Broker MQTT, recibir los datos del simulador meteorológico y
visualizarlos en un dashboard en tiempo real, sin escribir una sola línea de código.

---

## Cómo trabajaremos hoy

La dinámica de hoy es diferente a los laboratorios anteriores: en lugar de construir el
programa bloque por bloque y ejecutarlo al final, **veremos resultados después de cada
paso**. Cada bloque termina con un Deploy y un resultado visible en el navegador.

---

## Antes de comenzar

Verifica que tienes listo:

- [ ] El repositorio actualizado (`git pull`)
- [ ] El entorno virtual (`.venv`) activado
- [ ] El Broker MQTT en ejecución
- [ ] MQTT Explorer conectado al Broker

---

## Bloque 1 — Poner el sistema en marcha

### Objetivo

Verificar que el simulador está publicando antes de abrir Node-RED.

### Explicación

Node-RED se conectará al mismo Broker al que ya se conectan el simulador y el monitor.
Antes de abrirlo, confirma que el sistema base está funcionando correctamente.

### Ejecuta el simulador

En una terminal con el `.venv` activo:

```bash
python simulators/weather_simulator.py
```

Verifica en MQTT Explorer que el Topic `oan/weather` recibe un mensaje JSON nuevo cada
segundo.

Deja el simulador corriendo. Durante todo el laboratorio seguirá publicando en segundo
plano.

---

## Bloque 2 — Instalar Node-RED

### Objetivo

Instalar Node-RED y dejarlo corriendo como un servicio local en tu máquina.

### Explicación

Node-RED es una herramienta de programación visual que conecta servicios y dispositivos
mediante flujos. Corre como un servidor local y se opera desde el navegador. Como el
Broker Mosquitto, se deja corriendo en segundo plano mientras trabajas.

Node-RED requiere **Node.js**. Antes de instalarlo, verifica si ya lo tienes:

```bash
node --version
```

Si el comando muestra una versión (por ejemplo `v22.x.x`), pasa directamente a la
instalación de Node-RED. Si no, instala Node.js primero.

---

### Instalar Node.js (si no está instalado)

1. Ve a [https://nodejs.org](https://nodejs.org) y descarga la versión **LTS**.
2. Ejecuta el instalador. Las opciones predeterminadas están bien.
3. Cierra y vuelve a abrir **Git Bash** después de instalar.
4. Verifica:
   ```bash
   node --version
   npm --version
   ```

---

### Instalar Node-RED

Abre **Git Bash como administrador** y ejecuta:

```bash
npm install -g node-red
```

La descarga puede tardar un momento. Cuando termine, verifica la instalación:

```bash
node-red --version
```

---

### Iniciar Node-RED

En una **terminal nueva** (fuera del proyecto, no necesitas el `.venv`):

```bash
node-red
```

Verás mensajes de inicio. Node-RED quedará corriendo en esa terminal — no la cierres.

Abre el navegador y ve a:

```text
http://127.0.0.1:1880
```

Verás el editor de flujos de Node-RED. Eso es todo: está listo.

> **Para el asesor (Linux):** `npm install -g node-red` funciona igual. Si usas `nvm`,
> asegúrate de que la versión activa de Node.js sea ≥ 18 LTS antes de instalar.

---

## Bloque 3 — Instalar el Dashboard

### Objetivo

Agregar los nodos de visualización que usaremos para mostrar los datos del simulador.

### Explicación

Node-RED por defecto no incluye widgets de visualización (gauges, gráficas, etc.). El
**Dashboard** es un paquete adicional que los agrega. Se instala desde la propia interfaz
de Node-RED, sin usar la terminal.

### Pasos

1. En el editor de Node-RED, haz clic en el menú **☰** (esquina superior derecha).
2. Selecciona **Manage Palette**.
3. Ve a la pestaña **Install**.
4. Busca: `node-red-dashboard`
5. Haz clic en **Install** junto al paquete que aparece como `node-red-dashboard`.
6. Espera a que termine. Node-RED cargará los nodos automáticamente.

Después de instalar, verás nuevos nodos en la paleta izquierda bajo la sección **dashboard**.

El dashboard estará disponible en:

```text
http://127.0.0.1:1880/ui
```

(Por ahora estará vacío — lo llenaremos paso a paso.)

---

## Bloque 4 — Primer flujo: MQTT In → Debug

### Objetivo

Recibir mensajes del simulador en Node-RED y verlos en el panel de Debug.

### Explicación

En Node-RED, un **flujo** es una secuencia de nodos conectados. Los nodos se arrastran
desde la paleta izquierda al espacio de trabajo y se conectan entre sí.

El primer flujo que construiremos es el más simple posible: recibir un mensaje y
mostrarlo. Eso nos confirmará que Node-RED está hablando con el mismo Broker que el
simulador.

### Construye el flujo

**Paso 1 — Agregar un nodo MQTT In:**

- Arrastra el nodo **mqtt in** al espacio de trabajo.
- Haz doble clic para configurarlo:
  - **Server:** haz clic en el lápiz (✏) para agregar un nuevo broker.
    - Host: `localhost`
    - Port: `1883`
    - Guarda con **Add**.
  - **Topic:** `oan/weather`
  - **QoS:** `0`
  - **Output:** `a String`
- Confirma con **Done**.

**Paso 2 — Agregar un nodo Debug:**

- Arrastra el nodo **debug** al espacio de trabajo.
- La configuración predeterminada está bien (muestra `msg.payload`).

**Paso 3 — Conectar:**

- Arrastra desde el punto de salida del nodo **mqtt in** hasta el punto de entrada del
  nodo **debug**.

**Paso 4 — Deploy:**

- Haz clic en el botón rojo **Deploy** (esquina superior derecha).

**Paso 5 — Ver el resultado:**

- Abre el panel de **Debug** (ícono de insecto 🐞 en la barra derecha).
- Deberías ver un mensaje JSON nuevo cada segundo.

> Este es el primer "momento importante": Node-RED está recibiendo los datos del
> simulador que construiste ayer. Un sistema que antes solo funcionaba en la terminal
> ahora tiene una nueva ventana al mundo.

---

## Bloque 5 — Nodo JSON

### Objetivo

Convertir el texto recibido en un objeto que Node-RED pueda interpretar.

### Explicación

En el Debug del bloque anterior los mensajes aparecen como texto (un `string`). Para
poder acceder a cada campo por separado (`temperature`, `humidity`, etc.) necesitamos
convertir ese texto en un objeto — exactamente lo que hace `json.loads()` en Python.

En Node-RED existe un nodo que hace exactamente eso, sin escribir código.

> **Pregunta para discutir con el asesor:** ¿qué nodo de Python es el equivalente al
> nodo JSON de Node-RED?

### Modifica el flujo

- Arrastra el nodo **json** al espacio de trabajo, entre los dos nodos existentes.
- Conecta: `mqtt in → json → debug`
- **Deploy**.

Observa el Debug: ahora el mensaje aparece como un objeto con campos individuales, no
como texto plano. Node-RED lo muestra expandible.

---

## Bloque 6 — Primer gauge: temperatura

### Objetivo

Mostrar la temperatura en un indicador visual en el Dashboard.

### Explicación

Ahora que los datos llegan como objeto, podemos enrutar cada campo a su propio widget.
Para eso necesitamos dos cosas:

1. Un nodo **Change** que extraiga el campo que nos interesa y lo ponga en `msg.payload`.
2. Un nodo **Gauge** que lea `msg.payload` y lo muestre visualmente.

El nodo JSON conectará en paralelo con múltiples Change nodes — uno por cada variable.

### Configura el Dashboard

Antes de agregar el primer gauge, crea la estructura del dashboard:

1. En la paleta izquierda, en la sección **dashboard**, arrastra un nodo **gauge** al
   espacio de trabajo.
2. Haz doble clic para configurarlo.
3. En el campo **Group**, haz clic en el lápiz (✏):
   - Esto abre la configuración del **Grupo**.
   - En **Tab**, haz clic en el lápiz (✏):
     - Crea una Tab llamada `Weather Station`.
     - Guarda.
   - Nombre del grupo: `Atmosphere`.
   - Guarda.

Ahora configura el gauge:

- **Label:** `Temperature`
- **Units:** `°C`
- **Range:** min `0`, max `40`
- **Value Format:** `{{value}}`
- Guarda con **Done**.

### Conecta el Change node

- Arrastra un nodo **change** al espacio de trabajo.
- Haz doble clic para configurarlo:
  - **Rules:** Set `msg.payload` to `msg.payload.temperature`
  - Cambia el tipo de valor a **msg.** y escribe `payload.temperature`.
  - Guarda.
- Conecta: `json → change → gauge`

> El nodo JSON sigue conectado al Debug también — puedes mantener ambas conexiones
> para ver los datos crudos mientras pruebas.

### Deploy y verificar

- Haz clic en **Deploy**.
- Abre el Dashboard: `http://127.0.0.1:1880/ui`
- Verás el gauge de temperatura moviéndose en tiempo real.

---

## Bloque 7 — Completar el Dashboard

### Objetivo

Agregar un gauge para cada variable del simulador.

### Explicación

El proceso es el mismo para cada variable: un Change node que extrae el campo, conectado
a un Gauge configurado con su etiqueta y unidades. En Node-RED puedes duplicar nodos
(clic derecho → Duplicate) para agilizar el proceso.

### Agrega los siguientes gauges

Para cada uno: duplica el Change node, cambia el campo que extrae, duplica el Gauge y
configura etiqueta, unidades y rango.

| Variable     | Change: extraer         | Label       | Units | Min  | Max    |
|--------------|------------------------|-------------|-------|------|--------|
| `humidity`   | `msg.payload.humidity` | Humidity    | %     | 0    | 100    |
| `windSpeed`  | `msg.payload.windSpeed`| Wind Speed  | m/s   | 0    | 20     |
| `pressure`   | `msg.payload.pressure` | Pressure    | hPa   | 980  | 1030   |
| `dewPoint`   | `msg.payload.dewPoint` | Dew Point   | °C    | -10  | 20     |

### Deploy y verificar

- Haz clic en **Deploy** después de agregar cada gauge para ver el resultado
  progresivamente.
- Cuando termines, el Dashboard mostrará las cinco variables actualizándose en tiempo
  real.

---

## Bloque 8 — El sistema conectado en vivo

### Objetivo

Observar que Node-RED y el simulador están **desacoplados** — uno puede cambiar sin que
el otro tenga que cambiar.

### Explicación

El Broker MQTT actúa como intermediario: el simulador publica y no sabe quién escucha;
Node-RED escucha y no sabe quién publica. Esto permite que un componente evolucione sin
romper al otro.

### Demostración

1. Abre `simulators/weather_simulator.py` en VS Code.
2. Agrega una nueva variable al diccionario, por ejemplo:

   ```python
   "cloudCover": random.randint(0, 100)
   ```

3. Guarda el archivo, detén el simulador (`Ctrl+C`) y vuelve a ejecutarlo.
4. Abre el Debug en Node-RED.

Verás que el nuevo campo `cloudCover` ya aparece en el objeto — **sin haber tocado
Node-RED**. El sistema lo recibe automáticamente.

> **Para discutir:** si quisieras visualizar `cloudCover` en el Dashboard, ¿qué
> necesitarías agregar? ¿Cuánto tiempo te tomaría?

---

## Registrar cambios

Los flujos de Node-RED se guardan automáticamente en tu máquina, pero los cambios al
simulador deben quedar en el repositorio.

```bash
git status
git add simulators/weather_simulator.py
git commit -m "Add cloudCover field to weather simulator"
git push
```

---

## ¿Qué aprendimos hoy?

Al finalizar este laboratorio deberías comprender que:

- Node-RED puede suscribirse al mismo Broker MQTT que cualquier cliente Python.
- El nodo JSON convierte el payload de texto a objeto, de la misma forma que
  `json.loads()` en Python.
- Cada campo del JSON puede enrutarse de forma independiente a su propio widget visual.
- Un componente del sistema puede evolucionar (agregar campos) sin romper a los demás,
  porque el Broker actúa como intermediario.
- Un sistema distribuido puede tener múltiples "consumidores" de la misma información
  (el monitor Python y el Dashboard de Node-RED) corriendo al mismo tiempo.

---

## Arquitectura del proyecto hasta ahora

```text
Weather Simulator (Python)
          │
          ▼
      MQTT Broker
      ├──────────────────────┐
      ▼                      ▼
Weather Monitor          Node-RED
   (Python)            Dashboard (UI)
```
