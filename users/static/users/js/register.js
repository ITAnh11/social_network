// const upload_imageprofile_box = document.getElementById('upload-imageprofile-box');
// var cropper_avatar;
// var cropper_background;

// const input_avatar = document.getElementById('id_avatar');
// input_avatar.addEventListener('change', ()=>{
//     console.log('changed')

//     const img_data = input_avatar.files[0];
//     const url = URL.createObjectURL(img_data)

//     document.getElementById('upload-avatar-box').innerHTML = `<img src="${url}" name="avatar" id="image_avatar" width="200px">`

//     const avatar_preview = document.getElementById('img-avatar-preview');

//     const avatar = document.getElementById('image_avatar');
//     cropper_avatar = new Cropper(avatar, {
//         aspectRatio: 1,
//         minCropBoxWidth: 200,
//         crop(event) {
//         console.log(event.detail.x);
//         console.log(event.detail.y);
//         console.log(event.detail.width);
//         console.log(event.detail.height);
//         console.log(event.detail.rotate);
//         console.log(event.detail.scaleX);
//         console.log(event.detail.scaleY);

//         let canvas = this.cropper.getCroppedCanvas();
//         avatar_preview.src = canvas.toDataURL();
//         },
//     });
// })


// const input_background = document.getElementById('id_background');
// input_background.addEventListener('change', ()=>{
//     console.log('changed')

//     const img_data = input_background.files[0];
//     const url = URL.createObjectURL(img_data)

//     document.getElementById('upload-background-box').innerHTML = `<img src="${url}" id="image_background" width="200px" name="background">`

//     const background_preview = document.getElementById('img-background-preview');
//     const background = document.getElementById('image_background');
//     cropper_background = new Cropper(background, {
//         aspectRatio: 16 / 9,
//         minCropBoxWidth: 200,
//         crop(event) {
//         console.log(event.detail.x);
//         console.log(event.detail.y);
//         console.log(event.detail.width);
//         console.log(event.detail.height);
//         console.log(event.detail.rotate);
//         console.log(event.detail.scaleX);
//         console.log(event.detail.scaleY);
        
//         let canvas = this.cropper.getCroppedCanvas();
//         background_preview.src = canvas.toDataURL();
//         },
//     });
    
// })

document.getElementById('form-register').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    // collect form data
    const formData = new FormData(event.target);

    Promise.all([
        // new Promise(resolve => {
        //     if (cropper_avatar === undefined) {
        //         resolve();
        //         return;
        //     }
        //     cropper_avatar.getCroppedCanvas().toBlob((blob) => {
        //         formData.append('avatar', blob, 'avatar.png');
        //         resolve();
        //     });
        // }),
        // new Promise(resolve => {
        //     if (cropper_background === undefined) {
        //         resolve();
        //         return;
        //     }
        //     cropper_background.getCroppedCanvas().toBlob((blob) => {
        //         formData.append('background', blob, 'background.png');
        //         resolve();
        //     });
        // })
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
                window.location.href = data['redirect_url'];
            } else {
                // handle error
                alert(data['warning']);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
