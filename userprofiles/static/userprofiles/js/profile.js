var api_get_profile = '/userprofiles/get_profile/'

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

        var coverImage = document.getElementById('coverImage');
        coverImage.innerHTML += `<img src ="${data.imageprofile['background']}" alt="coverImage" class="coverImage">`;

        var avatarContainer = document.getElementById('avatarContainer');
        avatarContainer.innerHTML += `<img src ="${data.imageprofile['avatar']}" alt="avatar" class="dashboard-img">`;

        var profileImage = document.getElementsByClassName('profileImage');
        for (var i = 0; i < profileImage.length; i++) {
            profileImage[i].innerHTML += `<img src ="${data.imageprofile['avatar']}" alt="avatarIcon">`;
        }

        profile = document.getElementById('profile');
        profile.innerHTML += `<h3>Login with: ${data.user['email']}</h3>`     
        profile.innerHTML += `<h3>Bio: ${data.userprofile['bio']}</h3>`
        profile.innerHTML += `<img src="${data.imageprofile['avatar']}" alt="avatar" srcset="" style="border-radius: 100%; width: 200px; height: 200px; object-fit: cover;">`;
        profile.innerHTML += `<img src="${data.imageprofile['background']}" alt="background" srcset="" style="width: 640px; height: 360px; object-fit: cover;">`;
        
    })
    function set_user_data(data){
        localStorage.setItem('name', data.userprofile['first_name'] + " " + data.userprofile['last_name']);
        localStorage.setItem('avatar', data.imageprofile['avatar']);
    }

    //dgdj
    