import streamlit as st
import openai
import os
import schedule
import time
import threading
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dictionary to store medication schedules
drug_schedule = {}

# Function to generate chatbot response
def chatbot_response(prompt):
    response = openai.chat.completions.create(  # ✅ Updated API call
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Function to send reminders
def send_reminder():
    for drug, time in drug_schedule.items():
        st.warning(f"Reminder: It's time to take your {drug}!")

# Background scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds

# UI with Streamlit
st.set_page_config(page_title="Virtual Health Assistant", layout="wide")

# Sidebar for the menu image
st.sidebar.image("pngwing.com (27).png", use_container_width=True)

# Title
st.title("💊 Virtual Health Assistant")
st.write("Chat with an AI and set medication reminders.")

# Chatbot interface
user_input = st.text_input("Ask me anything about your medication:")
if user_input:
    response = chatbot_response(user_input)
    st.text_area("AI Response:", response, height=150)

# Medication reminder setup
st.subheader("Set Medication Reminders")
drug_name = st.text_input("Medication Name:")
drug_time = st.time_input("Reminder Time:")

if st.button("Set Reminder"):
    drug_schedule[drug_name] = drug_time.strftime("%H:%M")
    schedule.every().day.at(drug_schedule[drug_name]).do(send_reminder)
    st.success(f"Reminder set for {drug_name} at {drug_time}.")

# Run scheduler in the background
thread = threading.Thread(target=run_scheduler, daemon=True)
thread.start()