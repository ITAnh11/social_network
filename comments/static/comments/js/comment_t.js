const main_container = document.getElementById('main-container');


//lấy bài đăng
const api_get_posts_for_userprofilepage = '/userprofiles/get_posts/';
const api_get_comments_for_posts = '/comments/get_comments_for_post/';
const api_get_comments_for_comment = '/comments/get_comments_for_comment/';

const posts_lists = [];

function get_posts(){
    fetch(api_get_posts_for_userprofilepage)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        render_post(data,"old");
    })
}

function render_post(data,old) {
    data.posts.forEach(post => {

        posts_lists.push(post);

        var posts_id = post.id;
        var content = post.content;
        var created_at = post.created_at;
        var user_id = post.user.id;
        var user_name = post.user.name;
        var images = (post.media) ? post.media[0].media : "";
        var post = `<div class="posts-container" id="posts-${posts_id}" style="border: solid rgb(163, 162, 162); margin: 5px;">
                        <div class="post-box">
                            <div class="post" style="display: flex;">
                                <div class="post-header" style="margin: 5px 5px;">
                                    <div class="post-author">
                                        <p class="name" >${user_name} : </p>
                                    </div>
                                </div>
                                <div class="post-content" style="margin: 5px 5px;">
                                    <p class="content">${content}</p>
                                    <img src="${images}" alt="" style="width: 100px; height: 100px;">
                                </div>
                            </div>
                        </div>

                    <div class="comment-container">

                        <div id="active-comment">
                            <button id="active-comment-of-posts-btn-${posts_id}" class="${posts_id}" onclick="show_commented_of_posts(event)">show commented</button>
                        </div>
            
                        <div id="commented-of-posts-box-${posts_id}" style="display: none;"></div>
                        
                        <div id="comment-for-posts-container" style="margin-top: 10px;">
                            <form action="/comments/create_comment/" method="post" id="send-comment-for-posts-${posts_id}"">
                                <input type="text" name="content" id="content-comment-send">
                                <input type="submit" id="submit" value="comment">
                            </form>
                        </div>
                    </div>
        `;

        main_container.innerHTML += post;
    });

    posts_lists.forEach(post => {
        var posts_id = post.id;
        var form = document.getElementById(`send-comment-for-posts-${posts_id}`);
        form.addEventListener('submit', function(event){
            event.preventDefault();
            console.log("submit");
            send_comment(event, posts_id, -1, "posts");
        });
    });
    
}

function send_comment(event, posts_id, comment_id, forwhat){
    console.log("send_comment_for" + forwhat);

    const content = event.target.content.value;
    event.target.content.value = "";
    console.log(content);

    formData = new FormData();
    formData.append('content', content);
    formData.append('to_posts_id', posts_id);
    formData.append('to_comment_id', comment_id);

    idWhat = (forwhat === "posts") ? posts_id : comment_id;

    fetch('/comments/create_comment/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        render_comment(data, `commented-of-${forwhat}-box-${idWhat}`);
    })
}

function get_comments_for_post(posts_id, idElement){
    console.log("get_comments_for_post");

    formData = new FormData();
    formData.append('posts_id', posts_id);

    fetch(api_get_comments_for_posts, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        render_comment(data, idElement);
    })

}

function show_commented_of_posts(event){

    const posts_id = parseInt(event.target.classList[0]);
    console.log(posts_id);
    // console.log("clicked");
    posts_id_element = `commented-of-posts-box-${posts_id}`;

    var commented_box = document.getElementById(posts_id_element);
    // console.log(commented_box);

    // var active_comment = document.getElementById(`active-comment`);
    var active_comment_btn = document.getElementById(`active-comment-of-posts-btn-${posts_id}`);
    console.log(active_comment_btn);

    if (commented_box.innerHTML !== ""){
    } else {
        get_comments_for_post(posts_id, posts_id_element);
    }
    // get_comments_for_post(posts_id);

    if(commented_box.style.display === "none"){
        commented_box.style.display = "block";
        active_comment_btn.textContent = "hide commented";
    }
    else{
        commented_box.style.display = "none";
        active_comment_btn.textContent = "show commented";
    }
}

function get_comments_for_comment(comment_id, idElement){
    console.log("get_comments_for_comment");

    formData = new FormData();
    formData.append('comment_id', comment_id);

    fetch(api_get_comments_for_comment, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        render_comment(data, idElement);
    })
}

function show_commented_of_comment(event){

    const comment_id = parseInt(event.target.classList[0]);
    console.log(comment_id);
    // console.log("clicked");
    comment_id_element = `commented-of-comment-box-${comment_id}`;

    var commented_box = document.getElementById(comment_id_element);
    // console.log(commented_box);

    // var active_comment = document.getElementById(`active-comment`);
    var active_comment_btn = document.getElementById(`active-comment-of-comment-btn-${comment_id}`);
    console.log(active_comment_btn);

    if (commented_box.innerHTML !== ""){
    } else {
        get_comments_for_comment(comment_id, comment_id_element);
    }
    // get_comments_for_post(posts_id);

    if(commented_box.style.display === "none"){
        commented_box.style.display = "block";
        active_comment_btn.textContent = "hide reply";
    }
    else{
        commented_box.style.display = "none";
        active_comment_btn.textContent = "show reply";
    }
}

function render_comment(data, idElement){ {
    data.comments.forEach(comment => {
        var comment_id = comment.id;
        var content = comment.content;
        var created_at = comment.created_at;
        var user_id = comment.user_id;

        var comment = `<div id="comment-${comment_id}" class="comment" style="display: flex; flex-direction: column; margin-left: 20px;">
                            <div class="comment-header">
                                <div class="comment-author" style="margin: 0px 0px;">
                                    <p class="name" style="margin: 0px 0px;" >${user_id} : </p>
                                </div>
                            </div>
                            <div class="comment-content" style="margin: 0px 0px; margin-left: 20px;">
                                <p class="content" style="margin: 0px 0px;">${content}</p>
                            </div>

                            <div id="active-comment">
                                <button id="active-comment-of-comment-btn-${comment_id}" class="${comment_id}" onclick="show_commented_of_comment(event)">show reply</button>
                            </div>
                            
                            <div id="commented-of-comment-box-${comment_id}" style="display: none;"></div>
                            <div class="form-reply-comment" style="margin-left: 20px;">
                                <form action="/comments/create_comment/" method="post" id="send-comment-for-comment-${comment_id}" >
                                    <input type="text" name="content" id="content-comment-send">
                                    <input type="submit" id="submit" value="reply">
                                </form>
                            </div>
                        </div>`;

        var commented_box = document.getElementById(idElement);
        commented_box.innerHTML += comment;
    });

    data.comments.forEach(comment => {
        var comment_id = comment.id;
        var form = document.getElementById(`send-comment-for-comment-${comment_id}`);
        form.addEventListener('submit', function(event){
            event.preventDefault();
            console.log("submit");
            send_comment(event, -1, comment_id, "comment");
        });
    });
    }
}

get_posts();