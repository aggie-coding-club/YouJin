import os
import sys
from llama_cpp import Llama
import time

# Get the directory of the current file (backend/ai/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the model file inside ai/models/
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'Llama-3.2-3B-Instruct-Q8_0.gguf')

# Variable to hold the model instance
llm = None

def check():
    """
    Check if everything is valid before running the model.
    - Ensure the model file exists.
    - Add additional checks as needed.
    """
    # Check if the model file exists
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        return False

    print("All checks passed.")
    return True

def load_model():
    """Load the model into the global llm variable."""
    global llm
    if llm is None:
        print(f"Loading model from: {MODEL_PATH}")
        llm = Llama(
            model_path=MODEL_PATH,
            n_threads=4,
            n_ctx=2048,
            n_batch=512,
            use_mlock=True,
            n_gpu_layers=0,  # Adjust based on your GPU's VRAM
            verbose=False    # Suppresses informational logs
        )
    else:
        print("Model is already loaded.")

MAX_HISTORY_LENGTH = 5
conversation_history = []

def build_prompt(messages):
    prompt = ""
    for idx, message in enumerate(messages[-MAX_HISTORY_LENGTH:]):
        role = message['role']
        content = message['content'].strip()
        message_str = f"<|start_header_id|>{role}<|end_header_id|> {content}<|eot_id|>"
        prompt += message_str

    # Add the assistant role at the end of the prompt
    prompt += "<|start_header_id|>assistant<|end_header_id|> "
    
    return prompt

def process_input(user_message):
    # Load the model if not already loaded
    load_model()

    # Add the user message to conversation history
    conversation_history.append({'role': 'user', 'content': user_message})

    # Build the prompt for the AI model
    prompt = build_prompt(conversation_history)

    try:
        # Generate the response using the AI model with streaming enabled
        output = llm(
            prompt,
            max_tokens=512,
            stop=["<|eot_id|>", "<|start_header_id|>user<|end_header_id|>"],
            temperature=0.8,
            top_k=40,
            top_p=0.95,
            repeat_penalty=1.1,
            stream=True  # Enable streaming mode
        )

        # Initialize an empty response
        assistant_response = ""

        # Stream the response word by word
        for token in output:
            # Access the text from the streamed token
            word = token['choices'][0]['text']
            assistant_response += word
            # Yield the word to the caller
            yield word

        # Add the assistant's response to the conversation history
        conversation_history.append({'role': 'assistant', 'content': assistant_response})

    except Exception as e:
        print(f"\nError: {e}")
        error_message = "I'm sorry, something went wrong."
        yield error_message
        conversation_history.append({'role': 'assistant', 'content': error_message})
