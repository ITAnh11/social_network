var posts_upload_box = document.querySelector("#posts-upload-box");
var post_upload_area = document.querySelector(".post-upload-textarea");
var posting = document.querySelector(".overlay");
var uploadContent = posting.querySelector('textArea');
const uploadArea = document.querySelector('.upload-area');
const uploadInput = document.querySelector('#upload-input');
const uploadImg = document.querySelector('.upload-img');
const uploadInfoValue = document.querySelector('.upload-info-value');
const form_submit = document.getElementById('form-submit');

var currentNumberFiles = 0;

function resetValueUpload() {
    uploadImg.innerHTML = '';
    uploadInfoValue.textContent = '0';
    uploadInput.value = '';
    uploadContent.value = '';
    currentNumberFiles = 0;
}

post_upload_area.addEventListener("click", function () {
    posting.style.display = 'flex';
})

// ẩn chức năng đăng bài
var escBtn = posting.querySelector("#escBtn");
escBtn.addEventListener("click", function () {
    resetValueUpload();
    posting.style.display = 'none';
})


uploadArea.addEventListener('click', function () {
    uploadInput.click();
});

// Function to handle file upload
function handleFileUpload(event) {
    var files = event.target.files;
    for (var i = 0; i < files.length; i++) {
        readFile(files[i]);
    }
}

function removeImg(event) {
    // Remove the node parent element of the button
    if (event.target.parentNode.classList.contains('uploaded-img')) {
        event.target.parentNode.remove();
    } else if (event.target.parentNode.parentNode.classList.contains('uploaded-img')) {
        event.target.parentNode.parentNode.remove();
    }

    currentNumberFiles -= 1;
    uploadInfoValue.textContent = currentNumberFiles.toString();

    if (currentNumberFiles == 0) {
        uploadInput.value = '';
    }
}

// Function to read file as data URL
function readFile(file) {
    var reader = new FileReader();
    reader.onload = function (event) {
        // Create the elements
        var uploadedImgDiv = document.createElement('div');
        uploadedImgDiv.classList.add('uploaded-img');

        var img = document.createElement('img');
        img.src = event.target.result;

        var removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.classList.add('remove-btn');
        removeBtn.onclick = function (event) {
            removeImg(event);
        };

        var icon = document.createElement('i');
        icon.classList.add('fas', 'fa-times');

        // Append elements to the container
        removeBtn.appendChild(icon);
        uploadedImgDiv.appendChild(img);
        uploadedImgDiv.appendChild(removeBtn);
        uploadImg.appendChild(uploadedImgDiv);
    };
    reader.readAsDataURL(file); // Read file as data URL
}

// Event listener for file input change
uploadInput.addEventListener('change', function (event) {
    handleFileUpload(event);
    // Update the number of uploaded files
    currentNumberFiles += event.target.files.length;
    uploadInfoValue.textContent = currentNumberFiles.toString();
});

// xử lí nút đăng bài
const clickFormSubmit = () => {
    form_submit.click();
};

var post_btn = document.querySelector(".post_btn");
post_btn.addEventListener("click", function () {
    clickFormSubmit();
});

function appendImageToFormData(images, formData) {
    var promises = [];
    var number = 0;

    images.forEach(function (image) {
        var promise = fetch(image.src)
            .then(response => response.blob())
            .then(blob => {
                number += 1;
                formData.append(`media`, blob, `images_${number}.png`);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        promises.push(promise);
    });

    return promises;
}

//upload_post
form_submit.addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const images = document.querySelectorAll('.uploaded-img img');

    var content = uploadContent.value;
    var promises = appendImageToFormData(images, formData);

    if (content === "" && images.length === 0) {
        return;
    }

    formData.append(`content`, content);

    Promise.all(promises)
        .then(() => {
            fetch(event.target.action, {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data['warning'] != null) {
                        alert(data['warning']);
                    } else if (data['error'] != null) {
                        alert(data['error']);
                    } else {
                        console.log('Success:', data);
                        render_post(data, "new");
                    }
                })
                .then(() => {
                    resetValueUpload();
                    posting.style.display = 'none';
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        });
});


//cài đặt thông tin người dùng cho phần đăng bài
function set_user_post() {
    var userProfile = document.querySelector("#posts-upload-userprofile");
    // console.log(userProfile);
    var userNameElement = userProfile.querySelector("#posts-upload-name-user");
    var userImageElement = userProfile.querySelector("#posts-upload-image-user");

    var userprofileOverlay = posting.querySelector(".user-profile");
    var userImageElement1 = userprofileOverlay.querySelector("img");
    var userNameElement1 = userprofileOverlay.querySelector("p");


    if (userNameElement) {
        userNameElement.textContent = USER_NAME;
    }
    if (userImageElement) {
        userImageElement.src = USER_AVATAR;
    }
    if (userNameElement1) {
        userNameElement1.textContent = USER_NAME;
    }
    if (userImageElement1) {
        userImageElement1.src = USER_AVATAR;
    }

}

function showUploadPostsBox() {
    var url = window.location.href;
    var params = new URLSearchParams(window.location.search);
    if (url.includes("userprofiles")) {
        if (USER_ID != params.get('id')) {
            posts_upload_box.remove();
            console.log('remove posst upload box');
            return;
        }
    }

    posts_upload_box.style.display = 'block';
}


setTimeout(() => {
    showUploadPostsBox();
    set_user_post();
}, 2000);

