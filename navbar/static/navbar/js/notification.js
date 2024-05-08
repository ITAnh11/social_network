const bellOffIconSrc = "/static/navbar/images/notification-bell-off.png";
const bellOnIconSrc = "/static/navbar/images/notification-bell-on.png";
const api_get_notification = "/notifications/get_notifications/";
const api_accept_friend_request = "/friends/accept_friendrequest/";
const api_decline_friend_request = "/friends/denine_friendrequest/";
const api_get_userprofilebasic = "/userprofiles/get_profile_basic/";
let notificationSocket;
let reconnectInterval = 5000;  // ms

function connectNotificationSocket() {
  notificationSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/notification/'
    + USER_ID
    + '/'
  );

  notificationSocket.onmessage = function (event) {
    console.log('Received message from server:', event.data);
    // var notification = JSON.parse(event.data);
    // var notificationItem = createNotificationItem(notification);
    // var notificationDropdown = document.querySelector(".dropdown-notification");
    // notificationDropdown.insertAdjacentHTML("afterbegin", notificationItem);
  };

  notificationSocket.onopen = function (event) {
    console.log('WebSocket is open now.');
  };

  notificationSocket.onclose = function (event) {
    console.error('WebSocket is closed now. Reconnect will be attempted in ' + (reconnectInterval / 1000) + ' second(s).', event.reason);
    setTimeout(connectNotificationSocket, reconnectInterval);
  };

  notificationSocket.onerror = function (err) {
    console.error('WebSocket encountered error: ', err.message, 'Closing socket');
    notificationSocket.close();
  };

}

setTimeout(() => {
connectNotificationSocket();
}, 2000);

var bellIcon = document.querySelector(".notification_icon");
bellIcon.addEventListener('click', function () {
  var dropdown = document.querySelector(".dropdown-notification");
  dropdown.classList.toggle("active-notification");

  var bellIcon = document.querySelector(".icon-notification-bell");
  if (dropdown.classList.contains("active-notification")) {
    bellIcon.src = bellOnIconSrc;

    getNotification();
  } else {
    bellIcon.src = bellOffIconSrc;
  }

  var dotIcon = document.querySelector(".icon-notification-dot");
  dotIcon.style.display = "none";

  notificationSocket.send(JSON.stringify({ 'message': 'get_notification' }));
});


function clickNotificationItemGoToPostPage(event, post_id) {
  // console.log(event.target);

  var url = `/posts/page/?posts_id=${post_id}&image_id=1`;

  window.open(url, "_blank");
}

function clickNotificationItemGoToProfilePage(event, user_id) {
  // console.log(event.target);
  var url = `/userprofiles/?id=${user_id}`;
  window.open(url, "_blank");
}

function clickAcceptFriendRequest(event) {
  // console.log(event.target);
  console.log("Accept friend request");
  var formData = new FormData();
  formData.append("id", event.target.getAttribute("id_friend_request"));
  fetch(api_accept_friend_request, {
    method: "POST",
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      // getNotification();
      if (data['success']) {
        var btn_notification_addfriend_container = event.target.parentElement;
        var html = `<p class="btn-notification-addfriend accept-color-addfriend" style="background-color: rgba(0, 101, 252, 0.644); width: fit-content; margin: 0px;">Accepted</p>`;
        btn_notification_addfriend_container.innerHTML = html;
      }
    });
}

function clickDeclineFriendRequest(event) {
  // console.log(event.target);
  console.log("Decline friend request");
  var formData = new FormData();
  formData.append("id", event.target.getAttribute("id_friend_request"));
  fetch(api_decline_friend_request, {
    method: "POST",
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      // getNotification();
      if (data['success']) {
        var btn_notification_addfriend_container = event.target.parentElement;
        var html = `<p class="btn-notification-addfriend decline-color-addfriend" style="background-color: #9b9b9b50; width: fit-content; margin: 0px;">Declined</p>`;
        btn_notification_addfriend_container.innerHTML = html;
      }
    });
}

function createReactNotificationItem(notification) {

  var srcIconType = "";
  if (notification.type_reaction === "like") {
    srcIconType = "/static/posts/images/like.png";
  } else if (notification.type_reaction === "love") {
    srcIconType = "/static/posts/images/love.png";
  } else if (notification.type_reaction === "haha") {
    srcIconType = "/static/posts/images/haha.png";
  } else if (notification.type_reaction === "wow") {
    srcIconType = "/static/posts/images/wow.png";
  } else if (notification.type_reaction === "sad") {
    srcIconType = "/static/posts/images/sad.png";
  } else if (notification.type_reaction === "angry") {
    srcIconType = "/static/posts/images/angry.png";
  } else if (notification.type_reaction === "care") {
    srcIconType = "/static/posts/images/care.png";
  }

  return `<div class="notify_item" 
    notification_id="${notification.id}" 
    to_posts_id="${notification.to_posts_id}" 
    to_comment_id="${notification.to_comment_id}"
    onclick="clickNotificationItemGoToPostPage(event, ${notification.to_posts_id})"
    >
    <div class="notify_img">
      <div class="user-notification">
        <img
          class="img-user-notification"
          src="${notification.user.avatar}"
          alt="profile_pic"
          style="width: 50px; border-radius: 50%"
        />
        <img
          src="${srcIconType}"
          class="icon-type-notification"
        />
      </div>
    </div>
    <div class="notify_info">
      <p class="content-notification">
        <span class="name-user-notification">${notification.user.name}</span> ${notification.content}
      </p>
      <span class="notify_time">${notification.created_at}</span>
    </div>
  </div>`
}

