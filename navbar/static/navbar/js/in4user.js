var api_get_profile = '/userprofiles/get_profile'

fetch(api_get_profile) 
  .then(response => response.json())
  .then(data => {
    console.log(data);
    set_user_data(data);
    var userNames = document.getElementsByClassName('user-name');
    var userName1 = document.getElementById('userName1');
      userName1.style.color = "grey";
      userName1.style.fontWeight = "600";
      userName1.style.fontSize = "5px"; 
    for (var i = 0; i < userNames.length; i++) {
      userNames[i].innerHTML += `<h3>${data.userprofile['first_name'] + " " + data.userprofile['last_name']}</h3>`;
    }

    var profileImage = document.getElementsByClassName('profileImage');
    for (var i = 0; i < profileImage.length; i++) {
      profileImage[i].innerHTML += `<img src ="${data.imageprofile['avatar']}" alt="avatarIcon">`;
    }
  })
  function set_user_data(data) {
    localStorage.setItem('name', data.userprofile['first_name'] + " " + data.userprofile['last_name']);
    localStorage.setItem('avatar', data.imageprofile['avatar']);
  }