//lấy bài đăng
const params = (new URL(document.location)).searchParams;
const url_user_post = '/userprofiles/get_posts/?id=' + ((params.get('id') !== null) ? params.get('id') : '');
const url_homepage_post = '/homepage/get_posts/';

const url_get_posts = (window.location.pathname == '/userprofiles/') ? url_user_post : url_homepage_post;

const posted_area = document.querySelector(".posted_area");

const baseUrl = document.body.getAttribute('data-base-url');

import { createLayoutImages } from './gallery.js';

function get_posts(){
    fetch(url_get_posts)
    .then(response => response.json())
    .then(data => {
        render_post(data,"old");
        // console.log(data);
    })
}

//render_post
export function render_post(data,isOld){
    data.posts.forEach(function(post, index){

        setTimeout(function() {
            var newDiv = 
                `<div class="status-field-container write-post-container">
                <div class="user-profile-box">
                    <div class="user-profile">
                        <img src="${post.user.avatar}" alt="">
                        <div>
                            <a href="/userprofiles/?id=${post.user.id}" style="text-decoration: none;">
                                <p>${post.user.name}</p>
                            </a>
                            <small>${post.created_at}</small>
                        </div>
                    </div>
                    <div>
                        <a href="#"><i class="fas fa-ellipsis-v"></i></a>
                    </div>
                </div>
                <div class="status-field">
                    <p>${(post.content !== undefined && post.content !== null && post.content !== "") ? post.content : ""}</p>
                    <div class="gallery-container">
                    </div>
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

            var galleryContainerElement = posted.querySelector('.gallery-container');
            createLayoutImages(post.media, galleryContainerElement);

        }, 500 * index);

    })

}

get_posts();