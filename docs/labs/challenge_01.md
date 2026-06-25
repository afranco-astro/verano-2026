# Retos del bloque de la tarde — Día 06

## Explorando el sistema Simulator + Monitor

Hoy en la mañana construiste un sistema funcional: el `weather_simulator.py` publicando
datos continuamente y el `weather_monitor.py` recibiéndolos. Esta tarde no hay una
práctica larga que seguir paso a paso — son **retos cortos** para que explores el sistema
por tu cuenta y empieces a tomar pequeñas decisiones de diseño.

---

## Reto 1 — Personaliza el simulador

Realiza al menos **tres modificaciones** a `weather_simulator.py`.

Algunas ideas:

- Agregar una nueva variable, por ejemplo `cloudCover` (porcentaje de nubosidad) o
  `rainRate` (mm/h).
- Cambiar los rangos de alguna de las variables existentes.
- Publicar en un Topic diferente.
- Modificar el intervalo de publicación (`time.sleep`).

Verifica que el monitor continúa funcionando correctamente después de cada cambio.

> Si agregas una variable nueva, el monitor no la va a mostrar todavía — eso es
> intencional, lo resuelves en el Reto 2.

---

## Reto 2 — Mejora el monitor

Realiza al menos **dos mejoras** a `weather_monitor.py`.

Por ejemplo:

- Mostrar cualquier variable nueva que agregaste al simulador en el Reto 1.
- Mostrar el Topic del mensaje recibido (no solo su contenido).
- Agregar un contador de mensajes recibidos desde que se inició el monitor.
- Cambiar el formato de salida para que sea más legible.

---

## Reto 3 — Analiza el sistema

Responde brevemente en un archivo:

```text
docs/day06_notes.md
```

### Preguntas

1. ¿Qué responsabilidad tiene el Weather Simulator?
2. ¿Qué responsabilidad tiene el Weather Monitor?
3. ¿Qué ocurriría si el Broker MQTT dejara de funcionar?
4. ¿Qué ventaja tiene utilizar JSON en lugar de enviar un solo número?
5. En el Bloque 3 del Laboratorio 01 se mencionó que `dewPoint` podría terminar siendo
   mayor que `temperature`, algo imposible en una estación real. ¿Cómo lo resolverías?
6. ¿Qué componente del sistema podría sustituirse por una estación meteorológica real?

---

## Reto 4 — Investigación corta (preparación para la siguiente sesión)

Investiga brevemente sobre **Node-RED** y responde únicamente:

- ¿Qué es?
- ¿Para qué se utiliza?
- ¿Por qué suele usarse junto con MQTT?

No es necesario instalarlo todavía — solo tener una idea clara de su papel.

---

## Lo que revisaremos al inicio de la siguiente sesión

- Las mejoras realizadas al simulador.
- Las mejoras realizadas al monitor.
- Las respuestas del documento `day06_notes.md`.
- La investigación sobre Node-RED.
