const chatContainer = document.querySelector('.chat-container');
const toggleChatBtn = document.getElementById('toggleChat');

// Ensure the elements exist before adding event listener
if (toggleChatBtn && chatContainer) {
    // Toggle chat box visibility
    toggleChatBtn.addEventListener('click', (event) => {
        event.preventDefault();
        chatContainer.classList.toggle('closed');
    });
}
