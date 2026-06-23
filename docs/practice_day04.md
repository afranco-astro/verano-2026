# Práctica 04

## Desarrollo del primer Subscriber MQTT en Python

### Objetivo

Desarrollar un cliente MQTT capaz de recibir mensajes publicados por nuestro `publisher.py`.

---

## Antes de comenzar

Verifica que tienes listo:

- [ ] El repositorio está actualizado (`git pull`)
- [ ] El entorno virtual (`.venv`) está activado
- [ ] VS Code tiene abierto el proyecto
- [ ] El Broker MQTT está en ejecución
- [ ] El `publisher.py` desarrollado en la práctica anterior funciona correctamente

---

## Parte 1. Actualizar el repositorio

> **Configuración de Git (solo una vez por repositorio):**
> Configura que `git pull` use rebase en lugar de merge. Esta configuración es local al
> repositorio — no se aplica a otros proyectos en tu máquina.
>
> ```bash
> git config pull.rebase true
> git config rebase.autoStash true
> ```
>
> - `pull.rebase true` — al hacer `git pull`, tus commits locales se reacomodan encima de
>   los cambios remotos en lugar de crear un commit de merge. Mantiene el historial lineal
>   y más fácil de leer.
> - `rebase.autoStash true` — si tienes cambios sin commitear cuando haces `git pull`, el
>   rebase normalmente fallaría. Esta opción guarda tus cambios temporalmente (stash),
>   hace el rebase, y los restaura al terminar — automáticamente.

```bash
git pull
source .venv/Scripts/activate
```

---

## Parte 2. Analizar el Publisher

Antes de escribir código nuevo, abre `examples/<tu_usuario>/publisher.py` y responde junto
con el asesor:

- ¿Dónde se conecta el programa?
- ¿En qué Topic publica?
- ¿Qué hace después de publicar el mensaje?

---

## Parte 3. Diseñar el Subscriber

Antes de programar, piensa en el comportamiento esperado. Un Subscriber debe:

- Conectarse al Broker MQTT
- Suscribirse a un Topic
- **Permanecer ejecutándose esperando mensajes**
- Mostrar cada mensaje recibido

> **Diferencia clave con el Publisher:** el `publisher.py` termina su ejecución apenas
> publica el mensaje. El Subscriber, en cambio, **no debe terminar** — su trabajo es
> quedarse esperando indefinidamente. Esto es nuevo: el primer programa que escribiste
> tenía un final claro, este no lo tiene a propósito.

---

## Parte 4. Construir el Subscriber paso a paso

Crea el archivo `examples/<tu_usuario>/subscriber.py`.

### Paso 1 — Import

Igual que en el Publisher:

```python
import paho.mqtt.client as mqtt
```

### Paso 2 — Configuración

```python
BROKER = "localhost"
PORT   = 1883
TOPIC  = "observatory/weather"
```

### Paso 3 — Definir qué hacer al recibir un mensaje

El Subscriber necesita una función que se ejecute **automáticamente** cada vez que llega
un mensaje. No vamos a explicar todavía por qué funciona así (lo veremos en una sesión
posterior) — por ahora basta con saber que paho-mqtt la llama por nosotros.

```python
def on_message(client, userdata, message):
    # Completar con el asesor
    ...
```

> **Dato para investigar:** `message.payload` no es un `str`, es de tipo `bytes`. Antes
> de poder concatenarlo o imprimirlo como texto normal vas a necesitar convertirlo.
> Investiga qué método de `bytes` se usa para esto.

### Paso 4 — Crear el cliente, conectar y suscribirse

```python
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

# Completar con el asesor: connect() y subscribe()
```

**Nota de orden:** primero se crea el cliente, después se conecta, y la suscripción se
hace después de conectar — nunca antes.

### Paso 5 — Mantener el programa esperando mensajes

```python
client.loop_forever()
```

`loop_forever()` es lo que mantiene el programa corriendo. A diferencia del Publisher,
esta línea **no retorna** — el programa se queda aquí indefinidamente.

> **Importante:** Para detener el programa usa `Ctrl + C` en la terminal. Vas a ver un
> mensaje de `KeyboardInterrupt` — eso es esperado, no es un error que tengamos que
> arreglar todavía. Es simplemente la forma en que Python reporta que interrumpiste el
> programa manualmente.

