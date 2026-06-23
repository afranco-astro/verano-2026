import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "observatory/weather"

# Connect to the MQTT broker
client = mqtt.Client()
client.connect(BROKER, PORT)

# Publish a message to the topic
client.publish(TOPIC, "Temperature: 25 C")

# Disconnect from the broker
client.disconnect()