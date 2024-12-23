# # flask_app.py
# from flask import Flask, request, jsonify
# from twilio.rest import Client
# import os
# from dotenv import load_dotenv

# # ----------------------
# # Load Environment Variables
# # ----------------------
# load_dotenv()

# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
# USER_WHATSAPP_NUMBER = os.getenv("USER_WHATSAPP_NUMBER")

# # Flask App for Webhook
# app = Flask(__name__)

# # Twilio client
# twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# # Function to send WhatsApp message
# def send_whatsapp_message(message):
#     try:
#         twilio_client.messages.create(
#             body=message,
#             from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
#             to=f'whatsapp:{USER_WHATSAPP_NUMBER}'
#         )
#     except Exception as e:
#         print(f"Error sending WhatsApp message: {e}")

# # Flask route to handle incoming WhatsApp messages
# @app.route("/webhook", methods=["POST"])
# def whatsapp_webhook():
#     incoming_message = request.form.get('Body')
#     if incoming_message:
#         send_whatsapp_message(f"Received message: {incoming_message}")
#     return jsonify({"status": "received"})


# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)




# # flask_app.py
# from flask import Flask, request, jsonify
# from twilio.rest import Client
# import os
# from dotenv import load_dotenv

# # ----------------------
# # Load Environment Variables
# # ----------------------
# load_dotenv()

# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
# USER_WHATSAPP_NUMBER = os.getenv("USER_WHATSAPP_NUMBER")

# # Flask App for Webhook
# app = Flask(__name__)

# # Twilio client
# twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# # Function to send WhatsApp message
# def send_whatsapp_message(message):
#     try:
#         twilio_client.messages.create(
#             body=message,
#             from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
#             to=f'whatsapp:{USER_WHATSAPP_NUMBER}'
#         )
#     except Exception as e:
#         print(f"Error sending WhatsApp message: {e}")

# # Flask route to handle incoming WhatsApp messages
# @app.route("/webhook", methods=["POST"])
# def whatsapp_webhook():
#     incoming_message = request.form.get('Body')
#     print(f"Received message: {incoming_message}")  # Debugging line to check incoming message
    
#     if incoming_message:
#         send_whatsapp_message(f"Received message: {incoming_message}")
    
#     return jsonify({"status": "received"})

# # Home route for testing (Optional, to ensure Flask is running)
# @app.route('/')
# def home():
#     return "Flask app is running!"

# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)


















from flask import Flask, request, jsonify
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
USER_WHATSAPP_NUMBER = os.getenv("USER_WHATSAPP_NUMBER")

# Flask app initialization
app = Flask(__name__)

# Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to send WhatsApp message
def send_whatsapp_message(message):
    try:
        twilio_client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{USER_WHATSAPP_NUMBER}'
        )
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# Home route for testing
@app.route('/')
def home():
    return "Flask app is running!"

# Webhook route for incoming WhatsApp messages
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_message = request.form.get('Body')
    print(f"Received message: {incoming_message}")  # Debugging line
    
    if incoming_message:
        send_whatsapp_message(f"Received message: {incoming_message}")
    
    return jsonify({"status": "received"})

# Run the app with debugging
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
