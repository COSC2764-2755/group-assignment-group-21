from sense_hat_handler import show_fault_warning
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "security/alerts"


def on_connect(client, userdata, flags, rc):
    print("[SECURITY] Connected")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    message = msg.payload.decode()

    print(f"[SECURITY ALERT] {message}")

    show_fault_warning()

    # later: trigger Sense HAT here


def start():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    start()