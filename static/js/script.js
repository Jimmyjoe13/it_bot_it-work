async function sendMessage(event) {
    event.preventDefault();
    
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message) return;

    // Ajouter le message de l'utilisateur
    appendMessage(message, 'user');
    messageInput.value = '';

    try {
        const formData = new FormData();
        formData.append('message', message);

        const response = await fetch('/chat', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        // Ajouter la réponse du bot
        appendMessage(data.response, 'bot');
    } catch (error) {
        console.error('Erreur:', error);
        appendMessage('Désolé, une erreur est survenue.', 'bot');
    }

    scrollToBottom();
}

function appendMessage(content, role) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = content;
    messagesContainer.appendChild(messageDiv);
}

async function clearHistory() {
    try {
        await fetch('/clear', { method: 'POST' });
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = '';
    } catch (error) {
        console.error('Erreur lors de l\'effacement de l\'historique:', error);
    }
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Accessibilité - Support des raccourcis clavier
document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && event.ctrlKey) {
        document.querySelector('#chat-form button').click();
    }
});
