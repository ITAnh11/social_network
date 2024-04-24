// Lắng nghe sự kiện khi người dùng chọn file
document.getElementById('avatar').addEventListener('change', function(event) {
    // Lấy ra file đã chọn
    const file = event.target.files[0];

    // Kiểm tra xem file có phải là ảnh không
    if (file && file.type.startsWith('image')) {
        // Tạo đối tượng FileReader để đọc file ảnh
        const reader = new FileReader();

        // Lắng nghe sự kiện khi FileReader hoàn thành việc đọc file
        reader.onload = function(e) {
            // Hiển thị ảnh đã chọn trong thẻ img
            const img = document.createElement('img');
            img.src = e.target.result;
            document.getElementById('avt-preview').innerHTML = '';
            document.getElementById('avt-preview').appendChild(img);
        };

        // Đọc file ảnh
        reader.readAsDataURL(file);
    }
});

//upload cover
document.getElementById('background').addEventListener('change', function(event) {
    // Lấy ra file đã chọn
    const file = event.target.files[0];

    // Kiểm tra xem file có phải là ảnh không
    if (file && file.type.startsWith('image')) {
        // Tạo đối tượng FileReader để đọc file ảnh
        const reader = new FileReader();

        // Lắng nghe sự kiện khi FileReader hoàn thành việc đọc file
        reader.onload = function(e) {
            // Hiển thị ảnh đã chọn trong thẻ img
            const img = document.createElement('img');
            img.src = e.target.result;
            document.getElementById('cover-preview').innerHTML = '';
            document.getElementById('cover-preview').appendChild(img);

        };

        // Đọc file ảnh
        reader.readAsDataURL(file);
    }
});