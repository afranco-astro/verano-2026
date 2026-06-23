import paho.mqtt.client as mqtt

BROKER= "localhost"
PORT= 1883
TOPIC= "observatory/weather/camera"

client= mqtt.Client() #CONECTA AL BROKER
client.connect(BROKER, PORT) #CONECTA AL BROKER

#PUBLICAR MENSAJE
client.publish(TOPIC, "imagen correcta")
print("mensaje publicado")
#Disconnect from broker
client.disconnect()
