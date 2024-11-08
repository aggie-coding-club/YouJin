// frontend/static/js/scripts.js

// TODO: Implement form validation for message input
function sendMessage() {
    const chatbox = document.getElementById('chatbox');
    const inputbox = document.getElementById('inputbox');
    const message = inputbox.value.trim();

    if (message === '') return;

    // Append user message to chat area
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.textContent = message;
    chatbox.appendChild(userMessageDiv);

    // Clear input box
    inputbox.value = '';

    // Scroll to the bottom of the chat area
    chatbox.scrollTop = chatbox.scrollHeight;

    // Send the message to the backend
    fetch('http://localhost:5000/get-response', {  // Updated URL with full backend address
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Append bot response to chat area
        const botMessageDiv = document.createElement('div');
        botMessageDiv.classList.add('message', 'bot-message');
        botMessageDiv.textContent = data.response;
        chatbox.appendChild(botMessageDiv);

        // Scroll to the bottom
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally, display an error message to the user
    });
}

document.getElementById('inputbox').addEventListener('keypress', function(event) {
    // Check if Enter is pressed
    if (event.key === "Enter") {
        if(event.shiftKey){
            event.preventDefault()
            const inputbox = document.getElementById('inputbox')
            inputbox.value += "\n"

        }else{
            event.preventDefault(); // Prevent default action
            sendMessage();

        }
        
    }
});

function toggleTheme() {
    const checkbox = document.getElementById('theme-checkbox');
    document.body.classList.toggle('light-theme');
    
    //save theme preference
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