var post = document.querySelector(".write-post-container");
var posting = document.querySelector(".overlay");
var img_upload = document.querySelector('.img_upload');
var post_content = posting.querySelector('textArea');
const uploadArea = document.querySelector('.upload-area');
const uploadInput = document.querySelector('#upload-input');
const uploadImg = document.querySelector('.upload-img');
const uploadInfoValue = document.querySelector('.upload-info-value');
const form_submit = document.getElementById('form-submit');
const content_area = document.querySelector(".content-area");
const posted_area = document.querySelector(".posted_area");

const baseUrl = document.body.getAttribute('data-base-url');


post.addEventListener("click",function() {
    posting.style.display = 'flex';
})

// ẩn chức năng đăng bài
var escBtn = posting.querySelector("#escBtn");
escBtn.addEventListener("click",function(){
    posting.style.display = 'none';
    post_content.value = '';
})

var currentNumberFiles = 0;

function removeImg(event) {
    // Remove the node parent element of the button
    // console.log(event.target.parentNode);

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


uploadArea.addEventListener('click', function() {
    uploadInput.click();
});

uploadInput.addEventListener('change', function(event) {
    // console.log(event.target.files);

    filesAmount = event.target.files.length;

    for (var i = 0; i < filesAmount; i++) {
        var reader = new FileReader();
        reader.readAsDataURL(event.target.files[i]);
        reader.onload = function(event) {
            var html = `
                <div class="uploaded-img">
                    <img src="${event.target.result}">
                    <button type="button" class="remove-btn" onclick="removeImg(event)">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;

            uploadImg.insertAdjacentHTML('beforeend', html);
        }
    }

    currentNumberFiles += filesAmount;
    uploadInfoValue.textContent = currentNumberFiles.toString();
});


// xử lí nút đăng bài
const clickFormSubmit = () => {
    return new Promise((resolve, reject) => {
        Promise.all(promises)
            .then(() => {
                console.log("Form submit clicked");
                form_submit.click();
                resolve();
            })
            .catch(error => {
                reject(error);
            });
    });
};
const clickEscBtn = () => {
    return new Promise((resolve, reject) => {
        console.log("Esc button clicked");
        escBtn.click();
        resolve();
    });
};
var post_btn = document.querySelector(".post_btn");
post_btn.addEventListener("click", function() {
    clickFormSubmit()
        .then(() => clickEscBtn())
});



//render_post
function render_post(data,isOld){
    data.posts.forEach(function(post){
        var newDiv = 
            `<div class="status-field-container write-post-container">
            <div class="user-profile-box">
                <div class="user-profile">
                    <img src="${post.user.avatar}" alt="">
                    <div>
                        <p>${post.user.name}</p>
                        <small>${post.created_at}</small>
                    </div>
                </div>
                <div>
                    <a href="#"><i class="fas fa-ellipsis-v"></i></a>
                </div>
            </div>
            <div class="status-field">
                <p>${(post.content !== undefined && post.content !== null && post.content !== "") ? post.content : ""}</p>
                ${(post.media && post.media.length > 0) ? `<img src="${post.media[0].media}" alt="">` : ""}
            </div>
            <div class="post-reaction">
                <div class="activity-icons">
                    <div><img src="${baseUrl + "images/like-blue.png"}" alt="">120</div>
                    <div><img src="${baseUrl + "images/comments.png"}" alt="">52</div>
                    <div><img src="${baseUrl + "images/share.png"}" alt="">35</div>
                </div>
                <div class="post-profile-picture">
                    <img src="${post.user.avatar}" alt=""> <i class=" fas fa-caret-down"></i>
                </div>
            </div>
        </div>`
        var posted = document.createElement("div");
        posted.innerHTML = newDiv;

        if(isOld === "old"){
            posted_area.appendChild(posted);
        }
        else{
            var a = posted_area.children[0];
            posted_area.insertBefore(posted,a);
        }
    })
}

//upload_post
form_submit.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const images = document.querySelectorAll('.uploaded-img img');

    var content = post_content.value;
    formData.append(`content`,content);

    var number = 0;
    var promises = [];

    images.forEach(function(image) {
        // console.log(image.src)
        var promise = fetch(image.src)
        .then(response => response.blob())
        .then(blob => {
            console.log(blob);
            number += 1;
            formData.append(`media`, blob, `images_${number}.png`);
        })
        .catch(error => {
            console.error('Error:', error);
        });
        promises.push(promise);
    });

    Promise.all(promises)
        .then(() => {
        fetch(event.target.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            render_post(data,"new");
            console.log(data);
            if(data.posts[0].content === null){
                console.log("ko co noi dung");
            }
            else{
                console.log("co noi dung");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        });
});

function hiden_posting(isOwer) {
    if (isOwer === false){
        post.remove();
    }
}

//lấy bài đăng
const params = (new URL(document.location)).searchParams;
const url_user_post = '/userprofiles/get_posts/?id=' + ((params.get('id') !== null) ? params.get('id') : '');
const url_homepage_post = '/homepage/get_posts/';

const url_get_posts = (window.location.pathname == '/userprofiles/') ? url_user_post : url_homepage_post;

console.log(url_get_posts); 

function get_posts(){
    fetch(url_get_posts)
    .then(response => response.json())
    .then(data => {
        render_post(data,"old");
        hiden_posting(data.isOwner)
        console.log(data);
    })
}

get_posts();







