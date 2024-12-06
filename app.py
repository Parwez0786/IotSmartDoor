from flask import Flask, render_template, request, redirect, url_for
from flask_mqtt import Mqtt
import cloudinary
import cloudinary.uploader
import os
from flask_mail import Mail, Message
from threading import Thread
import traceback

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)

# Cloudinary Configuration
cloudinary.config(
    cloud_name='dtehrjclq',
    api_key='332114166428677',
    api_secret='Ibg3iwFonii43mIB0hVEXiAJ-uc',
    secure=True
)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dbmsproject09@gmail.com'
app.config['MAIL_PASSWORD'] = 'zhjeutybhujsmqhj'  # Ensure this is secure
app.config['MAIL_DEFAULT_SENDER'] = ('Iot', 'parwezansari1024@gmail.com')

mail = Mail(app)  # Initialize Flask-Mail

latest_image_url = None

IMAGE_TOPIC = "test/iot/image/door"
COMMAND_TOPIC = "test/iot/door/command"

# Define the recipient email
RECIPIENT_EMAIL = 'parwezansari1024@gmail.com'

def send_async_email(app, recipient, subject, html_body):
    """
    Sends an HTML email asynchronously within the Flask application context.
    """
    try:
        with app.app_context():
            msg = Message(subject=subject, recipients=[recipient])
            msg.html = html_body  # Include the HTML body
            mail.send(msg)
            print(f"Notification email sent to {recipient}.")
    except Exception as email_error:
        print(f"Failed to send email notification: {email_error}")
        traceback.print_exc()

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        mqtt.subscribe(IMAGE_TOPIC)
        print(f"Subscribed to topic: {IMAGE_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global latest_image_url
    if message.topic == IMAGE_TOPIC:
        img_byte_array = message.payload
        if img_byte_array:
            try:
                # Ensure the static/images directory exists
                os.makedirs('static/images', exist_ok=True)

                # Save the received image data to a file within the static folder
                image_path = os.path.join('static', 'images', 'received_image.jpg')
                with open(image_path, 'wb') as f:
                    f.write(img_byte_array)
                print(f"Image saved successfully as '{image_path}'.")

                # Check if the file is not empty
                if os.path.getsize(image_path) > 0:
                    with app.app_context():  # Ensure app context
                        # Upload the image to Cloudinary
                        result = cloudinary.uploader.upload(image_path)
                        latest_image_url = result.get('secure_url')
                        print(f"Image uploaded to Cloudinary: {latest_image_url}")

                        subject = "Knock - Knock"

                        # Render the HTML template inside app context
                        html_body = render_template('email_template.html', image_url=latest_image_url)
                        print("Rendered email_template.html successfully.")

                        # Send the email asynchronously
                        email_thread = Thread(target=send_async_email, args=(app, RECIPIENT_EMAIL, subject, html_body))
                        email_thread.start()
                        print("Started email sending thread.")
                else:
                    print("The received image file is empty.")
            except Exception as e:
                print(f"Error processing image: {e}")
                traceback.print_exc()
        else:
            print("Received empty payload on IMAGE_TOPIC.")
    else:
        print(f"Unhandled topic: {message.topic}")

@app.route('/')
def index():
    return render_template('index.html', image_url=latest_image_url)

@app.route('/command', methods=['POST'])
def send_command():
    command = request.form.get('command')
    print(f"Received command: {command}")
    mqtt.publish(COMMAND_TOPIC, command)
    print(f"Published command: {command} to topic: {COMMAND_TOPIC}")
    return render_template('index.html')

@app.route('/latest_image_url')
def get_latest_image_url():
    return {'image_url': latest_image_url}

if __name__ == '__main__':
    # Disable the reloader to prevent multiple instances
    app.run(debug=True, use_reloader=False)
