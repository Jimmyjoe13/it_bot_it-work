// Function to scroll to bottom of chat
function scrollToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Function to append a new message to the chat
function appendMessage(messageData) {
    const messagesContainer = document.getElementById('chat-messages');
    const isAssistant = messageData.role === 'assistant';
    
    const messageHTML = `
        <div class="message-group ${isAssistant ? 'left' : 'right'}">
            ${isAssistant ? `
                <div class="avatar assistant-avatar">
                    <svg viewBox="0 0 24 24" class="bot-icon">
                        <path fill="currentColor" d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
                    </svg>
                </div>
            ` : ''}
            <div class="message-content">
                <div class="message ${isAssistant ? 'assistant' : 'user'}">
                    <div class="message-bubble">
                        ${messageData.content}
                    </div>
                    <div class="message-info">
                        <span class="message-time">${isAssistant ? 'Assistant' : 'User'}</span>
                        <div class="message-actions">
                            <button class="action-button" title="Copier" onclick="copyMessage(this)">
                                <svg viewBox="0 0 24 24" width="16" height="16">
                                    <path fill="currentColor" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            ${!isAssistant ? `
                <div class="avatar user-avatar">
                    <svg viewBox="0 0 24 24" class="user-icon">
                        <path fill="currentColor" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
                    </svg>
                </div>
            ` : ''}
        </div>
    `;
    
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = messageHTML;
    const messageElement = tempDiv.firstElementChild;
    messagesContainer.appendChild(messageElement);
    scrollToBottom();
}

// Function to copy message content
function copyMessage(button) {
    const messageContent = button.closest('.message').querySelector('.message-bubble').textContent;
    navigator.clipboard.writeText(messageContent.trim()).then(() => {
        button.classList.add('copied');
        setTimeout(() => button.classList.remove('copied'), 1000);
    });
}

// Function to send a message
async function sendMessage(event) {
    event.preventDefault();
    
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message) return;

    try {
        const formData = new FormData();
        formData.append('message', message);

        const response = await fetch('/chat', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        // Add user message
        appendMessage(data.userMessage);
        
        // Clear input
        messageInput.value = '';
        
        // Add bot response
        appendMessage(data.botResponse);
    } catch (error) {
        console.error('Erreur:', error);
        appendMessage({
            content: 'Désolé, une erreur est survenue.',
            role: 'assistant'
        });
    }
}

// Function to clear chat history
async function clearHistory() {
    try {
        await fetch('/clear', { method: 'POST' });
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = '';
    } catch (error) {
        console.error('Erreur lors de l\'effacement de l\'historique:', error);
    }
}

// Keyboard shortcuts support
document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && event.ctrlKey) {
        document.querySelector('#chat-form button').click();
    }
});
