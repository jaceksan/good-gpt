import requests
import json
import streamlit as st
import os

# Slack API URL for posting messages
SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"

# Slack API token
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

# Slack channel to post messages to
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

# Function to send message to Slack channel
def send_slack_message(message):
    """
    Send a message to a Slack channel
    """
    payload = {
        "channel": SLACK_CHANNEL,
        "text": message
    }
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + SLACK_TOKEN
    }
    response = requests.post(SLACK_POST_MESSAGE_URL, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

# Function to receive messages from Slack channel
def receive_slack_message():
    """
    Receive messages from a Slack channel
    """
    messages_url = f"https://slack.com/api/conversations.history?channel={SLACK_CHANNEL}"
    headers = {"Authorization": "Bearer " + SLACK_TOKEN}
    response = requests.get(messages_url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
    messages = response.json()["messages"]
    for message in messages:
        username = message["user"]
        text = message["text"]
        st.write(f"{username}: {text}")

# Streamlit UI for sending and receiving messages
st.title("Slack Integration")
with st.form(key="send_message"):
    message = st.text_input("Type your message")
    submitted = st.form_submit_button("Send")
if submitted:
    send_slack_message(message)
    st.success("Message sent")
    st.experimental_rerun()

receive_slack_message()