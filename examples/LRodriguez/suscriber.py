import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883
TOPIC  = "observatory/weather"

def on_message(client, userdata, message):
        print("Topic:" +message.topic)
        print("Payload: " + message.payload.decode("utf-8"))
   

client= mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message= on_message

client.connect(BROKER, PORT) #CONECTA AL BROKER
client.subscribe(TOPIC) #Ayuda a conectar o saber que topico usar
client.loop_forever() # hace que siga en loop sin pararse

