var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();
// console.log(api_get_profile);
const urlFromEditProfile = document.body.getAttribute('link-url-editProfile');
const urlFromEditStory = document.body.getAttribute('link-url-editStory');

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
        var userName2 = document.getElementById('userName2');
        userName2.innerHTML += `<h3>${data.userprofile['first_name'] + " " + data.userprofile['last_name']}</h3>`;

        var coverImage = document.getElementById('coverImage');
        coverImage.innerHTML += `<img src ="${data.imageprofile['background']}" alt="coverImage" class="coverImage">`;

        var avatarContainer = document.getElementById('avatarContainer');
        avatarContainer.innerHTML += `<img src ="${data.imageprofile['avatar']}" alt="avatar" class="dashboard-img">`;

        var editProfile = document.getElementById('editProfile');
        var editStoryButton = document.getElementById('editStoryButton');
        var id_user = data.userprofile['user_id'];
        
        if (data.isOwner === true) {
            editProfile.innerHTML = `<button type="button" id="editProfileReal"> <i class="far fa-edit"></i><a href="${urlFromEditProfile}" style="text-decoration: none; color: white;">Edit your profile</a></button>`;
            editStoryButton.innerHTML += `<a href="${urlFromEditStory}" class="editStory">
                                            <button type="button" class="edit-story-btn">
                                                <i class="far fa-edit"></i> Edit your story
                                            </button>
                                         </a>`;
        }
        else {
            editProfile.innerHTML = `<button type="button"> <i class="fas fa-user-plus"></i> Add to your friend</button>`;

        }

        // edit story
        var intro_bio = document.getElementById('intro_bio');
        intro_bio.innerHTML += `<p>${data.userprofile['bio']}</p>`;

        var work = document.getElementById('work');
        work.innerHTML += `${data.userprofile['work']}`;

        var address_work = document.getElementById('address_work');
        address_work.innerHTML += `${data.userprofile['address_work']}`;

        var address = document.getElementById('address');
        address.innerHTML += `${data.userprofile['address']}`;

        var place_birth = document.getElementById('place_birth');
        place_birth.innerHTML += `${data.userprofile['place_birth']}`;

        var social_link = document.getElementById('social_link');
        social_link.innerHTML += `<a href="https://www.instagram.com/${data.userprofile['social_link']}/"><p>${data.userprofile['social_link']}</p></a>`;
        // social_link.innerHTML  += `<a href=></a>${data.userprofile['social_link']}`;
        //
        profile = document.getElementById('profile');
        profile.innerHTML += `<h3>Login with: ${data.user['email']}</h3>`     
        profile.innerHTML += `<h3>Bio: ${data.userprofile['bio']}</h3>`
        profile.innerHTML += `<img src="${data.imageprofile['avatar']}" alt="avatar" srcset="" style="border-radius: 100%; width: 200px; height: 200px; object-fit: cover;">`;
        profile.innerHTML += `<img src="${data.imageprofile['background']}" alt="background" srcset="" style="width: 640px; height: 360px; object-fit: cover;">`;
        
    })

    //dgdj
    