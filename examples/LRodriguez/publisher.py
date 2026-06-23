import paho.mqtt.client as mqtt

BROKER= "localhost"
PORT= 1883
TOPIC= "observatory/weather"

client= mqtt.Client() #CONECTA AL BROKER
client.connect(BROKER, PORT) #CONECTA AL BROKER

#PUBLICAR MENSAJE
client.publish(TOPIC, "Temperature: 25 C")
print("mensaje publicado")
#Disconnect from broker
client.disconnect()
