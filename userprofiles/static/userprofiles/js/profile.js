var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();
// console.log(api_get_profile);
const urlFromEditProfile = document.body.getAttribute('link-url-editProfile');
const urlFromEditStory = document.body.getAttribute('link-url-editStory');

// thu hồi lời mời kết bạn 
function revokeFriendRequest(id_user) {
    var formdata = new FormData();
    formdata.append("id", id_user);
    formdata.append("csrfmiddlewaretoken", csrftoken);

    fetch('/friends/revoke_friendrequest/', {
        method: 'POST',
        body: formdata,
    })
    .then(response => {
        if (response.ok) {
            editProfile.innerHTML = `<button type="button" onclick="sentFriendRequest(${id_user})"> <i class="fas fa-user-plus"></i> Add Friend</button>`;
            return response.json();
        } else {
            throw new Error('Failed to revoke friend request');
        }
    })
    .then(data => {
        if (data['success']) {
            console.log(data);
        // data.status_relationship = 'not_friend';
        } else {
            // handle error
            alert(data['warning']);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Xử lý lỗi nếu cần
    });
}

// ấn gửi kết bạn cho người khác
function sentFriendRequest(id_user) {
    var formdata = new FormData();
    formdata.append("id", id_user);
    formdata.append("csrfmiddlewaretoken", csrftoken);

    fetch('/friends/sent_friendrequest/', {
        method: 'POST',
        body: formdata,
    })
    .then(response => {
        if (response.ok) {
            editProfile.innerHTML = `<button type="button" onclick="revokeFriendRequest(${id_user})"> <i class="fas fa-check"></i> Sent Friend Request</button>`;
            return response.json();
        } else {
            throw new Error('Failed to sent friend request');
        }
    })
    .then(data => {
        if (data['success']) {
            console.log(data);
        } else {
            // handle error
            alert(data['warning']);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Xử lý lỗi nếu cần
    });
}

// Đồng ý kết bạn 
function acceptFriendRequest(id_user) {
    console.log(id_user);
    var formdata = new FormData();
    formdata.append("id", id_user);
    formdata.append("csrfmiddlewaretoken", csrftoken);

    fetch('/friends/accept_friendrequestprofile/', {
        method: 'POST',
        body: formdata,
    })
    .then(response => {
        if (response.ok) {
            editProfile.innerHTML = `<button type="button" onclick="cancelFriendRequest(${id_user})"> <i class="fas fa-user-friends"></i>Friend</button>`;
            return response.json();
        } else {
            throw new Error('Failed to accept friend request');
        }
    })
    .then(data => {
        if (data['success']) {
            console.log(data);
        } else {
            // handle error
            alert(data['warning']);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Xử lý lỗi nếu cần
    });
}

// Không chấp nhận kết bạn
function deninedFriendRequest(id_user) {
    var formdata = new FormData();
    formdata.append("id", id_user);
    formdata.append("csrfmiddlewaretoken", csrftoken);

    fetch('/friends/denine_friendrequestprofile/', {
        method: 'POST',
        body: formdata,
    })
    .then(response => {
        if (response.ok) {
            editProfile.innerHTML = `<button type="button" onclick="sentFriendRequest(${id_user})"> <i class="fas fa-user-plus"></i> Add Friend</button>`;
            return response.json();
        } else {
            throw new Error('Failed to deny friend request');
        }
    })
    .then(data => {
        if (data['success']) {
            console.log(data);
        } else {
            // handle error
            alert(data['warning']);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Xử lý lỗi nếu cần
    });
}
// Huỷ kết bạn
function cancelFriendRequest(id_user) {
    var formdata = new FormData();
    formdata.append("id", id_user);
    formdata.append("csrfmiddlewaretoken", csrftoken);

    fetch('/friends/cancel_friendrequest/', {
        method: 'POST',
        body: formdata,
    })
    .then(response => {
        if (response.ok) {
            editProfile.innerHTML = `<button type="button" onclick="sentFriendRequest(${id_user})"> <i class="fas fa-user-plus"></i> Add Friend</button>`;
            return response.json();
        } else {
            throw new Error('Failed to cancel friend request');
        }
    })
    .then(data => {
        if (data['success']) {
            console.log(data);
        } else {
            // handle error
            alert(data['warning']);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Xử lý lỗi nếu cần
    });
}

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {

        var userName2 = document.getElementById('userName2');
        userName2.innerHTML += `<h3>${data.userprofile['first_name'] + " " + data.userprofile['last_name']}</h3>`;

        var coverImage = document.getElementById('coverImage');
        coverImage.innerHTML += `<img src ="${data.imageprofile['background']}" alt="coverImage" class="coverImage">`;

        var avatarContainer = document.getElementById('avatarContainer');
        avatarContainer.innerHTML += `<img src ="${data.imageprofile['avatar']}" alt="avatar" class="dashboard-img" id="dashboard-img">`;

        // Kiểm tra nếu người dùng là chủ sở hữu của trang cá nhân

        var editProfile = document.getElementById('editProfile');
        var editStoryButton = document.getElementById('editStoryButton');
        var id_user = data.userprofile['user_id'];

        if (data.isOwner === true) {
            // Hiển thị nút chỉnh sửa thông tin cá nhân
            editProfile.innerHTML = `<button type="button" id="editProfileReal"> <i class="far fa-edit"></i><a href="${urlFromEditProfile}" style="text-decoration: none; color: white;">Edit your profile</a></button>`;
            editStoryButton.innerHTML +=`<a href="${urlFromEditStory}" class="editStory">
                                            <button type="button" class="edit-story-btn">
                                                    <i class="far fa-edit"></i> Edit your story
                                            </button>
                                         </a>`;
        } else {
            // Người dùng không phải là chủ sở hữu, kiểm tra trạng thái quan hệ bạn bè

            // Gọi API để kiểm tra trạng thái quan hệ bạn bè với người dùng khác
            fetch('/friends/get_statusfriend/?id=' + id_user)
                .then(response => response.json())
                .then(data => {
                    // Kiểm tra trạng thái quan hệ bạn bè
                    if (data.status_relationship === 'user') {
                        editProfile.innerHTML = `<button type="button" id="editProfileReal"> <i class="far fa-edit"></i><a href="${urlFromEditProfile}" style="text-decoration: none; color: white;">Edit your profile</a></button>`;
                    } else if (data.status_relationship === 'not_friend' || data.status_relationship === 'denied') {
                        editProfile.innerHTML = `<button type="button" onclick="sentFriendRequest(${id_user})"> <i class="fas fa-user-plus"></i> Add Friend</button>`;
                    } else if (data.status_relationship === 'friendrequestfromuser') {
                        editProfile.innerHTML = `<button type="button" onclick="revokeFriendRequest(${id_user})"> <i class="fas fa-check"></i> Sent Friend Request</button>`; 
                    } else if (data.status_relationship === 'friendrequesttouser') {
                        editProfile.innerHTML =`<button type="button" onclick="acceptFriendRequest(${id_user})">
                                                    <i class="fas fa-check"></i>
                                                    Accept
                                                </button>
                                                <button type="button" onclick="deninedFriendRequest(${id_user})">
                                                    <i class="fas fa-times"></i>
                                                    Denined
                                                </button>`;
                    } else if (data.status_relationship === 'accepted') {
                        editProfile.innerHTML = `<button type="button" onclick="cancelFriendRequest(${id_user})"> <i class="fas fa-user-friends"></i> Friend</button>`;
                    } 
                })
                .catch(error => {
                    console.error('Error:', error);
                });
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
    })

