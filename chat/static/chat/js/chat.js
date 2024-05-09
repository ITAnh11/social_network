const chatHeader = document.getElementById('chatHeader');
const all_messeeji = document.getElementById('chat');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const list_all_users = document.getElementById("userList");
const url_all_messeeji = '/chat/get_messeeji/'
const socketMap = {};
const chatContainer = document.querySelector('.chat-container');
const toggleChatBtn = document.getElementById('toggleChat');
const chatBox = document.getElementById('chatBox');
var inActiveSocket = null;
var current_user = localStorage.getItem('id');
toggleChatBtn.style.display = 'none';
var moreLink = document.createElement('a');
moreLink.textContent = "More";
moreLink.href = "#";
moreLink.className = 'more-link';

// Ensure the elements exist before adding event listener
if (toggleChatBtn && chatContainer) {
    // Toggle chat box visibility
    toggleChatBtn.addEventListener('click', (event) => {
        event.preventDefault();
        chatContainer.classList.toggle('closed');
        //chatBox.classList.remove('hide');
        toggleChatBtn.textContent = chatContainer.classList.contains('closed') ? 'Show chat' : 'Hide chat';
    });
}
document.addEventListener("DOMContentLoaded", function() {
  const contactList = document.getElementById('userList');


  // Add click event listener to each contact
  contactList.addEventListener('click', function(event) {
    const contact = event.target.closest('.contact');
    if (contact) {
      // Get user ID from data attribute
      const userId = contact.dataset.userId;
      // You can load chat history, user info, etc. based on the user ID
      // For simplicity, let's just show the chat box
      chatBox.classList.remove('hide');
      if (chatContainer.classList.contains('closed')) { // Check if chat container is closed
        chatContainer.classList.remove('closed'); // Open chat container
        toggleChatBtn.textContent = 'Hide chat'; // Change button text
    }
      toggleChatBtn.style.display = ''
    }
  });
});

function mark_as_read(channel_id, sender_id) {
  const csrftoken = getCookie('csrftoken');
  const url_mark_as_read = '/chat/mark_as_read/';
  const postData = {
    channel_id: channel_id,
    sender_id: sender_id,
  };
  fetch(url_mark_as_read, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(postData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to mark message as read');
    } else {
      
    }
  })
  .catch(error => {
    console.error('Error marking message as read:', error);
  });
}


list_all_users.appendChild(moreLink);
var url_all_users = "/search/@"; // Assuming this is the correct endpoint to fetch all users
var url_all_contact_users = "chat/all_contact_users";
var url_get_channel = "chat/create_channel/"

// Variable to store the URL of the next page
var nextPageUrl = url_all_contact_users;

// Function to fetch and display more users
function showMoreUsers() {
    if (nextPageUrl) {
        fetch(nextPageUrl)
            .then(response => response.json())
            .then(data => {
                console.log("data", data)
                current_user = data.results.current_user;
                if (data.next) {
                    nextPageUrl = data.next;
                } else {
                    moreLink.style.display = 'none';
                }
                data.results.list_users.forEach(function(user) {
                    var fullName = user.first_name + " " + user.last_name;
                    var divContact = document.createElement('div');
                    divContact.className = 'contact';
                    divContact.setAttribute('data-user-id', user.id);
                    var img = document.createElement('img');
                    img.className = 'pic';
                    img.setAttribute('src', user.avatar);
                    var divContactInfo = document.createElement('div');
                    divContactInfo.className = 'contact-info';
                    var divName = document.createElement('div');
                    divName.className = 'name';
                    divName.textContent = fullName;
                    var divMessage = document.createElement('div');
                    divMessage.className = 'message';
                    divMessage.textContent = 'Last message';
                    var divBadge = document.createElement('div');
                    divBadge.className = 'badge';
                    if (user.unread_amount == 0) {
                      divBadge.style.display = 'none'
                    } 
                    divBadge.textContent = user.unread_amount;
                    divContactInfo.appendChild(divName);
                    divContactInfo.appendChild(divMessage);
                    divContact.appendChild(img);
                    divContact.appendChild(divContactInfo);
                    divContact.appendChild(divBadge);
                    divContact.addEventListener('click', () => {
                        createChannel(user)
                            .then(channel_id => {
                                showChannel(user, channel_id);
                            })
                            .catch(error => {
                                console.error('Failed to create channel:', error);
                            });
                    });
                    list_all_users.appendChild(divContact);
                });
            })
            .catch(error => {
                console.error('Error fetching users:', error);
            });
    }
}

