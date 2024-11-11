import os
import importlib.util

class AI_Type:
    def __init__(self):
        """Initialize paths and available AI methods."""
        # Paths to run_model.py in various directories
        self.lm_studio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_methods', 'lm_studio', 'run_model.py')
        self.local_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_methods', 'local_ai', 'run_model.py')
        
        # Dictionary to store available AI methods
        self.ai_methods = {}
        # Variable to store the currently selected AI method
        self.current_ai = None
        # Variables to store loaded modules and functions
        self.lm_studio_module = None
        self.lm_studio_process_input = None
        self.local_model_module = None
        self.local_model_process_input = None
        # Check which AI methods are available on initialization
        self.check_available_ais()

    def check_available_ais(self):
        """Check which AI methods are available by calling each check function."""
        if self.check_lm_studio():
            self.ai_methods['lm_studio'] = self.run_lm_studio
            print("LM Studio is available and added to ai_methods.")
        else:
            print("LM Studio is not available.")
        
        if self.check_local_model():
            self.ai_methods['local_model'] = self.run_local_model
            print("Local AI model is available and added to ai_methods.")
        else:
            print("Local AI model is not available.")

        # Fallback is always available
        self.ai_methods['user_input'] = self.run_user_input
        print("Fallback user input method added to ai_methods.")

    def get_available_ais(self):
        """Return a list of available AI methods."""
        return list(self.ai_methods.keys())

    def set_selected_ai(self, ai_method):
        """Set the currently selected AI method."""
        print(f"Setting selected AI method to: {ai_method}")
        if ai_method in self.ai_methods:
            self.current_ai = ai_method
        else:
            print(f"AI method '{ai_method}' is not available. Defaulting to 'user_input'.")
            self.current_ai = 'user_input'  # Default to fallback

    def run_selected_ai(self, user_message):
        """Run the selected AI method based on current selection."""
        if not self.current_ai:
            print("No AI method has been selected. Defaulting to 'user_input'.")
            self.current_ai = 'user_input'

        print(f"Executing AI method: {self.current_ai}")
        return self.ai_methods[self.current_ai](user_message)

    ####### LM STUDIO #######

    def check_lm_studio(self):
        """Check if LM Studio AI model is available and the server is running."""
        if os.path.exists(self.lm_studio_path):
            try:
                # Load the run_model.py module dynamically
                if self.lm_studio_module is None:
                    spec = importlib.util.spec_from_file_location("lm_studio_run_model", self.lm_studio_path)
                    lm_studio_run_model = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(lm_studio_run_model)
                    if hasattr(lm_studio_run_model, 'check'):
                        if lm_studio_run_model.check():
                            self.lm_studio_module = lm_studio_run_model
                            self.lm_studio_process_input = lm_studio_run_model.process_input
                            return True
                        else:
                            print("LM Studio check function returned False.")
                            return False
                    else:
                        print("LM Studio check function is not available in run_model.py.")
                        return False
                else:
                    return True  # Module already loaded
            except Exception as e:
                print(f"Error checking LM Studio: {e}")
                return False
        else:
            print("LM Studio directory or run_model.py does not exist.")
            return False

    def run_lm_studio(self, user_message):
        """Run the LM Studio AI model."""
        try:
            if self.lm_studio_process_input is None:
                print("LM Studio process_input is not loaded.")
                return "Error: LM Studio is not properly configured."
            # Call the process_input function with the user_message
            return self.lm_studio_process_input(user_message)
        except Exception as e:
            print(f"Error running LM Studio: {e}")
            return "Error processing your request with LM Studio."

    ####### END LM STUDIO #######

    ####### LOCAL MODELS #######

    def check_local_model(self):
        """Check if the local model is available and everything is valid."""
        if os.path.exists(self.local_model_path):
            try:
                # Load the run_model.py module dynamically
                if self.local_model_module is None:
                    spec = importlib.util.spec_from_file_location("local_model_run_model", self.local_model_path)
                    local_model_run_model = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(local_model_run_model)
                    if hasattr(local_model_run_model, 'check'):
                        if local_model_run_model.check():
                            self.local_model_module = local_model_run_model
                            self.local_model_process_input = local_model_run_model.process_input
                            return True
                        else:
                            print("Local model check function returned False.")
                            return False
                    else:
                        print("Local model check function is not available in run_model.py.")
                        return False
                else:
                    return True  # Module already loaded
            except Exception as e:
                print(f"Error checking local model: {e}")
                return False
        else:
            print("Local model directory or run_model.py does not exist.")
            return False

    def run_local_model(self, user_message):
        """Run the local AI model."""
        try:
            if self.local_model_process_input is None:
                print("Local model process_input is not loaded.")
                return "Error: Local model is not properly configured."
            # Call the process_input function with the user_message
            return self.local_model_process_input(user_message)
        except Exception as e:
            print(f"Error running Local AI model: {e}")
            return "Error processing your request with the local model."

    ####### END LOCAL MODELS #######

    ####### FALLBACK USER INPUT #######

    def run_user_input(self, user_message):
        """Fallback method: Get bot response from user input (manual input as AI)."""
        print(f"User: {user_message}")
        bot_response = input("Your response as AI: ")
        return bot_response

    ####### END FALLBACK USER INPUT #######
