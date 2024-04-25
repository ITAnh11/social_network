var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
        var cover_review = document.getElementById('cover_review');
        var avt_review = document.getElementById('avt_review');
        
        cover_review.innerHTML += `<img id="img-background-preview" src ="${data.imageprofile['background']}" alt="image" style="width: 560px; height: 285px; object-fit: cover; position: relative;" />`;
        avt_review.innerHTML += `<img id="img-avatar-preview" src ="${data.imageprofile['avatar']}" alt="image" style="width: 120px; height: 120px; border-radius: 100%; object-fit: cover;
        position: relative; top: -45px; left: 20px;" />`;
        
    })
//choose and cropper avatar
const upload_imageprofile_box = document.getElementById('upload-imageprofile-box');
var cropper_avatar;
var cropper_background;
        
const input_avatar = document.getElementById('avatar');
const confirm_button_avt = document.getElementById('confirm-button-avt')
input_avatar.addEventListener('change', () => {
    // Xóa bỏ ảnh trước đó nếu có
    const existingImage = document.getElementById('image_avatar');
    if (existingImage) {
        existingImage.parentNode.removeChild(existingImage);
        cropper_avatar.destroy(); // Hủy bỏ đối tượng Cropper của ảnh trước đó
    }

    console.log('changed');

    const img_data = input_avatar.files[0];
    if (img_data) {
        const url = URL.createObjectURL(img_data);

    const avt_cropper = document.getElementById('upload-avatar-box');
    avt_cropper.innerHTML = '';
    avt_cropper.innerHTML += `<img src="${url}" id="image_avatar" name="avatar">`;

    const avatar_preview = document.getElementById('img-avatar-preview');

    const avatar = document.getElementById('image_avatar');
    cropper_avatar = new Cropper(avatar, {
        aspectRatio: 1,
        minCropBoxWidth: 200,
        autoCropArea: 0.5,
        scalable: false,
        background: false,
        crop(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);

            let canvas = this.cropper.getCroppedCanvas();
            avatar_preview.src = canvas.toDataURL();
        },
    });
        confirm_button_avt.style.display = 'flex';
    } else {
        confirm_button_avt.style.display = 'none';
    }
    
});


// choose and cropper background (coverImage)
const input_background = document.getElementById('background');
const confirm_button_bg = document.getElementById('confirm-button-bg')
input_background.addEventListener('change', () => {
    // Xóa bỏ ảnh trước đó nếu có
    const existingImage = document.getElementById('image_background');
    if (existingImage) {
        existingImage.parentNode.removeChild(existingImage);
        cropper_background.destroy(); // Hủy bỏ đối tượng Cropper của ảnh trước đó
    }

    console.log('changed');

    const img_data = input_background.files[0];
    if (img_data) {
        const url = URL.createObjectURL(img_data);

    const bg_cropper = document.getElementById('upload-background-box');
    bg_cropper.innerHTML = '';
    bg_cropper.innerHTML += `<img src="${url}" id="image_background" name="background">`;

    const background_preview = document.getElementById('img-background-preview');

    const background = document.getElementById('image_background');
    cropper_background = new Cropper(background, {
        aspectRatio: 16 / 9,
        crop(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);

            let canvas = this.cropper.getCroppedCanvas();
            background_preview.src = canvas.toDataURL();
        },
    });
        confirm_button_bg.style.display = 'flex';
    } else {
        confirm_button_bg.style.display = 'none';
    }
    
});

document.getElementById('form-editAvt').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    // collect form data
    const formData = new FormData(event.target);

    Promise.all([
        new Promise(resolve => {
            cropper_avatar.getCroppedCanvas().toBlob((blob) => {
                formData.append('avatar', blob, 'avatar.png');
                resolve();
            });
        })
    ]).then(() => {
        // make a POST request to the server
        fetch(event.target.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data['success']) {
                console.log(data);
                localStorage.setItem('avatar', data['avatar'])
                alert(data['success']);
            } else {
                // handle error
                alert(data['warning']);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

document.getElementById('form-editCover').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    // collect form data
    const formData = new FormData(event.target);

    Promise.all([
        new Promise(resolve => {
            cropper_background.getCroppedCanvas().toBlob((blob) => {
                formData.append('background', blob, 'background.png');
                resolve();
            });
        })
    ]).then(() => {
        // make a POST request to the server
        fetch(event.target.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data['success']) {
                console.log(data);
                alert(data['success']);
            } else {
                // handle error
                alert(data['warning']);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});