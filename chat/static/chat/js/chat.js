
const chatHeader = document.getElementById('chatHeader');
const all_messeeji = document.getElementById('chat');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const list_all_users = document.getElementById("userList");

var activeChannels = {};

var url_all_users = "/search/@"; // Assuming this is the correct endpoint to fetch all users
var url_get_channel = "chat/create_channel/"
function show_all_users() {
  fetch(url_all_users)
  .then(response => response.json())
  .then(data => {
      current_user = data.current_user;
      console.log(current_user)
      // console.log("all_users:", data);
      data.list_users.forEach(function(user) {
          console.log(user);
          var fullName = user.first_name + " " + user.last_name;
          var li = document.createElement('li');
          li.textContent = fullName;

          li.addEventListener('click', () => {
            // Show channel logic here

            // Send POST request
            createChannel(user)
              .then(channel_id => {
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
  chat.innerHTML = '';
  get_all_messeeji(user, channel_id);
  websocket_handle(user, channel_id);
}
//add a single message to div all_messeeji
function addMessage(message, sender) {
  const div = document.createElement('div');
  div.classList.add('message');
  div.classList.add(sender);
  div.textContent = message;
  all_messeeji.appendChild(div);
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
      data.data.forEach(function(messeeji) {
          if (user.id != messeeji.sender_id) {
            addMessage(messeeji.message_content, 'parker')
          } else {
            addMessage(messeeji.message_content, 'stark')
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

  function sendMessage() {
    const message = document.getElementById('messageInput').value;
    if (message == "") return 
    socket.send(
        JSON.stringify({
            'message_content': message,
            'channel_id': channel_id,
            'sender_id': user.id,
        })
    );
    console,log("user id is:", user.id)
  }
  // Form submit listener
  document.getElementById('sendMessageBtn').addEventListener('click', function(event){
    event.preventDefault();
    sendMessage()
  });

  document.getElementById('messageInput').addEventListener('keypress', function(event){
    // Check if Enter key is pressed (key code 13)
    if (event.keyCode === 13) {
      event.preventDefault(); // Prevent the default behavior (e.g., form submission)
      sendMessage(); // Call the sendMessage function
    }
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
    if (user.id != sender_id) {
      addMessage(message, 'parker');
    } else {
      addMessage(message, 'stark');
    }
    scrollToBottom();
  });
}
function scrollToBottom() {
  var messages = document.getElementById('chat');
  messages.scrollTop = chat.scrollHeight;
}