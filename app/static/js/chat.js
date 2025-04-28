// Chat functionality
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');
const sendButton = document.getElementById('sendButton');
const currentYearSpan = document.getElementById('currentYear');

// Update current year in footer
if (currentYearSpan) {
    currentYearSpan.textContent = new Date().getFullYear();
}

// Function to create a new message element
function createMessageElement(message, messageType) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${messageType}-message`);
    messageElement.innerHTML = `<div class="message-content"><p>${message}</p></div>`;
    return messageElement;
}

// Function to display loading dots
function showLoadingDots() {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'bot-message');
    messageElement.innerHTML = `<div class="message-content loading-dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageElement;
}

// Function to display a new message
function displayMessage(message, messageType) {
    const messageElement = createMessageElement(message, messageType);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to display a conversion result
function displayConversionResult(data) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'bot-message');
    messageElement.innerHTML = `<div class="message-content conversion-result"><p>نتيجة التحويل: <span class="amount">${formatCurrency(data.amount, data.base_currency)}</span> = <span class="amount">${formatCurrency(data.result, data.target_currency)}</span></p></div>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to handle the chat response
async function handleChatResponse(response) {
    const responseData = await response.json();
    
    // Check for errors
    if (response.status !== 200 || responseData.error) {
        displayMessage(responseData.error || 'حدث خطأ أثناء معالجة رسالتك.', 'bot');
        return;
    }
    
    // Check the type of the response
    if (responseData.response.type === 'conversion') {
        displayConversionResult(responseData.response.data);
    } else {
        displayMessage(responseData.response.text, 'bot');
    }
}

// Event listener for the chat form
chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = userInput.value;
    userInput.value = '';

    // Display the user's message
    displayMessage(message, 'user');
    
    // Show loading animation
    const loadingDots = showLoadingDots();

    // Send the message to the server
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });
        
        // Handle the response
        await handleChatResponse(response);

    } catch (error) {
        console.error('Error:', error);
        displayMessage('حدث خطأ أثناء معالجة رسالتك.', 'bot');
    } finally {
        // Remove loading animation
        chatMessages.removeChild(loadingDots);
    }
});

// Handle shortcut button clicks
const shortcutButtons = document.querySelectorAll('.shortcut-btn');
shortcutButtons.forEach(button => {
    button.addEventListener('click', () => {
        const query = button.getAttribute('data-query');
        userInput.value = query;
        sendButton.click(); // Simulate click on send button
    });
});