const avatarContainer = document.getElementById('avatarContainer');
const dashboard_img = document.getElementById('dashboard-img');
const avatarOptions = document.getElementById('avatarOptions');

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
