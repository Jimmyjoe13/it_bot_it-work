document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const clearButton = document.getElementById('clear-button');

    // Fonction pour convertir les URLs en liens cliquables
    function convertUrlsToLinks(text) {
        // Expression régulière améliorée pour détecter les URLs
        const urlRegex = /(https?:\/\/[^\s<>"']+|www\.[^\s<>"']+)/g;
        
        return text.replace(urlRegex, function(url) {
            // Ajouter http:// aux URLs commençant par www.
            const fullUrl = url.startsWith('www.') ? 'http://' + url : url;
            return `<a href="${fullUrl}" target="_blank" rel="noopener noreferrer" class="chat-link">${url}</a>`;
        });
    }

    // Fonction pour créer un message de l'utilisateur
    function createUserMessage(content) {
        // Convertir les URLs en liens cliquables
        const contentWithLinks = convertUrlsToLinks(content);
        
        return `
            <div class="message-group right">
                <div class="message-content">
                    <div class="message user">
                        <div class="message-bubble user-bubble">
                            ${contentWithLinks}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Fonction pour créer un message du chatbot
    function createBotMessage(content) {
        // Convertir les URLs en liens cliquables
        const contentWithLinks = convertUrlsToLinks(content);
        
        return `
            <div class="message-group left">
                <div class="avatar assistant-avatar">
                    <svg viewBox="0 0 24 24" class="bot-icon">
                        <path fill="currentColor" d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
                    </svg>
                </div>
                <div class="message-content">
                    <div class="message assistant">
                        <div class="message-bubble bot-bubble">
                            ${contentWithLinks}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Fonction pour créer l'animation de chargement
    function createLoadingMessage() {
        return `
            <div class="message-group left loading-message">
                <div class="avatar assistant-avatar">
                    <svg viewBox="0 0 24 24" class="bot-icon">
                        <path fill="currentColor" d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
                    </svg>
                </div>
                <div class="message-content">
                    <div class="message assistant">
                        <div class="message-bubble bot-bubble">
                            <div class="loading-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Fonction pour faire défiler vers le bas
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Gestionnaire de soumission du formulaire
    messageForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        // Afficher le message de l'utilisateur immédiatement
        chatMessages.insertAdjacentHTML('beforeend', createUserMessage(message));
        scrollToBottom();
        messageInput.value = '';

        // Afficher l'animation de chargement
        chatMessages.insertAdjacentHTML('beforeend', createLoadingMessage());
        scrollToBottom();

        try {
            // Attendre 1.5 secondes avant d'envoyer la requête
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Envoyer la requête au serveur
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `message=${encodeURIComponent(message)}`
            });

            if (!response.ok) throw new Error('Erreur réseau');
            
            const data = await response.json();

            // Supprimer l'animation de chargement
            const loadingMessage = document.querySelector('.loading-message');
            if (loadingMessage) loadingMessage.remove();

            // Afficher la réponse du chatbot
            chatMessages.insertAdjacentHTML('beforeend', createBotMessage(data.botResponse.content));
            scrollToBottom();
        } catch (error) {
            console.error('Erreur:', error);
            const loadingMessage = document.querySelector('.loading-message');
            if (loadingMessage) loadingMessage.remove();
            
            chatMessages.insertAdjacentHTML('beforeend', createBotMessage(
                "Désolé, j'ai rencontré une erreur. Pourriez-vous reformuler votre question ?"
            ));
            scrollToBottom();
        }
    });

    // Gestionnaire pour le bouton d'effacement
    clearButton.addEventListener('click', async function() {
        try {
            const response = await fetch('/clear', {
                method: 'POST'
            });
            if (!response.ok) throw new Error('Erreur réseau');
            location.reload();
        } catch (error) {
            console.error('Erreur:', error);
        }
    });
});
