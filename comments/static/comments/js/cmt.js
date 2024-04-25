
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

// button cmt in react 
function showCommentBox() {
  var commentBox = document.getElementById("commentBox");
  if (commentBox.style.display === "none") {
    commentBox.style.display = "block";
  } else {
    commentBox.style.display = "none";
  }
}

function showReplyBox() {
  var replyBox = document.getElementById("replyBox");
  if (replyBox.style.display === "none") {
    replyBox.style.display = "block";
  } else {
    replyBox.style.display = "none";
  }
}

function postComment() {
  var commentText = document.getElementById("commentText").value;
  if (commentText.trim() !== "") {
    var commentContent = document.getElementById("commentContent");
    var newComment = document.createElement("div");
    newComment.classList.add("comment_setting");
    newComment.innerHTML = `
      <div class="avt_user">
        <img src="{%static 'userprofiles/images/avatar.png' %}">
      </div>
      <div class="cmt"> 
        <h3 class="name_user">MinhTuan</h3>
        <p class="contentOfCmt">${commentText}</p>
      </div>
    `;
    commentContent.appendChild(newComment);
    document.getElementById("commentText").value = ""; 
    document.getElementById("commentBox").style.display = "none"; 
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