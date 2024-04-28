let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slides[slideIndex-1].style.display = "block";  
}

// function postComment(event) {
//   var commentText = document.getElementById("commentText").value;
//   if (commentText.trim() !== "") {
//     var commentContent = document.getElementById("commentContent");
//     var newComment = document.createElement("div");
//     newComment.classList.add("comment_setting");
//     newComment.innerHTML = `
//       <div class="avt_user">
//         <img src="{%static 'userprofiles/images/avatar.png' %}">
//       </div>
//       <div class="cmt"> 
//         <h3 class="name_user">MinhTuan</h3>
//         <p class="contentOfCmt">${commentText}</p>
//       </div>
//     `;
//     commentContent.appendChild(newComment);
//   }
// }

function showReplyBox() {
  var replyBox = document.getElementById("replyBox");
  if (replyBox.style.display === "none") {
    replyBox.style.display = "block";
  } else {
    replyBox.style.display = "none";
  }
}


function postReply() {
  var replyText = document.getElementById("replyText").value;
  if (replyText.trim() !== "") {
    var replyContent = document.getElementById("commentContent");
    var newReply = document.createElement("div");
    newReply.classList.add("comment_setting");
    newReply.innerHTML = `
      <div class="avt_user">
        <img src="{%static 'userprofiles/images/avatar.png' %}">
      </div>
      <div class="cmt"> 
        <h3 class="name_user">MinhTuan</h3>
        <p class="contentOfCmt">${replyText}</p>
      </div>
    `;
    replyContent.appendChild(newReply);
    document.getElementById("replyText").value = ""; 
    document.getElementById("replyBox").style.display = "none"; 
  }
}

document.getElementById('commentBox').addEventListener('click', function(event) {
  event.preventDefault(); // prevent form submission
  console.log(event.target.getAttribute('posts_id'));
  // collect form data
  const formData = new FormData();
  
  const content = document.getElementById('commentText').value;
  console.log(content);
  formData.append('content', content);
  formData.append('posts_id', event.target.getAttribute('posts_id'));
  formData.append('user_id', localStorage.getItem('id'));
  formData.append('user_name', localStorage.getItem('name'));
  formData.append('user_avatar', localStorage.getItem('avatar'));
  formData.append('comment_id', -1);
  // formData.append('csrfmiddlewaretoken', csrftoken);

  Promise.all([
      
  ]).then(() => {
      // make a POST request to the server
    fetch('/comments/create_comment/', {
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

function render_comment(data){ {

  data.comments.forEach(comment => {
      var comment_id = comment.id;
      var content = comment.content;
      var created_at = comment.created_at;
      var user = comment.user;

      var comment = `<div id="comment-${comment_id}" class="comment_setting">
                        <div class="avt_user">
                            <img src="${user.avatar}" alt="">
                        </div>
                        <div class="cmt">
                            <h3 class="name_user">${user.name}</h3>
                            <p class="contentOfCmt">${content}</p>
                        </div>
                      </div>`;
      var commentContent = document.getElementById('commentContent');
      commentContent.innerHTML += comment;
  });
  
  }
}

function getCommentsFromLocalStorage() {
  var comments = localStorage.getItem('comments');
  return comments ? JSON.parse(comments) : [];
}

function saveCommentsToLocalStorage(comments) {
  localStorage.setItem('comments', JSON.stringify(comments));
}

function postComment() {
  var commentText = document.getElementById('commentText').value;
  var newComment = {
    id: localStorage.getItem('id'),
    content: commentText,
    created_at: new Date(),
    user: {
      name: localStorage.getItem('name'), 
      avatar: localStorage.getItem('avatar'),
    }
  };
  console.log(newComment);
  var comments = getCommentsFromLocalStorage();
  comments.push(newComment);

  saveCommentsToLocalStorage(comments);

  render_comment({ comments: [newComment] });
}

// Khi trang được tải, render lại danh sách bình luận từ Local Storage
window.onload = function() {
  var comments = getCommentsFromLocalStorage();
  render_comment({ comments: comments });
};
