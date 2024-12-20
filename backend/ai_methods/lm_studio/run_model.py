import os
import requests
import json
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Detect if running in WSL and get base URL
def get_base_url():
    ip_address = os.getenv("LM_STUDIO_IP", "localhost")
    return f"http://{ip_address}:8080/v1/chat/completions"

API_URL = get_base_url()

def check():
    """Check if the LM Studio server is connected and running."""
    try:
        response = requests.get(API_URL, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        print("Error: Could not connect to LM Studio server.")
        return False

MAX_HISTORY_LENGTH = 5
conversation_history = []

def build_prompt(messages):
    prompt = ""
    for idx, message in enumerate(messages[-MAX_HISTORY_LENGTH:]):
        role = message['role']
        content = message['content'].strip()
        message_str = f"<|start_header_id|>{role}<|end_header_id|> {content}<|eot_id|>"
        prompt += message_str
    prompt += "<|start_header_id|>assistant<|end_header_id|> "
    return prompt

def process_input(user_message):
    conversation_history.append({'role': 'user', 'content': user_message})

    # Build the prompt (if needed)
    prompt = build_prompt(conversation_history)

    # API request payload
    payload = {
        "model": "bartowski/Llama-3.2-3B-Instruct-GGUF",
        "messages": conversation_history[-MAX_HISTORY_LENGTH:],  # Send conversation history
        "temperature": 0.8,
        "max_tokens": 512,
        "top_p": 0.95,
        "stream": True  # Enable streaming
    }

    try:
        response = requests.post(API_URL, json=payload, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors

        assistant_response = ''

        for line in response.iter_lines():
            if line:
                line_content = line.decode('utf-8').lstrip("data: ").strip()
                if line_content == "[DONE]":
                    break
                try:
                    chunk = json.loads(line_content)
                    word = chunk['choices'][0]['delta'].get('content', '')
                    assistant_response += word
                    yield word
                except json.JSONDecodeError:
                    continue

        # After generating the response, append it to the conversation history
        conversation_history.append({'role': 'assistant', 'content': assistant_response})

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # This will print the full traceback
        yield "Error in processing your request."
