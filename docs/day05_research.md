1. MQTT vs HTTP

**Investiga y explica:**
● ¿Qué es HTTP?
Es un protocolo como su nombre lo indica (Protocolo de Transferencia de Hipertexto) es el conjunto de reglas que permite la comunicación entre el cliente y los servidores. Este  funciona como un sistema de petición y respuesta (Request-Response) entre dos actores principales que son como mencioné antes el cliente y el servidor. Ese fuciona primero mandando una solicitud HTTP al servidor donde se aloja la página mientras que este a su vez recibe la petición, la procesa y le devuele al cliente con el código de estado para de esa forma mostrar la página. Algunos conceptos claves son:

- Código de estado:  Son números de tres dígitos que indican si la petición tuvo éxito o falló. 

- Cliente: El dispositivo que inicia la comunicación solicitando algo.

- Servidor: La computadora remota que almacena los datos, recibe la solicitud del cliente, la procesa y le devuelve una respuesta.

En este tipo de protocolos el servidor nunca podrá enviar información primero sin que reciba una indicación del usuario que los necesita.

● ¿Qué es MQTT?
Es un protocolo de comunicación diseñado principalmente para ser ultraligero, rápido y consume una cantidad mínima de datos y batería, en este los usuarios no se comunican directamente entre si, sino que se utiliza una comunación por medio de un broker el cual manda la información desde un usuario que publica un mensaje al broker, el broker la distribuye para los usuarios en este caso subscriber que quieren recibir esta información. Este consta de 3 elementos principales dos de ellos son clientes y un es el broker. Este utiliza un sistema publisher-suscribe.

● Menciona al menos tres diferencias entre ambos protocolos.
El primero de ellos es el modelo de comunicación que utilizan ambos uno utiliza el (petición-respuesta) y el otro (publusher-subscribe), por otro lado el MQTT tiene que mantenerce encendido para que el subscriber reciba mensajes cada cierto momento mientras que con el HTTP se puede mantener desconectado hasta que le den otra indicación el usuario. Para finalizar el http usa más ancho de banda al ser utilizado.

● ¿En qué situaciones utilizarías MQTT en lugar de HTTP?
En cualquier escenario donde los recursos sean limitados utilizaría MQTT porque es menos pesado que el HTTP, aunque también donde se tengan muchos usuarios pidiendo la misma información al mismo tiempo se podría utilizar mejor el MQTT para mandar el mensaje a todos.



2. Eclipse Mosquitto y Eclipse Paho
Investiga y explica:
● ¿Qué es Eclipse Mosquitto?
Es un Broker de MQTT de código abierto que puede servir como broker o como intermediario.Su tarea principal es recibir, filtrar y distribuir los mensajes a los subscriber que lo necesiten.

● ¿Qué es Eclipse Paho?
Es una parte de una librería que te brinda herramientas y funciones ya programadas para que se pueda seguir con ciertos comandos el protocolo de MQTT, sin esto tendrías que programar desde cero toda la lógica detrás de esto para poder conceta ral broker y crear un cliente.

● ¿Qué papel desempeña cada uno dentro de nuestro proyecto?
EL eclipse mosquitto en nuestro pproyecto se utiliza como broker para que los demás programas en python realizados con eclipse paho puedan ser utilizados correctamente en el subscriber y en el publisher.



3. MQTT fuera de la astronomía
Busca tres ejemplos reales donde se utilice MQTT.


Ejemplo 1: Sistema de casa inteligente
Para cada ejemplo describe brevemente:
● Qué información se intercambia.
● Por qué MQTT resulta una buena opción.
La información que intercambian son más comandos de control y para concer el estado de los sensores, el MQTT sería bueno ya que al tener varios dispositivos y sensores estos al ser necesario podrían estar conectados al mismo topic y así poder encenderse al mismo tiempo, de esa forma puede controlar y regular que se apaga y que no.

Ejemplo 2: Para comunicación de la telemetría en pruebas de motor
En algunas pruebas es necesario comunicar cuándo abrir las válvulas para que el motor pueda hacer una prueba; para esto, la aviónica principal actúa como el publisher enviando comandos hacia un broker central, el cual se encarga de transmitir de forma inmediata el mensaje al sistema de control del motor para que abra o cierre las válvulas. MQTT resulta la opción ideal ya que puede entregar las instrucciones  en tiempo real, de manera obligatoria y sin duplicados en la red, asegurando la sincronización crítica del flujo de combustible.


Ejemplo 3: Prueba de telemetría para obtención de datos en el vuelo
Durante la fase de vuelo es importante transmitir las lecturas de los sensores hacia la estación en tierra, por lo que la aviónica a bordo actúa como el publisher, transmitiendo constantemente los datos a través de un enlace hacia el broker ubicado en la estación base, el cual distribuye la información a las pantallas de monitoreo. Este es ideal porque es ligero de banda ancha y permite que la comunicación sea constante.

4. Relación con el observatorio
Durante tu visita al OAN-SPM observaste distintos
sistemas e instrumentos.
- Para los sensores del telescopio cuando indican que ya se ha movido correctamente este podrían pasarlos al broker que posteriormente le indica a la consola que se ha movido correctamente el telescopio a la posición que necesitaba, si no se usara de esa forma se tendría que tener un proceso de conectar y desconectar muy complicado que si se hace mal podría afectar a las capacidades mecánicas del telescopio.

- Cuando tienen que mandar un mensaje el guiador al telescopio cuando le indica constantemente que se mueva con él en ciertas coordenadas, pensaria porque es un proceso amplio y no tan rapido ya que es algo constante que se hace.

Describe al menos dos situaciones donde consideres que MQTT podría ser utilizado para intercambiar información. No es necesario que el sistema realmente use MQTT; lo importante es justificar tu respuesta.