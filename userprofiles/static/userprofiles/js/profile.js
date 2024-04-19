var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();
// console.log(api_get_profile);
const urlFromEditProfile = document.body.getAttribute('link-url');

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        set_user_data(data);
        // edit profile
        var userName2 = document.getElementById('userName2');
        userName2.innerHTML += `<h3>${data.userprofile['first_name'] + " " + data.userprofile['last_name']}</h3>`;

        var coverImage = document.getElementById('coverImage');
        coverImage.innerHTML += `<img src ="${data.imageprofile['background']}" alt="coverImage" class="coverImage">`;

        var avatarContainer = document.getElementById('avatarContainer');
        avatarContainer.innerHTML += `<img src ="${data.imageprofile['avatar']}" alt="avatar" class="dashboard-img">`;

        var editProfile = document.getElementById('editProfile');
        var id_user = data.userprofile['user_id'];

        if (data.isOwner === true) {
            editProfile.innerHTML = `<button type="button" id="editProfileReal"> <i class="far fa-edit"></i><a href="${urlFromEditProfile}" style="text-decoration: none; color: white;">Edit your profile</a></button>`;
        }
        else {
            editProfile.innerHTML = `<button type="button"> <i class="fas fa-user-plus"></i> Add to your friend</button>`;
        }

        // edit story
        var intro_bio = document.getElementById('intro_bio');
        intro_bio.innerHTML += `<p>${data.userprofile['bio']}</p>`;

        //
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
    