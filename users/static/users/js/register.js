// const form_image = document.getElementById('upload-box')
// // console.log(form_image.innerHTML)


// const input_avatar = document.getElementById('id_avatar')
// const input_background = document.getElementById('id_background')

// let cropper_avatar = null
// let cropper_background = null

// const csrf = document.getElementsByName('csrfmiddlewaretoken')

document.getElementById('form-register').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    // collect form data
    const formData = new FormData(event.target);

    // make a POST request to the server
    fetch(event.target.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data['success']) {
            console.log(data);
            alert(data['success']);
            window.location.href = data['redirect_url'];
        } else {
            alert(data['warning'])
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// input_avatar.addEventListener('change', ()=>{
//     console.log('changed')

//     const img_data = input_avatar.files[0];
//     const url = URL.createObjectURL(img_data)

//     document.getElementById('upload-avatar-box').innerHTML = `<img src="${url}" name="avatar" id="image_avatar" width="200px">`

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
//         },
//     });
// })


// input_background.addEventListener('change', ()=>{
//     console.log('changed')

//     const img_data = input_background.files[0];
//     const url = URL.createObjectURL(img_data)

//     document.getElementById('upload-background-box').innerHTML = `<img src="${url}" id="image_background" width="200px" name="background">`

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
//         },
//     });
// })


