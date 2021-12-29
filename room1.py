import paho.mqtt.client as mqtt
from personal_broker import broker
from time import sleep


def room_pub(topic, msg, client):
    client.publish(topic, msg)
    print(f'just published: {msg}')


def on_message(client, userdata, msg):
    request = str(msg.payload.decode("utf-8"))

    if request == '1':
        grant = str(input('intercom asking for door access, grant? (y/n): '))

        roomNumber = '2'
        room_pub(
                topic=f'gdsc_iot2/{roomNumber}',
                msg=grant,
                client=client
                )

    else:
        pass


def room_listen(client, topic, broker, port):
    
    client.connect(broker, port)
    print('connected to broker')
    
    client.loop_start()

    client.subscribe(topic)
    print(f'subscribed to: {topic}')

    client.on_message = on_message

    sleep(30)

    client.unsubscribe(topic)
    client.disconnect()
    print('disconnecting from broker...')


def main():
    #mqttBroker = "mqtt.eclipseprojects.io"
    mqttBroker = broker
    
    
    roomNumber = '1'
    room1=mqtt.Client(f'room {roomNumber}')
    room1.username_pw_set(username="edwin", password="ids_2021")

    room_listen(
                topic=f'gdsc_iot2/{roomNumber}',
                broker=mqttBroker,
                port=1883,
                client=room1
                )
    

if __name__ == "__main__":
    main()
