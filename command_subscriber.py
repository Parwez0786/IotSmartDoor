import paho.mqtt.client as mqtt

# Configuration Variables
MQTT_BROKER = "broker.hivemq.com"  # Public MQTT broker
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
COMMAND_TOPIC = "test/iot/door/command"

# Optional: Define actions based on commands
def handle_command(command):
    command = command.lower()
    if command == "open":
        print("Received command to OPEN the door.")
        # Add your door opening logic here
    elif command == "close":
        print("Received command to CLOSE the door.")
        # Add your door closing logic here
    else:
        print(f"Received unknown command: {command}")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(COMMAND_TOPIC)
        print(f"Subscribed to topic: {COMMAND_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    try:
        command = msg.payload.decode('utf-8').strip()
        print(f"Received message on topic '{msg.topic}': {command}")
        handle_command(command)
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Create an MQTT client instance
    client = mqtt.Client()

    # Assign callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # Connect to the MQTT broker
        client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    except Exception as e:
        print(f"Could not connect to MQTT Broker: {e}")
        return

    # Start the network loop and process callbacks
    try:
        print("Starting MQTT subscriber loop...")
        client.loop_forever()
    except KeyboardInterrupt:
        print("Subscriber stopped by user.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
