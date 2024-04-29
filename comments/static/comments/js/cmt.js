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

// Big Comment js

document.getElementById('commentBox').addEventListener('click', function(event) {
  event.preventDefault(); // prevent form submission
  // console.log(event.target.getAttribute('posts_id'));
  // collect form data
  const formData = new FormData();
  
  const content = document.getElementById('commentText').value;
  // console.log(content);
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
              // console.log(data);
              alert(data['success']);
          } else {
              // handle error
              alert(data['warning']);
          }
      })
      .catch(error => console.error('Error:', error));
  });
});

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
  var comments = getCommentsFromLocalStorage();
  comments.push(newComment);

  saveCommentsToLocalStorage(comments);

  render_comment({ comments: [newComment] });
}

function render_comment(data){ {
  data.comments.forEach(comment => {
      var comment_id = comment.id;
      var content = comment.content;
      var created_at = comment.created_at;
      var user = comment.user;

      var comment = `<div id="comment-${comment_id}" class="comment_setting" cmt_id="${comment_id}">
                        <div class="avt_user">
                            <img src="${user.avatar}" alt="">
                        </div>
                        <div class="cmt">
                            <h3 class="name_user">${user.name}</h3>
                            <p class="contentOfCmt">${content}</p>
                        </div>
                      </div>
                      <div class="reactOfUser">
                        <div class="time">
                          6 minutes ago 
                        </div>
                        <div class="reply" id="replyButton">
                          <button class="replyButton" onClick="toggleReplyBox()">
                            <p>Reply</p>
                          </button>
                          <button class="replyButton">
                            <p>React</p>
                          </button>
                        </div>
                      </div>
                      <div id="replyBox" class="replyBoxHidden">
                        <textarea
                          id="replyText"
                          class="replyText"
                          placeholder="Write your reply here..."
                        ></textarea>
                        <button comment_id="${comment_id}" onclick="postReply(event)" type="submit" class="sendReplyButton">Reply</button>
                      </div>
                      <div id="replyContent" class="replyContent">

                      </div>`;
      var commentContent = document.getElementById('commentContent');
      commentContent.innerHTML += comment;
  });
  
  }
}

function saveCommentsToLocalStorage(comments) {
  localStorage.setItem('comments', JSON.stringify(comments));
}

function getCommentsFromLocalStorage() {
  var comments = localStorage.getItem('comments');
  return comments ? JSON.parse(comments) : [];
}

// When the page loads, render comments from local storage
window.onload = function() {
  var comments = getCommentsFromLocalStorage();
  render_comment({ comments: comments });

  var list_comments = getRepliesFromLocalStorage();
  render_reply({ list_comments : list_comments });
};


//Reply box js

function toggleReplyBox() {
  var replyBox = document.getElementById('replyBox');
  replyBox.classList.toggle("replyBoxHidden");
}

document.getElementById('replyBox').addEventListener('submit', function(event) {
  event.preventDefault(); 
  const formData = new FormData();
  
  const content = document.getElementById('replyText').value;
  console.log(content);
  formData.append('content', content);
  formData.append('comment_id', comment_id);

  Promise.all([
      
  ]).then(() => {
      
    fetch('/comments/get_comments_for_comment/', {
          method: 'POST',
          body: formData,
      })
      .then(response => response.json())
      .then(data => {
          if (data['success']) {
              // console.log(data);
              alert(data['success']);
          } else {
              // handle error
              alert(data['warning']);
          }
      })
      .catch(error => console.error('Error:', error));
  });
});

function postReply() {
  var replyText = document.getElementById('replyText').value;
  var newReply = {
    id: localStorage.getItem('id'),
    content: replyText,
    created_at: new Date(),
    user: {
      name: localStorage.getItem('name'), 
      avatar: localStorage.getItem('avatar'),
    }
  };
  var list_comments = getRepliesFromLocalStorage();
  list_comments.push(newReply);

  saveRepliesToLocalStorage(list_comments);

  render_reply({ list_comments: [newReply] });
}

function render_reply(data){ {

  data.list_comments.forEach(dataComment => {
      var dataComment_id = dataComment.id;
      var content = dataComment.content;
      var created_at = dataComment.created_at;
      var user = dataComment.user;

      var dataComment =   `<div id="reply-${dataComment_id}" class="reply_setting" style="margin-left: 20px;">
                            <div class="avt_user">
                                <img src="${user.avatar}" alt="">
                            </div>
                            <div class="cmt">
                                <h3 class="name_user">${user.name}</h3>
                                <p class="contentOfCmt">${content}</p>
                            </div>
                          </div>
                          <div class="reactOfUser">
                            <div class="time">
                              6 minutes ago 
                            </div>
                            <div class="reply" id="replyButton">
                              <button class="replyButton" onClick="toggleReplyBox()">
                                <p>Reply</p>
                              </button>
                            </div>
                          </div>
                          <div id="replyBox" class="replyBoxHidden">
                            <textarea
                              id="replyText"
                              class="replyText"
                              placeholder="Write your reply here..."
                            ></textarea>
                            <button onclick="postReply(event)" type="click" class="sendReplyButton">Reply</button>
                          </div>
                          <div class="replyContent">

                          </div>`;
      var replyContent = document.getElementById('replyContent');
      replyContent.innerHTML += dataComment;
  });
  
  }
}

function saveRepliesToLocalStorage(list_comments) {
  localStorage.setItem('list_comments', JSON.stringify(list_comments));
}

function getRepliesFromLocalStorage() {
  var list_comments = localStorage.getItem('list_comments');
  return list_comments ? JSON.parse(list_comments) : [];
}
