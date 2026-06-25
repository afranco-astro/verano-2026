import json 
from datetime import datetime 
import paho.mqtt.client as mqtt

BROKER= "localhost"
PORT= 1883
TOPIC= "oan/weather"
client= mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_message(client, userdata, message):

    data = json.loads(message.payload.decode())
    timestamp = datetime.now().strftime("%H:%M:%S") #nos indica en que momento de a hora se esta utilizando 

    print("--------------------------------")
    print(f"Received at : {timestamp}") #nos da la hora impresa junto con los datos
    print(f"Temperature : {data['temperature']['value']} °{data['temperature']['unit']}")
    print(f"Humidity    : {data['humidity']} %")
    print(f"Wind Speed  : {data['windSpeed']} m/s")
    print(f"Pressure    : {data['pressure']} hPa")
    print(f"Dew Point   : {data['dewPoint']} °C")


client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_forever()