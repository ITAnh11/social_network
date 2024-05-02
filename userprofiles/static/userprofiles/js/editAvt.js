var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();
const avatarContainer = document.getElementById('avatarContainer');
const dashboard_img = document.getElementById('dashboard-img');
const avatarOptions = document.getElementById('avatarOptions');

const urlEditImages = document.body.getAttribute('link-editImages');
var chooseAvatarButton = document.getElementById('chooseAvatarButton');

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
        if (data.isOwner === true) {
            chooseAvatarButton.innerHTML += `<a href="${urlEditImages}">
                                                <button onclick="chooseAvatar()">Choose Avatar</button>
                                            </a>`;
        } else {
            console.log('Không thể chỉnh sửa avatar');
        }
    })



avatarContainer.addEventListener('click', function(event) {
    event.stopPropagation(); 
    avatarOptions.style.display = 'block';
});

document.addEventListener('click', function(event) {
    avatarOptions.style.display = 'none';
});

avatarOptions.addEventListener('mouseleave', function() {
    avatarOptions.style.display = 'none';
});

function viewAvatar() {
    window.open(dashboard_img.src, '_blank');
}

function chooseAvatar() {
    alert('Chọn ảnh đại diện');
}
