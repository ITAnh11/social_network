var api_get_profile = '/userprofiles/getprofile/'

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        user = data.user;
        userprofile = data.userprofile;
        imageprofile = data.imageprofile;

        profile = document.getElementById('profile');
        profile.innerHTML += `<h3>Login with: ${user['email']}</h3>`
        profile.innerHTML += `<h3>Name: ${userprofile['first_name'] + " " + userprofile['last_name']}</h3>`
        profile.innerHTML += `<h3>Bio: ${userprofile['bio']}</h3>`
        profile.innerHTML += `<img src="${imageprofile['avatar']}" alt="avatar" srcset="" style="border-radius: 100%; width: 200px; height: 200px; object-fit: cover;">`
        profile.innerHTML += `<img src="${imageprofile['background']}" alt="background" srcset="" style="width: 400px; height: 400px; object-fit: cover;">`
    })