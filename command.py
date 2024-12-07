import paho.mqtt.client as mqtt
import time
import sys

# MQTT Broker Details
BROKER = "broker.hivemq.com"  # Free public broker
PORT = 1883
TOPIC = "test/iot/door/command"  # Topic for the message

# MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Broker successfully.")
        # Publish the message after connecting
        client.publish(TOPIC, userdata['message'])
        print("Message published successfully.")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

def main(message):
    # Create MQTT client with userdata to pass the message
    client = mqtt.Client(userdata={'message': message})
    
    # Assign callback functions
    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        # Connect to the MQTT Broker
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # Start the loop and wait until the message is published
    client.loop_start()

    # Wait sufficient time to ensure message is sent
    time.sleep(2)

    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    # Check if a message was provided as a command-line argument
    if len(sys.argv) > 1:
        message_to_publish = ' '.join(sys.argv[1:])
    else:
        # Default message if none provided
        message_to_publish = "Hello, kya haal."

    main(message_to_publish)
