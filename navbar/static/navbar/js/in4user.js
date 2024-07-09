const api_get_profile_basic = "/userprofiles/get_profile_basic/";

let USER_ID = "";
let USER_NAME = "";
let USER_AVATAR = "";

function get_user_profile() {
    fetch(api_get_profile_basic)
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            USER_ID = data['id'];
            USER_NAME = data['name'];
            USER_AVATAR = data['avatar'];
            setUserProfileForNavbar();
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

get_user_profile();

function setUserProfileForNavbar() {
  var userName1 = document.getElementById('userName1');
  userName1.innerHTML += `<h4>${USER_NAME}</h4>`;
    
  var profileImage = document.getElementsByClassName('profileImage');
  for (var i = 0; i < profileImage.length; i++) {
    profileImage[i].innerHTML += `<img src ="${USER_AVATAR}" alt="avatarIcon">`;
  }
}
