# streamlit_app.py
import streamlit as st
import openai
import os
from dotenv import load_dotenv
import requests

# ----------------------
# Load Environment Variables
# ----------------------
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
PDF_PATH = os.getenv("PDF_PATH")
WEBSITE_URL = os.getenv("WEBSITE_URL")

# Function to extract PDF text
def extract_pdf_text(file_path):
    try:
        with open(file_path, "rb") as file:
            from PyPDF2 import PdfReader
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
        from bs4 import BeautifulSoup
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

