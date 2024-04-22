// show all users
const chatHeader = document.getElementById('chatHeader');
const all_messeeji = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const searchInput = document.getElementById('search');
const list_all_users = document.getElementById("userList");
var conversations = [
];

var url_all_users = "../search/@"; // Assuming this is the correct endpoint to fetch all users
var url_get_channel = "create_channel/"
function show_all_users() {
  fetch(url_all_users)
  .then(response => response.json())
  .then(data => {
      // console.log("all_users:", data);
      data.list_users.forEach(function(user) {
          console.log(user);
          var url = ""; // You might want to define a URL to link to each user's profile
          var fullName = user.first_name + " " + user.last_name;
          var li = document.createElement('li');
          li.textContent = fullName;

          li.addEventListener('click', () => {
            // Show channel logic here

            // Send POST request
            createChannel(user)
              .then(channel_id => {
                console.log('Channel ID:', channel_id);
                // You can use channel_id here
                console.log("channel id: ", channel_id);
                showChannel(user, channel_id);
              })
              .catch(error => {
                // Handle error
                console.error('Failed to create channel:', error);
              });
            
          });

          list_all_users.appendChild(li);
          // console.log(li)
      });
  })
  .catch(error => {
      console.error('Error fetching users:', error);
      // Handle errors, such as displaying an error message to the user
  });
}
// send request to create channel
function createChannel(user) {
  return new Promise((resolve, reject) => {
    // Get the CSRF token from the cookies
    const csrftoken = getCookie('csrftoken');

    var postData = {
      target_id: user.id,  // Assuming user id is required for the post request
      // Add any other data needed for the post request
    };

    fetch(url_get_channel, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
      },
      body: JSON.stringify(postData)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to create channel');
      }
      return response.json();
    })
    .then(data => {
      // Handle response if needed
      console.log('create_channel request successful:', data.data[0].channel_id);
      resolve(data.data[0].channel_id);
    })
    .catch(error => {
      console.error('Error sending POST request:', error);
      reject(error); // Reject the promise with the error
    });
  });
}

// Function to get CSRF token from cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
show_all_users();

// show channel when click on Username
function showChannel(user, channel_id) {
  var full_name = user.first_name + " " + user.last_name;
  chatHeader.textContent = full_name;
  chatMessages.innerHTML = '';
  get_all_messeeji(user, channel_id);
  websocket_handle(user, channel_id);
}
// show all message with given channel_id
const url_all_messeeji = '/chat/get_messeeji/'
function get_all_messeeji(user, channel_id){
  const csrftoken = getCookie('csrftoken');
  var postData = {
    channel_id : channel_id,
  }
  fetch(url_all_messeeji, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
    },
    body: JSON.stringify(postData),
  })
  .then(response => response.json())
  .then(data => {
      // console.log("all_users:", data);
      data.data.forEach(function(messeeji) {
          // console.log(messeeji);
          if (user.id == messeeji.sender_id) {
            const div = document.createElement('div');
            div.classList.add('message');
            div.classList.add('sent');
            div.textContent = messeeji.message_content;
            all_messeeji.appendChild(div);
          } else {
            const div = document.createElement('div');
            div.classList.add('message');
            div.classList.add('received');
            div.textContent = messeeji.message_content;
            all_messeeji.appendChild(div);
          }
          
      });
      scrollToBottom()
  })
  .catch(error => {
      console.error('Error fetching users:', error);
      // Handle errors, such as displaying an error message to the user
  });
}

// HANDLE WEBSOCKET
function websocket_handle(user, channel_id) {
  const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
  const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notification/${channel_id}/`;
  const socket = new WebSocket(wsEndpoint);
  // Successful connection event
  socket.onopen = (event) => {
    console.log("WebSocket connection opened!");
  };
  // Socket disconnect event
  socket.onclose = (event) => {
    console.log("WebSocket connection closed!");
  };  
  // Form submit listener
  document.getElementById('sendMessageBtn').addEventListener('click', function(event){
    event.preventDefault();
    const message = document.getElementById('messageInput').value;
    socket.send(
        JSON.stringify({
            'message_content': message,
            'channel_id': channel_id,
            'sender_id': user.id,
        })
    );
  });

  // Response from consumer on the server
  socket.addEventListener("message", (event) => {
    const messageData = JSON.parse(event.data)['data'];
    console.log(messageData);

    var sender_id = messageData['sender_id'];
    var message = messageData['message_content'];

    // Empty the message input field after the message has been sent
    if (sender_id == user.id){
        document.getElementById('messageInput').value = '';
    }

    // Append the message to the chatbox
    if (user.id == sender_id) {
      const div = document.createElement('div');
      div.classList.add('message');
      div.classList.add('sent');
      div.textContent = message;
      all_messeeji.appendChild(div);
    } else {
      const div = document.createElement('div');
      div.classList.add('message');
      div.classList.add('received');
      div.textContent = message;
      all_messeeji.appendChild(div);
    }
    scrollToBottom();
  });
}
function scrollToBottom() {
  var chatMessages = document.getElementById('chatMessages');
  chatMessages.scrollTop = chatMessages.scrollHeight;
}



// // Send message
// sendMessageBtn.addEventListener('click', () => {
//   const message = messageInput.value;
//   if (message.trim() !== '') {
//     const activeConversationIndex = findActiveConversationIndex();
//     conversations[activeConversationIndex].messages.push(message);
//     showConversation(activeConversationIndex);
//     messageInput.value = '';
//   }
// });

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

// const url_conversation = '/chat/get_conversations'

// function get_conversations(){
//     fetch(url_conversation)
//     .then(response => response.json())
//     .then(data => {
//       add_conversation(data);
//       showConversationList();
//       // console.log(conversations);
//     })
// }

// function add_conversation(data){
//     data.conversations.forEach(function(conversation){
//         var newconv = {name: conversation.title, messages: []}
//         conversations.push(newconv)
//     })
// }

// get_conversations();

// const conversationList = document.getElementById('conversationList');

// // Populate conversation list
// function showConversationList(){
//   console.log(conversations);
//   conversations.forEach(function(conversation, index){
//     const li = document.createElement('li');
//     li.textContent = conversation.name;
//     li.addEventListener('click', () => {
//       showConversation(index);
//     });

//     conversationList.appendChild(li);
    
//     // console.log(conversationList);
//   });
// }

// Show conversation
// function showConversation() {
//   const conversation = 
//   chatHeader.textContent = conversation.name;
//   chatMessages.innerHTML = '';
//   conversation.messages.forEach(function(message){
//     const div = document.createElement('div');
//     div.classList.add('message');
//     div.textContent = message;
//     chatMessages.appendChild(div);
//   });
// }

