import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "observatory/weather"

# Connect to the MQTT broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

# Publish a message to the topic
client.publish(TOPIC, "Temperature: 36 C")

print("Mensaje publicado")

# Disconnect from the broker
client.disconnect()