// Event listener for the "More" link
moreLink.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default link behavior
    showMoreUsers(); // Fetch and display more users
});

// Initial call to fetch and display users
showMoreUsers();

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
//show_all_users();
// show channel when click on Username
function showChannel(user, channel_id) {
  console.log("channel: ", channel_id)
  var full_name = user.first_name + " " + user.last_name;
  chatHeader.textContent = full_name;
  var img = document.createElement('img');
  img.className = 'avt';
  img.setAttribute('src', user.avatar);
  chatHeader.appendChild(img); 
  get_all_messeeji(user, channel_id)
  .then(() => {
    // Mark all messages in the channel as read

    mark_as_read(channel_id, user.id);
  })
  .catch(error => {
    console.error('Error fetching messages:', error);
  });

  websocket_handle(user, channel_id);
}
//add a single message to div all_messeeji
function addMessage(message, sender) {
  console.log("message added: ",message)
  const div = document.createElement('div');
  div.classList.add('message');
  div.classList.add(sender);
  div.textContent = message;
  all_messeeji.appendChild(div);
}

// show all message with given channel_id
function get_all_messeeji(user, channel_id){
  return new Promise((resolve, reject) => {
    all_messeeji.innerHTML = '';
    const csrftoken = getCookie('csrftoken');

    var postData = {
      channel_id: channel_id,
    };

    fetch(url_all_messeeji, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify(postData),
    })
    .then(response => response.json())
    .then(data => {
      data.data.forEach(function(messeeji) {
        if (current_user == messeeji.sender_id) {
          addMessage(messeeji.message_content, 'parker')
        } else {
          addMessage(messeeji.message_content, 'stark')
        }
      });
      scrollToBottom();
      resolve(); // Resolve the Promise after messages are fetched
    })
    .catch(error => {
      console.error('Error fetching messages:', error);
      reject(error); // Reject the Promise if there's an error
    });
  });
}

// Gắn sự kiện click cho các tin nhắn để xử lý khi người dùng đọc tin nhắn
all_messeeji.addEventListener('click', function(event) {
  // Kiểm tra xem người dùng đã nhấp vào tin nhắn hay không
  const message = event.target.closest('.message');
  if (message) {
      // Đánh dấu tin nhắn đã đọc và ẩn divBadge tương ứng
      const divBadge = message.querySelector('.badge');
      if (divBadge) {
          divBadge.style.display = 'none'; // Ẩn divBadge
      }
  }
});

// Gắn sự kiện cho nút gửi tin nhắn
sendMessageBtn.addEventListener('click', function(event) {
  if (inActiveSocket != null) {
    event.preventDefault();
    console.log("current user: ", current_user)
    sendMessage();
  }
});

messageInput.addEventListener('keypress', function(event) {
  if ((event.keyCode === 13) && (inActiveSocket != null)) {
    event.preventDefault();
    console.log("current user: ", current_user)
    sendMessage();
  }
});

function sendMessage() {
  const message = messageInput.value.trim();
  if (!message) return;
  socketMap[inActiveSocket].send(
      JSON.stringify({
          'message_content': message,
          'channel_id': inActiveSocket,
          'sender_id': current_user,
      })
  );
}

// HANDLE WEBSOCKET
function websocket_handle(user, channel_id) {
  if (socketMap[inActiveSocket]) {
    // Close the existing WebSocket connection
    socketMap[inActiveSocket].close();
    console.log("Closed existing WebSocket connection for channel:", inActiveSocket);
  }

  const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
  const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/chat_notification/${channel_id}/`;
  socketMap[channel_id] = new WebSocket(wsEndpoint);

  inActiveSocket = channel_id;
  // Successful connection event
  socketMap[channel_id].onopen = (event) => {
    console.log("WebSocket connection opened!");
  };
  // Socket disconnect event
  socketMap[channel_id].onclose = (event) => {
    console.log("WebSocket connection closed!");
  };  

  socketMap[channel_id].addEventListener("message", (event) => {
    const messageData = JSON.parse(event.data)['data'];
    console.log(messageData);

    var sender_id = messageData['sender_id'];
    var message = messageData['message_content'];

    // Empty the message input field after the message has been sent
    if (sender_id == current_user){
        document.getElementById('messageInput').value = '';
    }
    // Append the message to the chatbox
    if (current_user == sender_id) {
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