function createCommentNotificationItem(notification) {
  return `<div class="notify_item" 
    notification_id="${notification.id}" 
    to_posts_id="${notification.to_posts_id}" 
    to_comment_id="${notification.to_comment_id}"
    onclick="clickNotificationItemGoToPostPage(event, ${notification.to_posts_id})"
    >
    <div class="notify_img">
      <div class="user-notification">
        <img
          class="img-user-notification"
          src="${notification.user.avatar}"
          alt="profile_pic"
          style="width: 50px; border-radius: 50%"
        />
        <img
          src="/static/navbar/images/speech-bubble.png"
          class="icon-type-notification"
        />
      </div>
    </div>
    <div class="notify_info">
      <p class="content-notification">
            <span class="name-user-notification">${notification.user.name}</span> ${notification.content}
      </p>
      <span class="notify_time">${notification.created_at}</span>
    </div>
  </div>`
}

function createFriendRequestNotificationItem(notification) {
  console.log(notification);
  var statusBtnFriendRequest = "";
  if (notification.status_request == "pending") {
    statusBtnFriendRequest = `<button class="btn-notification-addfriend accept-color-addfriend" 
        onclick="clickAcceptFriendRequest(event)"
        id_friend_request="${notification.id_friend_request}"
        >Accept</button>
        <button class="btn-notification-addfriend decline-color-addfriend" 
        onclick="clickDeclineFriendRequest(event)"
        id_friend_request="${notification.id_friend_request}"
        >Decline</button>`;
  } else if (notification.status_request == "accepted") {
    statusBtnFriendRequest = `<p class="btn-notification-addfriend accept-color-addfriend" style="background-color: rgba(0, 101, 252, 0.644); width: fit-content; margin: 0px;">Accepted</p>`;
  } else if (notification.status_request == "declined") {
    statusBtnFriendRequest = `<p class="btn-notification-addfriend decline-color-addfriend" style="background-color: #9b9b9b50; width: fit-content; margin: 0px;">Declined</p>`;
  }

  return `<div class="notify_item" 
    notification_id="${notification.id}"
    >
    <div class="notify_img" onclick="clickNotificationItemGoToProfilePage(event, ${notification.user.id})">
      <div class="user-notification">
        <img
          class="img-user-notification"
          src="${notification.user.avatar}"
          alt="profile_pic"
          style="width: 50px; border-radius: 50%"
        />
        <img
          src="/static/navbar/images/notification-add-friend.png"
          class="icon-type-notification"
        />
      </div>
    </div>
    <div class="notify_info">
      <p class="content-notification" onclick="clickNotificationItemGoToProfilePage(event, ${notification.user.id})">
        <span class="name-user-notification">${notification.user.name}</span> ${notification.content}
      </p>
      <div class="btn-notification-addfriend-container">
        <!-- <button class="btn-notification-addfriend accept-color-addfriend">Accept</button>
        <button class="btn-notification-addfriend decline-color-addfriend">Decline</button> -->
        <!-- <p class="btn-notification-addfriend accept-color-addfriend" style="background-color: rgba(0, 101, 252, 0.644); width: fit-content; margin: 0px;">Accepted</p> -->
        <!-- <p class="btn-notification-addfriend decline-color-addfriend" style="background-color: #9b9b9b50; width: fit-content; margin: 0px;">Declined</p> -->
        ${statusBtnFriendRequest}
      </div>
      <span class="notify_time">${notification.created_at}</span>
    </div>
  </div>`;
}

function createNotificationItem(notification) {
  if (notification.type === "reaction") {
    return createReactNotificationItem(notification);
  } else if (notification.type === "comment") {
    return createCommentNotificationItem(notification);
  } else if (notification.type === "add_friend") {
    return createFriendRequestNotificationItem(notification);
  }
}

function renderNotificationList(notifications) {
  var notificationDropdown = document.querySelector(".dropdown-notification");
  notificationDropdown.innerHTML = "";
  notifications.forEach(notification => {
    var notificationItem = createNotificationItem(notification);
    notificationDropdown.insertAdjacentHTML("afterbegin", notificationItem);
  });
}

function getNotification() {
  fetch(api_get_notification)
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      renderNotificationList(data.notifications);
    });
}

