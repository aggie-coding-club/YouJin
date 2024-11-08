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

// Function to parse markdown for bold, italics, and headings
function parseMarkdown(text) {
    return marked.parse(text);
}

function sendMessage() {
    const chatbox = document.getElementById('chatbox');
    const message = inputbox.value.trim();

    if (message === '') return;

    // Parse and append user message with markdown formatting
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.innerHTML = parseMarkdown(message);  // Use innerHTML for parsed markdown content
    chatbox.appendChild(userMessageDiv);

    // Clear input box and reset height
    inputbox.value = '';
    inputbox.style.height = 'auto';

    // Append bot message div for the streaming response
    const botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('message', 'bot-message');
    chatbox.appendChild(botMessageDiv);

    // Scroll to the bottom of the chat area
    chatbox.scrollTop = chatbox.scrollHeight;

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
        let accumulatedResponse = '';  // Accumulate chunks here

        function read() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    // Final update with the parsed markdown of the full response
                    botMessageDiv.innerHTML = parseMarkdown(accumulatedResponse);
                    chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the bottom
                    return;
                }

                // Decode and accumulate the chunk
                const chunk = decoder.decode(value, { stream: true });
                accumulatedResponse += chunk;

                // Parse markdown of the accumulated response and update bot message div
                botMessageDiv.innerHTML = parseMarkdown(accumulatedResponse);
                chatbox.scrollTop = chatbox.scrollHeight;

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

// Theme toggle functions (unchanged)
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
