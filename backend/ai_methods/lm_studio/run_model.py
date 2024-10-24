import os
import requests
import platform
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Detect if running in WSL and get base URL
def get_base_url():
    ip_address = os.getenv("LM_STUDIO_IP", "localhost")  # Default to localhost if env variable is not set
    return f"http://{ip_address}:8080/v1/chat/completions"

API_URL = get_base_url()

def is_server_running():
    """Check if the LM Studio server is running on port 8080."""
    url = API_URL
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
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

    # Add assistant role at the end
    prompt += "<|start_header_id|>assistant<|end_header_id|> "
    return prompt

def process_input(user_message):
    conversation_history.append({'role': 'user', 'content': user_message})
    prompt = build_prompt(conversation_history)

    # API request payload
    payload = {
        "model": "bartowski/Llama-3.2-3B-Instruct-GGUF",  # Use your model's correct identifier
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.8,
        "max_tokens": 512,
        "top_p": 0.95,
        "stream": True  # Enable streaming
    }

    try:
        # Send request to LM Studio
        response = requests.post(API_URL, json=payload, stream=True)
        
        assistant_response = ""
        for line in response.iter_lines():
            if line:
                # Remove 'data: ' prefix before decoding
                line_content = line.decode('utf-8').lstrip("data: ").strip()

                # Skip the '[DONE]' signal
                if line_content == "[DONE]":
                    break

                if line_content:
                    try:
                        # Parse JSON from the line
                        chunk = json.loads(line_content)
                        
                        # Access content safely
                        word = chunk['choices'][0]['delta'].get('content', '')
                        assistant_response += word
                        print(word, end="", flush=True)
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError: {e} - Line content: {line_content}")
                        continue  # Skip this line if it's not valid JSON

        conversation_history.append({'role': 'assistant', 'content': assistant_response})

    except Exception as e:
        print(f"Error: {e}")
        assistant_response = "Error in processing your request."

    return assistant_response

# Main loop for testing
if __name__ == "__main__":
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == "exit":
            print("Ending chat.")
            break
        process_input(user_input)
