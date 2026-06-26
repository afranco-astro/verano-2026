¿Qué responsabilidad tiene el Weather Simulator?
**mandar los datos que se ocupan para el monitor, en este cas se utiliza como publisher que tiene que mandar un mensaje que es necesario para alguna parte del telescopio**

¿Qué responsabilidad tiene el Weather Monitor?
**Recibir el mensaje para poder procesar los datos, es el que se encarga de ser el subscriber**

¿Qué ocurriría si el Broker MQTT dejara de funcionar?
**No se enviaría ninguno de los datos que se estan mandando, así que tampoco recibiría nada de información**

¿Qué ventaja tiene utilizar JSON en lugar de enviar un solo número?
**Que se pueden mandar varia información sin algun problema de que se confundan los datos, mientras que de otra forma si se puede actualizar pero no se identifica correctamente que dato es de que**

En el Bloque 3 del Laboratorio 01 se mencionó que dewPointpodría terminar siendo mayor que temperature, algo imposible en una estación real. ¿Cómo lo resolverías?
**Podríamos reducir el rango del dewPoint para que eso no ocurra**

¿Qué componente del sistema podría sustituirse por una estación meteorológica real?
**todo el sistema del simulador porque podría darnos datos reales en lugar de inventarlos**



**INVESTIGACIÓN CORTA**
Investiga brevemente sobre Node-RED y responde únicamente:

¿Qué es?
**es una herramienta de programación visual de código (low-code). En lugar de escribir líneas de código tradicionales, utilizas una interfaz gráfica en tu navegador web donde arrastras y sueltas bloques llamados "nodos" para entradas y salidas que se conectan entre sí como si fueran cables para formar programas.**

¿Para qué se utiliza?
**Sirve principalmente para comunicar diferentes dispositivos y servicios entre sí, automatizar procesos y procesar datos en tiempo real. Este recibe información de una fuente, la procesa o condiciona visualmente y la envía hacia otro destino dependiendo para que funcione la información y a quien esta destinada.**

¿Por qué suele usarse junto con MQTT?
**ya que Node-RED incluye nodos nativos que permiten suscribirse o publicar en tópicos MQTT visualmente en segundos, consume pocos recursos, y facilita la transformación de los mensajes en  JSON que viajan por MQTT para conectarlos directamente a componentes gráficos y crear interfaces en tiempo real sin necesidad de programar código de interfaz.**
