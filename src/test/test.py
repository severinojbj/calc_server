import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe ("test")
        #client.publish ("test", "start")
            
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg): 
    print(msg.topic+" "+str(msg.payload))
    msg_send = str(msg.payload)
    print (msg_send)
    
    
if __name__ == '__main__':
    client = mqtt.Client()
    client.connect ("192.168.0.103", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    