Preguntas

1. ¿Qué partes del código son prácticamente iguales en Publisher y Subscriber?
**La importación de la librería, la parte donde identificamos el broker, topic en teoría si quieres que esten comunicados debería ser igual sino igual tienen el mismo formato, el puerto al que se conecta, también la parte donde se conecta al broker es similar en uno de los comandos y el otro es igual.**

2. ¿Qué partes cambian entre ambos programas?
**que para uno se debe definir el mensaje que se quiere enviar mientras que el otro para recibirlo se tiene que asegurar que el mensaje recibido pueda ser leido y se cambie al formato correcto para que pueda ser obtenido. Por otro lado el publisher si se debe desconectar en algun momento con un comando, mientras el subscriber se debe mantener activo debido a que se necesitan recibir activamente los mensajes.**

3. ¿Cuál es la función de `on_message` durante la práctica? ¿Quién la ejecuta y cuándo?
**Identificar cual es el mensaje que esta utilizando es como una variable que tiene la recepción de los datos envaidos por el broker, luego lo cambia para tener el mismo formato y poder transmitirlo en pantalla, pra su ejecución por eso lo tenemos en la librería ese comando, por otro lado este se ejecuta de forma automática cada vez que llega un mensaje nuevo al tópico** 

4. ¿Por qué el Subscriber nunca termina por sí solo, mientras que el Publisher sí?
**porque el subscriber tiene que seguir recibiendo mensajes y terminarlo seria como cortar el recibir información requerida o en dado caso perder información en lo que conecta y desconecta del broker, mientras que el publisher como es el que manda la información él puede desconectarse cada cierto tiempo si no necesita nada para mandarle la información**

5. Si mañana quisieras desarrollar un simulador de un instrumento astronómico, ¿partirías
   del Publisher o del Subscriber? Explica por qué.
   **En el publisher se puedeidentificar primero cual es el mensaje, cual es el topic y a donde quieres mandarlo, pero en lo personal creo que es mejor iniciar con el subscriber podría ayudarnos a tener claro que es lo que necesita cada uno de los sistemas y que información necesita para operar, sin mencionar que también se puede utilizar para identificar los topicos necesarios y ordenarlos, así que con todo eso expuesto creo que la mejor opción de inicio es el Subscriber.**
