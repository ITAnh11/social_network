var api_get_profile = '/userprofiles/get_profile/'

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
        console.log(data);

        profile = document.getElementById('profile');
        profile.innerHTML += `<h3>Login with: ${data.user['email']}</h3>`
        profile.innerHTML += `<h3>Name: ${data.userprofile['first_name'] + " " + data.userprofile['last_name']}</h3>`
        profile.innerHTML += `<h3>Bio: ${data.userprofile['bio']}</h3>`
        profile.innerHTML += `<img src="${data.imageprofile['avatar']}" alt="avatar" srcset="" style="border-radius: 100%; width: 200px; height: 200px; object-fit: cover;">`;
        
        profile.innerHTML += `<img src="${data.imageprofile['background']}" alt="background" srcset="" style="width: 640px; height: 360px; object-fit: cover;">`
    })