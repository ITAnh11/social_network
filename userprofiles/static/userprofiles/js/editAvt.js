// Lấy các phần tử từ HTML
const avatarContainer = document.getElementById('avatarContainer');
const avatarImage = document.getElementById('avatarImage');
const avatarOptions = document.getElementById('avatarOptions');

// Xử lý sự kiện click vào avatar để hiển thị menu lựa chọn
avatarContainer.addEventListener('click', function(event) {
    event.stopPropagation(); // Ngăn sự kiện click lan ra các phần tử cha
    avatarOptions.style.display = 'block'; // Hiển thị menu lựa chọn
});

// Xử lý sự kiện click ra ngoài để thu lại menu lựa chọn
document.addEventListener('click', function(event) {
    avatarOptions.style.display = 'none'; // Thu lại menu lựa chọn khi click ra ngoài
});

// Xử lý sự kiện mouseleave trên menu lựa chọn để thu lại khi di chuột ra khỏi menu
avatarOptions.addEventListener('mouseleave', function() {
    avatarOptions.style.display = 'none'; // Thu lại menu lựa chọn khi di chuột ra khỏi menu
});

// Hàm xem ảnh đại diện
function viewAvatar() {
    // Thêm logic xem ảnh đại diện ở đây (ví dụ: mở ảnh đại diện trong cửa sổ mới)
    window.open(avatarImage.src, '_blank');
}

// Hàm chọn ảnh đại diện
function chooseAvatar() {
    // Thêm logic chọn ảnh đại diện ở đây (ví dụ: hiển thị thông báo)
    alert('Chọn ảnh đại diện');
}
