var api_get_profile = '/userprofiles/get_profile/';

function getUserProfile() {
  if (localStorage.getItem('id') != null) {
    setUserProfileForNavbar();
    return;
  }
  console.log('getUserProfile');
  fetch(api_get_profile) 
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      cacheUserprofile(data);
      setUserProfileForNavbar();
    })
}

function setUserProfileForNavbar() {
  nameUser = localStorage.getItem('name');
  avatar = localStorage.getItem('avatar');

  var userName1 = document.getElementById('userName1');
  userName1.innerHTML += `<h4>${nameUser}</h4>`;
    
  var profileImage = document.getElementsByClassName('profileImage');
  for (var i = 0; i < profileImage.length; i++) {
    profileImage[i].innerHTML += `<img src ="${avatar}" alt="avatarIcon">`;
  }
}

function cacheUserprofile(data) {
    localStorage.setItem('name', data.userprofile['first_name'] + " " + data.userprofile['last_name']);
    localStorage.setItem('avatar', data.imageprofile['avatar']);
    localStorage.setItem('id', data.imageprofile['user_id']);
}

getUserProfile();