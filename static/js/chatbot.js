document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const quickReplies = document.getElementById('quick-replies');
    
    // Generate a random user ID for the session
    let userId = 'user_' + Math.random().toString(36).substr(2, 9);
    
    // Add a message to the chat
    function addMessage(sender, text, options = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;
    
    // Allow HTML in responses
    msgDiv.innerHTML = `<div class="message-text">${text}</div>`;
    
    if (options) {
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'message-options';
        
        options.forEach(option => {
            const btn = document.createElement('button');
            btn.textContent = option.text;
            btn.onclick = () => {
                // Remove all option buttons
                document.querySelectorAll('.message-options').forEach(el => el.remove());
                // Add user's selection as a message
                addMessage('user', option.text);
                // Send the value to backend
                sendMessage(option.value, true);
            };
            optionsDiv.appendChild(btn);
        });
        
        msgDiv.appendChild(optionsDiv);
    }
    
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
    // Modify your sendMessage function to use the new addMessage:
    async function sendMessage(message, isOptionSelection = false) {
        if (!message.trim()) return;
        
        if (!isOptionSelection) {
            addMessage('user', message);
        }
        chatInput.value = '';
        
        // Show typing indicator
        const typingMsg = document.createElement('div');
        typingMsg.className = 'message bot-message typing-indicator';
        typingMsg.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingMsg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message: message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            chatMessages.removeChild(typingMsg);
            
            // Add response with options if available
            addMessage('bot', data.response, data.options);
            
            if (data.redirect) {
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1500);
            }
        } catch (error) {
            chatMessages.removeChild(typingMsg);
            addMessage('bot', "⚠️ Sorry, I'm having trouble responding.");
        }
    }
    
    // Event listeners
    sendBtn.addEventListener('click', () => {
        if (chatInput.value.trim()) {
            sendMessage(chatInput.value);
        }
    });
    
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && chatInput.value.trim()) {
            sendMessage(chatInput.value);
        }
    });
    
    // Initial greeting
    setTimeout(() => {
        addMessage('bot', "Hello! I'm your PCOS assistant. Ask me about nutrition, fitness, or general PCOS tips.");
    }, 500);
});