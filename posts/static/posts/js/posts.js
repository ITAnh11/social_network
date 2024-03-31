var post = document.querySelector(".write-post-container");
var posting = document.querySelector(".overlay");
var img_upload = document.querySelector('.img_upload');
var post_content = posting.querySelector('textArea');

post.addEventListener("click",function() {
    posting.style.display = 'flex';
})

// ẩn chức năng đăng bài
var escBtn = posting.querySelector("#escBtn");
escBtn.addEventListener("click",function(){
    posting.style.display = 'none';
    post_content.value = '';
})



const uploadArea = document.querySelector('.upload-area');
const uploadInput = document.querySelector('#upload-input');
const uploadImg = document.querySelector('.upload-img');
const uploadInfoValue = document.querySelector('.upload-info-value');
const form_submit = document.getElementById('form-submit');

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

document.addEventListener('DOMContentLoaded', function() {

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


    form_submit.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const images = document.querySelectorAll('.uploaded-img img');
    
        var number = 0;
        var promises = [];
        images.forEach(function(image) {
            // console.log(image.src);
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
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
            });
    });
});





