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

        // Kiểm tra nếu người dùng là chủ sở hữu của trang cá nhân

        var editProfile = document.getElementById('editProfile');
        var editStoryButton = document.getElementById('editStoryButton');
        var id_user = data.userprofile['user_id'];

        if (data.isOwner === true) {
            // Hiển thị nút chỉnh sửa thông tin cá nhân
            editProfile.innerHTML = `<button type="button" id="editProfileReal"> <i class="far fa-edit"></i><a href="${urlFromEditProfile}" style="text-decoration: none; color: white;">Edit your profile</a></button>`;
        } else {
            // Người dùng không phải là chủ sở hữu, kiểm tra trạng thái quan hệ bạn bè

            // Gọi API để kiểm tra trạng thái quan hệ bạn bè với người dùng khác
            fetch('http://127.0.0.1:8000/friends/get_statusfriend/?id=' + id_user)
                .then(response => response.json())
                .then(data => {
                    // Kiểm tra trạng thái quan hệ bạn bè
                    if (data.status_relationship === 'user') {
                        editProfile.innerHTML = `<button type="button" id="editProfileReal"> <i class="far fa-edit"></i><a href="${urlFromEditProfile}" style="text-decoration: none; color: white;">Edit your profile</a></button>`;
                    } else if (data.status_relationship === 'not_friend' || data.status_relationship === 'denied') {
                        // Hiển thị nút gửi lời mời kết bạn
                        editProfile.innerHTML = `<button type="button" onclick="sendFriendRequest(${id_user})"> <i class="fas fa-user-plus"></i> Send Friend Request</button>`;
                    } else if (data.status_relationship === 'pending') {
                        // Hiển thị nút gửi lời mời kết bạn
                        editProfile.innerHTML = `<button type="button" onclick="sentFriendRequest(${id_user})"> <i class="fas fa-check"></i> Sent Friend Request</button>`;
                    } else if (data.status_relationship === 'friend') {
                        // Hiển thị nút hủy kết bạn
                        editProfile.innerHTML = `<button type="button" onclick="cancelFriendRequest(${id_user})"> <i class="fas fa-user-friends"></i> Unfriend</button>`;
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

function getStatusFriend(userId) {
    // Gửi yêu cầu API để kiểm tra trạng thái bạn bè giữa người dùng hiện tại và người dùng có ID là 'userId'
    fetch('http://127.0.0.1:8000/userprofiles/?id=' + userId)
        .then(response => response.json())
        .then(data => {
            // Xử lý kết quả trả về từ API
            if (data.status_relationship === 'user') {
                console.log('Bạn đang xem trang của chính mình.');
            } else if (data.status_relationship === 'not_friend') {
                console.log('Bạn và người này chưa là bạn bè.');
                // Thực hiện các hành động khi hai người chưa là bạn bè
            } else {
                console.log('Bạn và người này đã là bạn bè.');
                // Thực hiện các hành động khi hai người đã là bạn bè
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Gọi hàm getStatusFriend với userId của người dùng khác
var otherUserId = '1';
getStatusFriend(otherUserId);