---

## Parte 5. Ejecutar el Subscriber

Con el entorno virtual activo:

```bash
python examples/<tu_usuario>/subscriber.py
```

El programa quedará esperando — **no vuelve al prompt**, eso es correcto.

En otra terminal (con el venv también activado) ejecuta el Publisher:

```bash
python examples/<tu_usuario>/publisher.py
```

Verifica que el mensaje aparece en la terminal del Subscriber.

**Si no aparece nada:**
- ¿El Topic del Publisher coincide exactamente con el del Subscriber?
- ¿El Broker sigue corriendo?
- ¿Olvidaste asignar `client.on_message = on_message` antes de conectar?

---

## Parte 6. Experimentar

- Cambia el Topic del Publisher sin cambiar el del Subscriber. ¿Qué pasa?
**Se ejecuta correctamente el programa de publisher pero no llega el mensaje al subscriber debido a que no tienen el mimo tópico**

- Ejecuta el Publisher varias veces seguidas mientras el Subscriber sigue corriendo.
**se envían los mensajes que se fueron cambiando en el publisher si mantiene el mismo tópico**

- Detén el Subscriber con `Ctrl+C`, modifica el mensaje que imprime, y vuelve a
  ejecutarlo.
- Intenta suscribirte usando un comodín (`observatory/#`) y publica en varios topics
  distintos bajo `observatory/`.
**Si en el subscriber se usa el # entonces llegan los mensajes de todo canal que sea del observatory así que sí me siguen llegando los mensajes** 
---

## Parte 7. Comparando ambos programas

Completa la siguiente tabla durante la sesión, marcando con ✓ o ✗ si el comportamiento
aplica a cada cliente.

| Comportamiento                 | Publisher | Subscriber |
| ------------------------------ | --------- | ---------- |
| Conecta al Broker              |     ✓     |     ✓      |
| Publica mensajes               |     ✓     |     ✗      |
| Se suscribe a Topics           |     ✗     |     ✓      |
| Finaliza su ejecución          |     ✓     |     ✗      |
| Permanece esperando mensajes   |     ✗     |     ✓     |
|                                |           |            |

Comenta las diferencias con el asesor.

---

## Parte 8. Registrar cambios

Puedes hacer el `add` y el `commit` de dos formas — elige la que prefieras.

**Opción A — Git Bash (manual):**

```bash
git status
git add examples/<tu_usuario>/subscriber.py
git commit -m "Add first MQTT subscriber example"
```

**Opción B — Visual Studio Code:**

1. Abre la pestaña de **Source Control** (icono de rama en la barra lateral).
2. Revisa los cambios en `subscriber.py`.
3. Marca el archivo para incluirlo en el commit (`+` o "Stage Changes").
4. Escribe el mensaje del commit en el cuadro de texto y confirma con el ✓.

El `push` y el `pull` los seguimos haciendo siempre desde Git Bash:

```bash
git push
```

---

## Actividad para el bloque de la tarde

No es necesario escribir código adicional.

Dedica un tiempo a revisar `publisher.py` y `subscriber.py`. Elabora un documento en
`docs/day04_notes.md` (máximo una página) respondiendo:

1. ¿Qué partes del código son prácticamente iguales en Publisher y Subscriber?
2. ¿Qué partes cambian entre ambos programas?
3. ¿Cuál es la función de `on_message` durante la práctica? ¿Quién la ejecuta y cuándo?
4. ¿Por qué el Subscriber nunca termina por sí solo, mientras que el Publisher sí?
5. Si mañana quisieras desarrollar un simulador de un instrumento astronómico, ¿partirías
   del Publisher o del Subscriber? Explica por qué.

No existe una única respuesta correcta; el objetivo es reflexionar sobre la arquitectura
del sistema.

---

## Al finalizar debes tener

- [ ] `subscriber.py` funcionando y recibiendo mensajes del Publisher
- [ ] Entendido por qué el programa no termina solo y cómo detenerlo (`Ctrl+C`)
- [ ] Cambios enviados al repositorio mediante Git
- [ ] Un mejor entendimiento de las diferencias entre ambos tipos de clientes MQTT
