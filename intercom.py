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
        sleep(10)
        print('door locked')
        client.disconnect()
    elif request == 'n':
        print('door access not granted :(')
        client.disconnect()
    else:
        pass


def intercom_listen(topic, client):
    client.loop_start()
    client.subscribe(topic)
    print(f'subscribed to: {topic}')


    client.on_message = on_message
    sleep(60)

    client.unsubscribe(topic)
    client.disconnect()
    print('disconnecting from broker...')


def main():

    #mqttBroker = "mqtt.eclipseprojects.io"
    mqttBroker = broker

    roomNumber = str(input('input room number: '))
    print('\n')

    cmdPrompt = 'input: \n1 - to request door access \n2 - to request chat \n'
    cmd = str(input(cmdPrompt))
    print('\n')

    intercom=mqtt.Client('intercom')
    intercom.username_pw_set(username="edwin", password="ids_2021")

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
    
    
if __name__ == "__main__":
    main()
