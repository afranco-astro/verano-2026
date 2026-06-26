# Challenge — Día 07

## Construye el simulador de cúpula

---

## Contexto

El sistema de monitoreo del observatorio no solo necesita datos del clima. La **cúpula**
es uno de los componentes más visibles del observatorio: su posición debe sincronizarse
con el apuntado del telescopio, y su estado (abierta, cerrada, en movimiento) es
información crítica durante una noche de observación.

Tu tarea es construir un simulador para la cúpula del observatorio y visualizar sus
datos en el Dashboard de Node-RED.

---

## Lo que debes construir

Crea el archivo:

```text
simulators/dome_simulator.py
```

El simulador debe cumplir los siguientes requisitos:

- Publicar mediante MQTT cada segundo.
- Utilizar el Topic `oan/dome`.
- El payload debe ser un JSON con al menos estas tres variables:

| Variable  | Tipo    | Descripción                                           |
|-----------|---------|-------------------------------------------------------|
| `azimuth` | float   | Posición de la cúpula en grados (0.0 a 360.0)        |
| `isOpen`  | boolean | Si la abertura de la cúpula está abierta o cerrada   |
| `status`  | string  | Estado actual: `"tracking"`, `"parked"` o `"slewing"`|

---

## Punto de partida

Ya tienes un simulador funcionando: `weather_simulator.py`. No empieces desde cero —
revísalo y adapta lo que necesites. Los desarrolladores reutilizamos componentes
existentes y los modificamos para un nuevo problema; eso es exactamente lo que harás aquí.

---

## Dashboard

Una vez que el simulador esté publicando, agrega los datos de la cúpula al Dashboard
de Node-RED que construiste esta mañana.

Decide tú cómo visualizarlo — no hay una única respuesta correcta. Puedes usar los
mismos tipos de nodos que ya conoces (Gauge, Change) u explorar alguno nuevo.

---

## Al finalizar, registra tus cambios

```bash
git add simulators/dome_simulator.py
git commit -m "Add dome simulator"
git push
```

---

## Para el lunes

Al inicio de la sesión revisaremos:

- El simulador que construiste: cómo elegiste simular cada variable y por qué.
- Cómo lo integraste en el Dashboard.
- Cualquier duda o decisión de diseño que hayas tomado.

No importa si quedó incompleto — lo que más vale es lo que puedas explicar sobre lo
que hiciste y lo que intentaste.
