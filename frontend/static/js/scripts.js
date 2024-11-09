// Get the input box and chatbox elements
const inputbox = document.getElementById('inputbox');
const chatbox = document.getElementById('chatbox');
let isAutoScrollEnabled = true;

// Automatically adjust the height of the input box based on content
inputbox.addEventListener('input', adjustInputBoxHeight);
inputbox.addEventListener('keypress', function(event) {
    if (event.key === "Enter" && event.shiftKey) {
        adjustInputBoxHeight();
    }
});

function adjustInputBoxHeight() {
    inputbox.style.height = 'auto';
    if (inputbox.scrollHeight > inputbox.clientHeight) {
        inputbox.style.height = Math.min(inputbox.scrollHeight, 160) + 'px';
    }
}

// Function to parse markdown with optional image exclusion
function parseMarkdown(text, excludeImages = false) {
    const renderer = excludeImages ? new marked.Renderer() : null;
    if (excludeImages && renderer) {
        renderer.image = (href, title, text) => `<em>[Image: ${text}]</em>`;
    }
    return marked.parse(text, { renderer });
}

// Autoscroll control
chatbox.addEventListener('scroll', () => {
    const threshold = 50;
    const atBottom = chatbox.scrollHeight - chatbox.scrollTop - chatbox.clientHeight <= threshold;
    isAutoScrollEnabled = atBottom;
});

// Get references to elements
const aiMethodSelect = document.getElementById('ai-method-select');
const sendButton = document.getElementById('send-button');

// Event listener for AI method selection
aiMethodSelect.addEventListener('change', function() {
    const selectedAiMethod = aiMethodSelect.value;
    if (selectedAiMethod) {
        // Enable the send button
        sendButton.disabled = false;

        // // Save the selected AI method in localStorage
        // localStorage.setItem('ai_method', selectedAiMethod);

        // Send request to backend to set AI method
        fetch('http://localhost:5000/set-ai-method', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ai_method: selectedAiMethod })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'AI method set successfully.') {
                console.log('AI method set on backend.');
            } else {
                console.error('Error setting AI method on backend:', data.error);
            }
        })
        .catch(error => {
            console.error('Error setting AI method on backend:', error);
        });
    }
});

// Send Message with Selected AI Method
function sendMessage() {
    const message = inputbox.value.trim();
    if (message === '') return;

    // Append user message
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.innerHTML = parseMarkdown(message);
    chatbox.appendChild(userMessageDiv);

    // Clear input box and reset height
    inputbox.value = '';
    inputbox.style.height = 'auto';

    // Append bot message placeholder
    const botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('message', 'bot-message');
    chatbox.appendChild(botMessageDiv);

    // Autoscroll to the bottom if enabled
    if (isAutoScrollEnabled) chatbox.scrollTop = chatbox.scrollHeight;

    // Send message to backend
    fetch('http://localhost:5000/get-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            message: message
            // No need to send ai_method
        })
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedResponse = '';

        function read() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    botMessageDiv.innerHTML = parseMarkdown(accumulatedResponse);
                    if (isAutoScrollEnabled) chatbox.scrollTop = chatbox.scrollHeight;
                    return;
                }

                const chunk = decoder.decode(value, { stream: true });
                accumulatedResponse += chunk;
                botMessageDiv.innerHTML = parseMarkdown(accumulatedResponse, true);

                if (isAutoScrollEnabled) chatbox.scrollTop = chatbox.scrollHeight;
                read();
            }).catch(error => {
                console.error('Error reading stream:', error);
            });
        }
        read();
    })
    .catch(error => {
        console.error('Error:', error);
        botMessageDiv.textContent = 'Error: Unable to receive response.';
    });
}

// Load available AI methods on page load and set theme
window.onload = function() {
    const checkbox = document.getElementById('theme-checkbox');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        checkbox.checked = true;
    }

    // Initially disable the send button
    sendButton.disabled = true;

    // Fetch AI methods and populate dropdown
    fetch('http://localhost:5000/get-ai-methods')
        .then(response => response.json())
        .then(data => {
            const methods = data.methods;
            const aiMethodSelect = document.getElementById('ai-method-select');

            // Always start with the default option
            aiMethodSelect.innerHTML = '<option value="" disabled selected>Select a method</option>';

            // Populate dropdown with available methods
            methods.forEach(method => {
                const option = document.createElement('option');
                option.value = method;
                option.textContent = method;
                aiMethodSelect.appendChild(option);
            });

            // const savedMethod = localStorage.getItem('ai_method');
            // if (savedMethod && methods.includes(savedMethod)) {
            //     aiMethodSelect.value = savedMethod;
            //     sendButton.disabled = false;
            //     aiMethodSelect.dispatchEvent(new Event('change'));
            // }
        })
        .catch(error => {
            console.error('Error fetching AI methods:', error);
        });
};

// Update the AI method change event listener to disable the send button when the default is selected
aiMethodSelect.addEventListener('change', function() {
    const selectedAiMethod = aiMethodSelect.value;
    if (selectedAiMethod) {
        sendButton.disabled = false;

        // Save the selected AI method in localStorage
        localStorage.setItem('ai_method', selectedAiMethod);

        // Send request to backend to set AI method
        fetch('http://localhost:5000/set-ai-method', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ai_method: selectedAiMethod })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'AI method set successfully.') {
                console.log('AI method set on backend.');
            } else {
                console.error('Error setting AI method on backend:', data.error);
            }
        })
        .catch(error => {
            console.error('Error setting AI method on backend:', error);
        });
    } else {
        sendButton.disabled = true; // Disable send button if no valid method is selected
    }
});

// Event listener for Enter key
inputbox.addEventListener('keydown', function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

// Theme toggle functions
function toggleTheme() {
    const checkbox = document.getElementById('theme-checkbox');
    document.body.classList.toggle('light-theme');
    localStorage.setItem('theme', checkbox.checked ? 'light' : 'dark');
}

document.getElementById('theme-checkbox').addEventListener('change', toggleTheme);
