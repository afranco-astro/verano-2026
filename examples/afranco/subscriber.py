import paho.mqtt.client as mqtt

BROKER= "test.mosquitto.org"
PORT= 1883
TOPIC= "observatory/weather"

def on_message(client, userdata, message):
    try:
        print("Topico: " + message.topic)
        print("Payload: " + message.payload.decode("utf-8"))
    except Exception as ex:
        print("Error: ", ex)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect(BROKER, PORT)

client.subscribe(TOPIC)

client.loop_forever()
