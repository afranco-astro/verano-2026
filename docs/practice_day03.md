# Práctica 03

## Primer cliente MQTT en Python

### Objetivo

Escribir un programa en Python que se conecte a un Broker MQTT y publique un mensaje.

---

## Antes de comenzar

Verifica que tienes listo:

- [ ] El Broker MQTT está en ejecución
- [ ] Hay un `mosquitto_sub` escuchando en otra terminal
- [ ] Python funciona (`python --version`)
- [ ] VS Code tiene abierto el repositorio del proyecto

---

## Parte 1. Actualizar el repositorio

Abre **Git Bash** en el directorio del proyecto y obtén los últimos cambios:

```bash
git pull
```

---

## Parte 2. Crear tu directorio de trabajo

Todo el código que escribas durante el curso debe ir dentro de tu carpeta personal en
`examples/`. Créala usando el formato `<inicial_nombre><primer_apellido>`:

```text
examples/
    afranco/
    jlopez/
```

---

## Parte 3. Crear el entorno virtual

Un **entorno virtual** es un espacio aislado donde instalamos las bibliotecas del proyecto
sin afectar el resto del sistema. El entorno virtual del curso vive en la raíz del
repositorio y es compartido por todas las prácticas — solo se crea una vez.

Desde la raíz del proyecto, crea el entorno virtual:

```bash
python -m venv .venv
```

Actívalo:

```bash
source .venv/Scripts/activate
```

Si se activó correctamente, verás el prefijo `(.venv)` al inicio de la línea:

```text
(.venv) $
```

> Cada vez que abras una terminal nueva para trabajar en el proyecto, deberás activar
> el entorno virtual nuevamente.

---

## Parte 4. Configurar VS Code

Abre el proyecto en VS Code y selecciona el intérprete de Python que corresponde al
entorno virtual. VS Code lo mostrará como:

```text
Python X.X.X ('.venv': venv)
```

Esto asegura que VS Code use las mismas bibliotecas que instalaste en el entorno virtual.

---

## Parte 5. Instalar Paho MQTT

**Paho MQTT** es la biblioteca que permite a Python comunicarse mediante el protocolo
MQTT.

Instálala con la versión exacta que usaremos en el curso:

```bash
pip install "paho-mqtt==2.1.0"
```

Verifica que quedó instalada:

```bash
pip list
```

Guarda las dependencias del proyecto en un archivo:

```bash
pip freeze > requirements.txt
```

Abre `requirements.txt` y observa su contenido. Este archivo le permite a cualquier
persona reproducir exactamente el mismo ambiente en otra computadora.

---

## Parte 6. Escribir el Publisher

Crea el archivo `examples/<tu_usuario>/publisher.py` en VS Code.

Vamos a construirlo en cuatro pasos. Escribe cada bloque, lee el comentario, y discute
con el asesor qué hace antes de continuar.

### Paso 1 — Importar la biblioteca

La primera línea de cualquier programa que use paho-mqtt es:

```python
import paho.mqtt.client as mqtt
```

`import` le dice a Python qué biblioteca necesita. El `as mqtt` es un nombre corto para
no tener que escribir `paho.mqtt.client` cada vez.

### Paso 2 — Definir la configuración

En lugar de escribir `"localhost"` o `1883` directamente dentro del código, los
guardamos en variables con nombres claros. Así si algo cambia, solo lo modificamos
en un lugar.

```python
BROKER = "localhost"
PORT   = 1883
TOPIC  = "observatory/weather"
```

### Paso 3 — Crear el cliente y conectarse

Aquí crearemos un objeto cliente MQTT y lo conectaremos al Broker.

```python
# Completar con el asesor
```

### Paso 4 — Publicar y desconectarse

Con la conexión establecida, publicaremos el mensaje y cerraremos la conexión
correctamente.

```python
# Completar con el asesor
```

---

## Parte 7. Ejecutar y verificar

Con el entorno virtual activo, ejecuta el programa:

```bash
python examples/<tu_usuario>/publisher.py
```

Revisa la terminal donde está corriendo `mosquitto_sub`. El mensaje debe aparecer ahí.

**Si no aparece, verifica:**
- ¿El Broker está corriendo?
- ¿El topic en tu código y en `mosquitto_sub` son exactamente iguales?
- ¿El entorno virtual está activo en la terminal donde ejecutas el programa?

### Experimenta

Una vez que funcione, prueba lo siguiente:

- Cambia el texto del mensaje y vuelve a ejecutar
- Cambia el topic y observa qué pasa en `mosquitto_sub`
- Publica dos mensajes distintos en el mismo script

---

## Parte 8. Guardar tu trabajo en Git

Revisa qué archivos cambiaron:

```bash
git status
```

Agrega los archivos de esta sesión:

```bash
git add examples/<tu_usuario>/publisher.py
git add requirements.txt
```

Crea el commit:

```bash
git commit -m "Add first MQTT publisher example"
```

Envía los cambios:

```bash
git push
```

---

## Preguntas de reflexión

1. ¿Qué hace la línea `import paho.mqtt.client as mqtt`?
Si no entiendo mal es para que la computadora o programa entienda que se ve a utilizar esa librería para ser más especificos el modulo de cliente dentro de esa librería el cual nos permitirá conectarnos o que al menos sepan que utilizaremos el broker.

2. ¿Por qué guardamos `BROKER`, `PORT` y `TOPIC` en variables en lugar de escribirlos
   directamente en el código?
   Tengo entendido que primero se escriben como mayusulas para diferenciar y decir que esas son constantes, para comenzar el BROKER es así para poder tener más movimiento al momento de poder conectarlo, puedes conectarlo tanto a la computadora local como a un servidor. El PORT es el que utilizan todos pero igual puede cambiar.

3. ¿Qué ocurre si ejecutas el publisher cuando el Broker no está en ejecución?
No sé con seguridad pero si no esta corriendo, puede que no llegue el mensaje a ningun lado o que el programa tenga una "falla" y no termine de copilar

4. ¿Para qué sirve el entorno virtual?
Nos sirve para tener aislado un proyecto y que no tenga problemas con otros proyectos, además nos ayuda a tener diferentes versiones de un mismo programa de ser necesario se puede crear un .venv con otra versión y que no afecte a la primera, es como aislar un pequeño sector para que no afecte el resto de mi computadora ni que el resto lo afecte a ese entorno.
5. ¿Qué pasaría si alguien clona el repositorio y ejecuta `pip install -r requirements.txt`?
Se replicará ese mismo repositorio en la otra computadora.
---

## Al finalizar debes tener

- [ ] Entorno virtual creado y activo
- [ ] VS Code usando el intérprete del entorno virtual
- [ ] paho-mqtt 2.1.0 instalado
- [ ] `requirements.txt` guardado en el repositorio
- [ ] `publisher.py` funcionando y publicando mensajes
- [ ] Cambios enviados con `git push`

## Para observar durante la visita al observatorio

Durante las actividades del fin de semana, observa si identificas situaciones donde diferentes equipos o programas necesiten intercambiar información.

No es necesario escribir un reporte ni programar nada.

El martes dedicaremos unos minutos a conversar sobre lo que observaste y cómo podría relacionarse con los conceptos vistos en el curso.