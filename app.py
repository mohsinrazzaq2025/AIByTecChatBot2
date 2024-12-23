import streamlit as st
import openai
import os
import requests
import subprocess
from flask import Flask, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

# ----------------------
# Load Environment Variables
# ----------------------
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
USER_WHATSAPP_NUMBER = os.getenv("USER_WHATSAPP_NUMBER")
PDF_PATH = "./Aibytec fine tuned data.pdf"
WEBSITE_URL = os.getenv("WEBSITE_URL")

# ----------------------------
# Flask App for WhatsApp Webhook
# ----------------------------
app = Flask(__name__)

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(message):
    try:
        twilio_client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{USER_WHATSAPP_NUMBER}'
        )
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_message = request.form.get('Body')
    print(f"Received message: {incoming_message}")  # Debugging line
    
    if incoming_message:
        send_whatsapp_message(f"Received message: {incoming_message}")
    
    return jsonify({"status": "received"})

# Start Flask in a separate process
def start_flask():
    subprocess.Popen(["flask", "run", "--host=0.0.0.0", "--port=5000"])

# -------------------------
# Streamlit Chatbot Interface
# -------------------------
# Function to extract PDF text
def extract_pdf_text(file_path):
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"Error scraping website: {e}"

# Function to generate OpenAI response
def chat_with_ai(user_question, website_text, pdf_text, chat_history):
    combined_context = f"Website Content:\n{website_text}\n\nPDF Content:\n{pdf_text}"
    messages = [{"role": "system", "content": "You are a helpful assistant. Use the provided content."}]
    for entry in chat_history:
        messages.append({"role": "user", "content": entry['user']})
        messages.append({"role": "assistant", "content": entry['bot']})
    messages.append({"role": "user", "content": f"{combined_context}\n\nQuestion: {user_question}"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=False
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit UI
st.set_page_config(page_title="Chatbot with WhatsApp Support", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history
for entry in st.session_state['chat_history']:
    st.markdown(
        f"""
        <div style="background-color: #78bae4; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
            {entry['user']}
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="background-color:  #D3D3D3; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
            {entry['bot']}
        </div>
        """, 
        unsafe_allow_html=True
    )

# Load PDF and Website content once
pdf_text = extract_pdf_text(PDF_PATH) if os.path.exists(PDF_PATH) else "PDF file not found."
website_text = scrape_website(WEBSITE_URL)

user_input = st.chat_input("Type your question here...", key="user_input_fixed")

if user_input:
    with st.spinner("Generating response..."):
        bot_response = chat_with_ai(user_input, website_text, pdf_text, st.session_state['chat_history'])
    st.session_state['chat_history'].append({"user": user_input, "bot": bot_response})
    st.rerun()

# Start Flask app when the script runs
if __name__ == "__main__":
    start_flask()
