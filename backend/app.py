import os
import sys

# Get the current directory of app.py (i.e., backend directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to sys.path to access terminal_class
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from ai_type import AI_Type  # Import the AI_Type class
from terminal.terminal_class import Terminal

app = Flask(__name__)
CORS(app)

# Initialize the Terminal object for storing conversation blocks
terminal = Terminal()

# Initialize the AI system
ai_system = AI_Type()

# Route to provide available AI methods
@app.route('/get-ai-methods', methods=['GET'])
def get_ai_methods():
    """Return the list of available AI methods."""
    available_methods = ai_system.get_available_ais()
    return jsonify({'methods': available_methods})

# Route to set the AI method
@app.route('/set-ai-method', methods=['POST'])
def set_ai_method():
    data = request.get_json()
    selected_ai_method = data.get('ai_method')

    # Validate the selected AI method
    if not selected_ai_method:
        return jsonify({'error': 'No AI method selected.'}), 400
    if selected_ai_method not in ai_system.get_available_ais():
        return jsonify({'error': 'Selected AI method is not available.'}), 400

    # Initialize the selected AI method
    ai_system.set_selected_ai(selected_ai_method)

    return jsonify({'status': 'AI method set successfully.'})

# Route to process user input
@app.route('/get-response', methods=['POST'])
def get_response():
    """Process user input using the currently selected AI method."""
    data = request.get_json()
    user_message = data.get('message')

    # Check if an AI method is selected
    if not ai_system.current_ai:
        return jsonify({'error': 'No AI method selected. Please select an AI method to proceed.'}), 400

    # Run the selected AI and get the response or response generator
    response = ai_system.run_selected_ai(user_message)

    if isinstance(response, str):
        # Check if the selected method is "user_input" and return plain text
        if ai_system.current_ai == "user_input":
            conversation_block = {"user": user_message, "bot": response}
            terminal.store_conversation_block(conversation_block)
            return response  # Return as plain text for user input

        # Non-streaming response for other methods: Return as JSON
        conversation_block = {"user": user_message, "bot": response}
        terminal.store_conversation_block(conversation_block)
        return jsonify({'response': response})

    elif hasattr(response, '__iter__') and not isinstance(response, str):
        # Handle streaming response
        def generate():
            bot_response = ''
            for token in response:
                bot_response += token
                yield token
            # Store the entire response after streaming
            conversation_block = {"user": user_message, "bot": bot_response}
            terminal.store_conversation_block(conversation_block)

        return Response(stream_with_context(generate()), mimetype='text/plain')
    
    else:
        # Unexpected response format from AI
        return jsonify({'error': 'Unexpected response format from AI method.'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
