# Práctica 02

## Introducción a MQTT utilizando Mosquitto

### Objetivo

Comprender el funcionamiento básico del modelo **Publish / Subscribe** utilizando un Broker
MQTT y clientes de consola, y ser capaz de describir el recorrido completo de un mensaje.

### Lo que necesitarás

- Mosquitto instalado (Broker + clientes de consola)
- MQTT Explorer instalado
- Tres ventanas de terminal abiertas simultáneamente

---

## Parte 1. Instalación de Mosquitto

Descarga Mosquitto para Windows desde la página oficial del proyecto e instálalo con las
opciones predeterminadas.

Al finalizar, verifica que los siguientes programas estén disponibles desde la terminal:

- `mosquitto` — el Broker
- `mosquitto_pub` — cliente para publicar mensajes
- `mosquitto_sub` — cliente para recibir mensajes

> **Nota:** En Windows, Mosquitto no siempre se agrega automáticamente al PATH del sistema.
> Si al ejecutar `mosquitto` en Git Bash obtienes un error de "command not found", investiga
> cómo agregar el directorio de instalación al PATH, o navega directamente a la carpeta de
> instalación antes de ejecutar los comandos.

---

## Parte 2. Configurar y arrancar el Broker

### El problema con Mosquitto 2.x

A partir de la versión 2.0, Mosquitto **no permite conexiones anónimas por defecto**. Si
intentas iniciarlo sin configuración y luego conectarte, obtendrás un error de conexión
rechazada aunque el Broker parezca estar corriendo.

Para esta práctica necesitas crear un archivo de configuración mínimo. Investiga:

- ¿Qué directivas de configuración permiten conexiones anónimas en Mosquitto 2.x?
- ¿Cómo se le indica a Mosquitto que use un archivo de configuración específico?

Las dos directivas que necesitas son `listener` y `allow_anonymous`.

> **Tip:** La documentación oficial de Mosquitto y su página de man son buenos puntos de
> partida. También puedes buscar el error exacto que te aparezca — es un problema muy
> común y bien documentado.

### Iniciar el Broker

Abre una terminal **Git Bash** e inicia el Broker con tu archivo de configuración.

Si todo funciona correctamente verás un mensaje similar a:

```
mosquitto version X.X.X starting
...
mosquitto version X.X.X running
```

**No cierres esta ventana.** El Broker debe permanecer en ejecución durante toda la práctica.

> **Problema frecuente:** Si ves el error `Address already in use` significa que el puerto
> 1883 ya está ocupado. Investiga qué proceso lo está usando y cómo detenerlo, o cómo
> configurar Mosquitto para usar un puerto diferente.

---

## Parte 3. Suscribirse a un Topic

Abre una **segunda** ventana de Git Bash.

Utiliza `mosquitto_sub` para suscribirte al topic `observatory/weather`.

Antes de ejecutar el comando, consulta la ayuda del programa para entender qué hace cada
flag:

```bash
mosquitto_sub --help
```

El programa debe quedar en espera de mensajes sin retornar al prompt.

> **Nota:** Si el Broker no está corriendo o la configuración de acceso anónimo no es
> correcta, `mosquitto_sub` mostrará un error de conexión. Verifica el estado del Broker en
> la primera ventana.

---

## Parte 4. Publicar un mensaje

Abre una **tercera** ventana de Git Bash.

Utiliza `mosquitto_pub` para publicar el siguiente mensaje en el topic `observatory/weather`:

```
Temperature 12.5 C
```

Consulta `mosquitto_pub --help` para conocer los flags necesarios.

Observa qué ocurre en la ventana donde ejecutaste `mosquitto_sub`.

**Pregunta:** ¿Qué tuvieron en común el comando de publicación y el de suscripción para que
el mensaje llegara?

---

## Parte 5. Publicar en un Topic diferente

Sin cerrar la suscripción a `observatory/weather`, publica el siguiente mensaje en un topic
distinto:

```
mosquitto_pub -t observatory/camera -m "Exposure Started"
```

**Pregunta:** ¿Qué ocurrió en la ventana de `mosquitto_sub`? ¿Por qué?

Escribe tu respuesta antes de continuar.

---

## Parte 6. Cambiar la suscripción

Detén `mosquitto_sub` con `Ctrl + C` y suscríbete ahora al topic `observatory/camera`.

Publica el siguiente mensaje:

```
mosquitto_pub -t observatory/camera -m "Exposure Finished"
```

Observa el resultado y compáralo con lo que ocurrió en la Parte 5.

---

## Parte 7. Suscripción con comodines

En la presentación viste el topic `observatory/camera/#`. El símbolo `#` es un **comodín**
que representa cualquier nivel de jerarquía a partir de ese punto.

Investiga qué comodines soporta MQTT y cuál es la diferencia entre `#` y `+`.

Luego realiza el siguiente experimento:

1. Suscríbete al topic `observatory/camera/#` en una ventana.
2. Desde otra ventana, publica mensajes en los siguientes topics:
   - `observatory/camera/temperature`
   - `observatory/camera/exposure`
   - `observatory/weather`
3. Observa qué mensajes recibe el Subscriber.

**Pregunta:** ¿Qué mensajes llegaron y cuáles no? ¿Por qué?

> **Nota:** Los Topics en MQTT son sensibles a mayúsculas y minúsculas.
> `Observatory/Camera` y `observatory/camera` son Topics distintos.

---

## Parte 8. Visualización con MQTT Explorer

MQTT Explorer es una herramienta gráfica que permite ver en tiempo real todos los Topics
y mensajes que fluyen por el Broker.

Abre MQTT Explorer y conéctate a tu Broker local. Los datos de conexión son:

- **Host:** `localhost`
- **Puerto:** `1883`
- Sin usuario ni contraseña (conexión anónima)

Una vez conectado:

1. Publica algunos mensajes desde la consola y observa cómo aparecen en el árbol de Topics.
2. Identifica los Topics que utilizaste durante la práctica.
3. Investiga si puedes publicar un mensaje directamente desde MQTT Explorer.

> **Nota:** Si los Topics aparecen vacíos o no ves mensajes anteriores, es porque por
> defecto MQTT no retiene mensajes. Solo verás mensajes que se publiquen *mientras* MQTT
> Explorer está conectado. Esto es comportamiento esperado.

---

## Preguntas de reflexión

1. ¿Cuál fue la función del Broker durante la práctica? ¿Qué pasaría si el Broker se
   detuviera mientras hay Publishers y Subscribers activos?

2. ¿Qué ocurre cuando un Publisher publica en un Topic para el cual no existen Subscribers
   en ese momento?

3. ¿Por qué los mensajes de `observatory/camera` no llegaron a la suscripción de
   `observatory/weather`?

4. ¿En qué situaciones sería útil usar el comodín `#`? ¿Y cuándo sería un problema usarlo?

5. ¿Qué ventaja tiene MQTT Explorer sobre `mosquitto_sub` para monitorear el sistema?

---

## Conclusión

Escribe un párrafo de entre 5 y 10 líneas describiendo el recorrido completo de un mensaje
MQTT: desde que el Publisher lo envía, cómo lo procesa el Broker, y cómo llega al Subscriber.
Incluye en tu descripción el papel que juegan los Topics en ese proceso.
