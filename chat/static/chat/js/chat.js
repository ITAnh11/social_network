// Sample conversation data
var conversations = [
];

const url_conversation = '/chat/get_conversations'

function get_conversations(){
    fetch(url_conversation)
    .then(response => response.json())
    .then(data => {
      add_conversation(data);
      showConversationList();
      // console.log(conversations);
    })
}

function add_conversation(data){
    data.conversations.forEach(function(conversation){
        var newconv = {name: conversation.title, messages: []}
        conversations.push(newconv)
    })
}

get_conversations();

const conversationList = document.getElementById('conversationList');
const chatHeader = document.getElementById('chatHeader');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const searchInput = document.getElementById('search');

console.log("im out loop");
// Populate conversation list
function showConversationList(){
  console.log(conversations);
  conversations.forEach(function(conversation, index){
    console.log("im in loop");
    const li = document.createElement('li');
    li.textContent = conversation.name;
    li.addEventListener('click', () => {
      showConversation(index);
    });

    conversationList.appendChild(li);
    
    // console.log(conversationList);
  });
}

// Show conversation
function showConversation(index) {
  const conversation = conversations[index];
  chatHeader.textContent = conversation.name;
  chatMessages.innerHTML = '';
  conversation.messages.forEach(function(message){
    const div = document.createElement('div');
    div.classList.add('message');
    div.textContent = message;
    chatMessages.appendChild(div);
  });
}

// Send message
sendMessageBtn.addEventListener('click', () => {
  const message = messageInput.value;
  if (message.trim() !== '') {
    const activeConversationIndex = findActiveConversationIndex();
    conversations[activeConversationIndex].messages.push(message);
    showConversation(activeConversationIndex);
    messageInput.value = '';
  }
});

// Search functionality
searchInput.addEventListener('input', () => {
  const searchTerm = searchInput.value.toLowerCase();
  conversationList.innerHTML = '';
  conversations.forEach((conversation, index) => {
    if (conversation.name.toLowerCase().includes(searchTerm)) {
      const li = document.createElement('li');
      li.textContent = conversation.name;
      li.addEventListener('click', () => {
        showConversation(index);
      });
      conversationList.appendChild(li);
    }
  });
});

// Helper function to find active conversation index
function findActiveConversationIndex() {
  const activeConversationName = chatHeader.textContent;
  return conversations.findIndex(conversation => conversation.name === activeConversationName);
}
