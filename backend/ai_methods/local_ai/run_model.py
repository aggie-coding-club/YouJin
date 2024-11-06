import os
import sys
from llama_cpp import Llama
import time

# Get the directory of the current file (backend/ai/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the model file inside ai/models/
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'Llama-3.2-3B-Instruct-Q8_0.gguf')

# Print the model path to verify
print(f"Loading model from: {MODEL_PATH}")

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

    # Check for any additional conditions (e.g., system resources, environment variables)
    # Additional checks can be added here

    print("All checks passed.")
    return True


# Initialize the model with GPU acceleration
llm = Llama(
    model_path=MODEL_PATH,
    n_threads=4,
    n_ctx=2048,
    n_batch=512,
    use_mlock=True,
    n_gpu_layers=0,  # Adjust based on your GPU's VRAM
    verbose=False    # Suppresses informational logs
)

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
        print("AI: ", end="", flush=True)

        # Stream the response word by word
        for token in output:
            # Correctly access the text from the streamed token
            word = token['choices'][0]['text']
            print(word, end="", flush=True)
            assistant_response += word
            time.sleep(0.05)  # Delay for a more natural typing effect

        # Add the assistant's response to the conversation history
        conversation_history.append({'role': 'assistant', 'content': assistant_response})

    except Exception as e:
        print(f"\nError: {e}")
        assistant_response = "I'm sorry, something went wrong."

    # Return the assistant's full response
    return assistant_response

# Main chat loop for testing
if __name__ == "__main__":
    while True:
        # Get user input
        user_input = input("\nUser: ")

        # Exit condition
        if user_input.lower() == "exit":
            print("Ending chat.")
            break

        # Process the input and print the assistant's response
        process_input(user_input)
