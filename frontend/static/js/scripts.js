// Get the input box element
const inputbox = document.getElementById('inputbox');

// Automatically adjust the height of the input box based on content
inputbox.addEventListener('input', adjustInputBoxHeight);

// Listen for Shift+Enter to adjust height immediately
inputbox.addEventListener('keypress', function(event) {
    if (event.key === "Enter" && event.shiftKey) {
        adjustInputBoxHeight();
    }
});

function adjustInputBoxHeight() {
    // Reset to allow shrinking if needed
    inputbox.style.height = 'auto';

    // Set height only if the scrollHeight exceeds the clientHeight
    if (inputbox.scrollHeight > inputbox.clientHeight) {
        inputbox.style.height = Math.min(inputbox.scrollHeight, 160) + 'px';
    }
}

// Function to parse markdown with optional image exclusion
function parseMarkdown(text, excludeImages = false) {
    if (excludeImages) {
        const renderer = new marked.Renderer();

        // Override image rendering to exclude images
        renderer.image = function(href, title, text) {
            return `<em>[Image: ${text}]</em>`;
        };

        return marked.parse(text, { renderer: renderer });
    } else {
        // Default parsing including images
        return marked.parse(text);
    }
}

// Autoscroll control
let isAutoScrollEnabled = true;
const chatbox = document.getElementById('chatbox');

// Event listener to detect user scrolling
chatbox.addEventListener('scroll', () => {
    const threshold = 50; // Adjust this value as needed
    const atBottom = chatbox.scrollHeight - chatbox.scrollTop - chatbox.clientHeight <= threshold;
    isAutoScrollEnabled = atBottom;
});

function sendMessage() {
    const message = inputbox.value.trim();

    if (message === '') return;

    // Parse and append user message with markdown formatting
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.innerHTML = parseMarkdown(message);
    chatbox.appendChild(userMessageDiv);

    // Clear input box and reset height
    inputbox.value = '';
    inputbox.style.height = 'auto';

    // Append bot message div for the streaming response
    const botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('message', 'bot-message');
    chatbox.appendChild(botMessageDiv);

    // Scroll to the bottom of the chat area
    if (isAutoScrollEnabled) {
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    // Send the message to the backend and handle streaming response
    fetch('http://localhost:5000/get-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedResponse = '';

        function read() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    // Final update with the parsed markdown of the full response including images
                    botMessageDiv.innerHTML = parseMarkdown(accumulatedResponse);
                    if (isAutoScrollEnabled) {
                        chatbox.scrollTop = chatbox.scrollHeight;
                    }
                    return;
                }

                // Decode and accumulate the chunk
                const chunk = decoder.decode(value, { stream: true });
                accumulatedResponse += chunk;

                // Parse markdown excluding images during streaming
                botMessageDiv.innerHTML = parseMarkdown(accumulatedResponse, true);

                // Scroll if the user is at the bottom
                if (isAutoScrollEnabled) {
                    chatbox.scrollTop = chatbox.scrollHeight;
                }

                // Continue reading
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

// Event listener for Enter key
inputbox.addEventListener('keydown', function(event) {
    // Check if Enter is pressed without Shift
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // Prevent default Enter behavior
        sendMessage();          // Send the message
    }
    // For Shift+Enter, do nothing and allow the default behavior (newline insertion)
});

// Theme toggle functions
function toggleTheme() {
    const checkbox = document.getElementById('theme-checkbox');
    document.body.classList.toggle('light-theme');
    
    // Save theme preference
    if (checkbox.checked) {
        localStorage.setItem('theme', 'light');
    } else {
        localStorage.setItem('theme', 'dark');
    }
}

window.onload = function() {
    const checkbox = document.getElementById('theme-checkbox');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        checkbox.checked = true;
    }
}

document.getElementById('theme-checkbox').addEventListener('change', toggleTheme);
