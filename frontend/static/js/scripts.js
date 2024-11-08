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

// Modify sendMessage to handle streaming response
function sendMessage() {
    const chatbox = document.getElementById('chatbox');
    const message = inputbox.value.trim();

    if (message === '') return;

    // Append user message to chat area
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.textContent = message;
    chatbox.appendChild(userMessageDiv);

    // Clear input box and reset height
    inputbox.value = '';
    inputbox.style.height = 'auto';  // Reset to default height

    // Append bot message div to chat area
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
        function read() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    return;
                }
                const chunk = decoder.decode(value, { stream: true });
                botMessageDiv.textContent += chunk;
                chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the bottom
                read(); // Continue reading
            }).catch(error => {
                console.error('Error reading stream:', error);
            });
        }
        read();
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally, display an error message to the user
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
