# Challenge — Día 08

## Observatory Monitoring Dashboard

---

## Contexto

Esta mañana construiste tres nuevos simuladores que representan los instrumentos
principales del observatorio: la montura del telescopio, la cámara CCD y el sistema de
guiado. Junto con el simulador de clima y el de cúpula que ya tenías, el sistema ahora
genera datos de cinco fuentes distintas simultáneamente.

Tu reto de esta tarde es integrar todos esos datos en un único dashboard en Node-RED.

---

## Lo que debes construir

Un dashboard en Node-RED que muestre, en tiempo real, el estado del observatorio
completo. No hay una única forma correcta de organizarlo — las decisiones de diseño
son tuyas.

Para completar el reto, el dashboard debe mostrar al menos **una visualización de
cada simulador**:

| Simulador        | Topic         | Al menos un dato visible en el dashboard |
|------------------|---------------|------------------------------------------|
| Weather Station  | `oan/weather` | Ya tienes esto del Lab 03                |
| Dome             | `oan/dome`    | Challenge del día anterior               |
| Telescope Mount  | `oan/mount`   | Nuevo hoy                                |
| CCD Camera       | `oan/camera`  | Nuevo hoy                                |
| Guider           | `oan/guider`  | Nuevo hoy                                |

---

## Cómo empezar

Antes de abrir Node-RED, abre **cinco terminales** y ejecuta un simulador en cada una:

```bash
python simulators/weather_simulator.py
```
```bash
python simulators/dome_simulator.py
```
```bash
python simulators/mount_simulator.py
```
```bash
python simulators/camera_simulator.py
```
```bash
python simulators/guider_simulator.py
```

Verifica en MQTT Explorer que los cinco topics están recibiendo datos antes de continuar.

---

## Sugerencias por simulador

Estas son ideas — no instrucciones. Puedes usarlas, ignorarlas o mezclarlas con tus
propias ideas.

**Weather Station** — ya tienes gauges de las cinco variables. Puedes reorganizarlos
o dejarlos como están.

**Dome** — un gauge de azimut (0–360°) y algún indicador para `isOpen` y `status`.

**Telescope Mount** — los campos de texto (`ra`, `dec`, `ha`) se muestran bien con un
nodo `ui_text`. Para `alt` y `az` puedes usar gauges. Para `limitWarning` explora el
nodo `ui_led` o un nodo `ui_text` con color condicional usando un nodo `switch` antes.

**CCD Camera** — `exposureProgress` es ideal para una barra de progreso (`ui_gauge` en
modo "donut" o `ui_chart`). `status` y `filter` como texto. `temperature` como gauge
con rango −30 a +20 °C.

**Guider** — `rmsRA` y `rmsDec` como texto o gauges pequeños. `guiding` y `starLocked`
como indicadores de estado (verde / rojo).

---

## Criterio de éxito

Al finalizar deberías poder tomar un screenshot del dashboard con los cinco simuladores
corriendo y que alguien externo pueda entender qué está pasando en el observatorio solo
con verlo.

---

## Al finalizar, registra tus cambios

Node-RED guarda los flujos automáticamente en tu máquina. Si modificaste algún
simulador durante la tarde, regístralo:

```bash
git status
git add simulators/<archivo_modificado>.py
git commit -m "Update simulator / dashboard work"
git push
```

---

## Para el martes

Al inicio de la sesión revisaremos el dashboard juntos. Prepárate para explicar:

- ¿Cómo organizaste la información? ¿Por tabs, por sección, todo en una sola pantalla?
- ¿Qué fue lo más difícil de visualizar y cómo lo resolviste?
- ¿Hay algún dato que no supiste cómo mostrar?

El martes dedicaremos tiempo a dejar el dashboard presentable para la demostración final.
