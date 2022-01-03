import paho.mqtt.client as mqtt
from personal_broker import broker
from time import sleep


def intercom_pub(topic, msg, broker, port, client):
    client.connect(broker, port)
    print('connected to broker')
    client.publish(topic, msg)
    print(f'just published: {msg}')


def on_message(client, userdata, msg):
    request = str(msg.payload.decode("utf-8"))

    if request == 'y':
        print('door unlocked!')
        sleep(5)
        print('door locked')
    elif request == 'n':
        print('door access not granted :(')
    else:
        pass

    print('\n')
 

def intercom_listen(topic, client):

    client.loop_start()
    client.subscribe(topic)
    print(f'subscribed to: {topic}')

    client.on_message = on_message # not synchronous, we just activated it
    sleep(10) # whenever a callback is received, wait 10 seconds before stopping the loop

    client.loop_stop()



def main():
    mqttBroker = broker
    intercom=mqtt.Client('intercom')
    intercom.username_pw_set(username="edwin", password="ids_2021")

    cmd = '1'
    while cmd == '1':

        roomNumber = str(input('input room number: '))
        print('\n')

        cmdPrompt = 'input: \n1 - to request door access \n2 - to close connection \n'
        cmd = str(input(cmdPrompt))
        print('\n')

        if cmd == '1':
            intercom_pub(
                        topic=f'gdsc_iot2/{roomNumber}',
                        msg=cmd,
                        broker=mqttBroker,
                        port=1883,
                        client=intercom
                        )

            intercom_listen(
                            topic=f'gdsc_iot2/{roomNumber}',
                            client=intercom
                            )
        
        else:
            pass

    
if __name__ == "__main__":
    main()
