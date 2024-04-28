//lấy bài đăng
const params = (new URL(document.location)).searchParams;
const url_user_post = '/userprofiles/get_posts/?id=' + ((params.get('id') !== null) ? params.get('id') : '');
const url_homepage_post = '/homepage/get_posts/';
const url_mark_as_watched = '/posts/mark_as_watched/';

const is_in_homepage = (window.location.pathname == '/') ? true : false;
const url_get_posts = (is_in_homepage == false) ? url_user_post : url_homepage_post;

const posted_area = document.querySelector(".posted_area");

const baseUrl = document.body.getAttribute('data-base-url');

let currentNumberOfPosts = 0;

function get_posts() {
    loadMorePosts()
}

//render_post
function render_post(data, isOld) {
    currentNumberOfPosts += data.posts.length;
    // console.log(data.posts)
    document.body.style.overflow = 'hidden';
    

    data.posts.forEach(function (post, index) {
        setTimeout(function () {
            var newDiv =
                `<div class="status-field-container write-post-container" id="posts-${post.id}" posts_id="${post.id}">
                <div class="user-profile-box">
                    <div class="user-profile">
                        <a href="/userprofiles/?id=${post.user.id}" style="text-decoration: none;">
                            <img src="${post.user.avatar}" alt="">
                        </a>
                        <div>
                            <div style="display: flex; align-items: center;">
                            <div id="name-user-of-post">
                                <a href="/userprofiles/?id=${post.user.id}" style="text-decoration: none;">
                                <p>${post.user.name}</p>
                                </a>
                            </div>
                            <div
                                id="title-of-posts"
                                class="title-posts"
                                style="padding-top: 4px;"
                            >
                                <small style="font-size: 13px; margin-left: 5px">
                                ${((post.title) ? post.title : "")}
                                </small>
                            </div>
                            </div>
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
                
                <div class="count-reactionPost" id="count-reaction-${post.id}">
                    <div>
                        <p id="count-reaction-posts-${post.id}">120</p>
                    </div>
                </div>

                <div class="post-reaction">
                    <div class="activity-icons">
                        <div onmouseover="show_list_reaction_for_post(event)" onclick="delete_reaction_for_post(event)">
                            <img src="${baseUrl + "images/like3.png"}" id="reaction_img_${post.id}" alt="" status="default"> 
                        </div>
                        <div onclick="clickCommentBtn(event)" posts_id="${post.id}"><img src="${baseUrl + "images/comment.png"}" alt="">Comments</div>
                        <div><img src="${baseUrl + "images/share0.png"}" alt="">Share</div>
                    </div>

                    <div class="post-profile-picture">
                        <img src="${post.user.avatar}" alt=""> <i class=" fas fa-caret-down"></i>
                    </div>

                    <div class="list_reactionPost">
                        <div class="reaction_btnPost" onclick="create_reaction_for_post(event)">
                            <img class="love" src="${baseUrl + "images/love.png"}">
                        </div>
                        <div class="reaction_btnPost" onclick="create_reaction_for_post(event)">
                            <img class="like" src="${baseUrl + "images/like.png"}">
                        </div>
                        <div class="reaction_btnPost" onclick="create_reaction_for_post(event)">
                            <img class="care" src="${baseUrl + "images/care.png"}">
                        </div>
                        <div class="reaction_btnPost" onclick="create_reaction_for_post(event)">
                            <img class="haha" src="${baseUrl + "images/haha.png"}">
                        </div>
                        <div class="reaction_btnPost" onclick="create_reaction_for_post(event)">
                            <img class="wow" src="${baseUrl + "images/wow.png"}">
                        </div>
                        <div class="reaction_btnPost" onclick="create_reaction_for_post(event)">
                            <img class="sad" src="${baseUrl + "images/sad.png"}">
                        </div>
                        <div class="reaction_btnPost" onclick="create_reaction_for_post(event)">
                            <img class="angry" src="${baseUrl + "images/angry.png"}">
                        </div>
                    </div>

                </div>
            </div>`
            var posted = document.createElement("div");
            posted.innerHTML = newDiv;

            if (isOld === "old") {
                posted_area.appendChild(posted);
            }
            else {
                var a = posted_area.children[0];
                posted_area.insertBefore(posted, a);
            }

            setCountReaction_for_post("posts", post.id);
            is_reacted_for_post(post.id);

            var galleryContainerElement = posted.querySelector('.gallery-container');
            createLayoutImages(post.media, galleryContainerElement, post.id);

            // After the last post is rendered, re-enable scrolling
            if (index === Math.floor(data.posts.length / 3)) {
                document.body.style.overflow = '';
            }
        }, 500 * index);

    })
}



let isLoading = false; // Biến trạng thái để kiểm soát việc đang tải dữ liệu hay không

window.addEventListener('scroll', () => {

    if (is_in_homepage) {
        checkPostInView();
    }

    // Nếu đang trong quá trình tải dữ liệu, không thực hiện gì cả
    if (isLoading) return;

    const windowHeight = window.innerHeight;
    const documentHeight = document.body.offsetHeight;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;

    if (scrollTop > (11 / 13) * (documentHeight - windowHeight)) {
        // Đặt isLoading thành true để chỉ ra rằng đang trong quá trình tải dữ liệu
        isLoading = true;
        loadMorePosts().then(() => {
            // Sau khi dữ liệu được tải thành công, đặt isLoading thành false để cho phép tải thêm lần tiếp theo
            isLoading = false;
        }).catch(error => {
            // Xử lý lỗi nếu có
            console.error('Error loading more posts:', error);
            // Đặt isLoading thành false để cho phép tải thêm lần tiếp theo dù có lỗi xảy ra
            isLoading = false;
        });
    }
});

function loadMorePosts() {
    // Trả về một Promise để thực hiện việc gọi API hoặc tải dữ liệu
    // Ví dụ:
    return new Promise((resolve, reject) => {
        // Gọi API hoặc thực hiện tải dữ liệu ở đây
        // Sau khi dữ liệu được tải thành công, gọi hàm resolve
        // Nếu có lỗi, gọi hàm reject với lỗi tương ứng
        setTimeout(() => {
            // Ví dụ: giả định dữ liệu đã được tải thành công sau 1 giây
            console.log('Loaded more posts');
            console.log(currentNumberOfPosts)
            var formData = new FormData()
            formData.append('current_number_of_posts', currentNumberOfPosts)

            fetch(url_get_posts, {
                'method': 'POST',
                'body': formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data['error'] != null) {
                        return;
                    }
                    render_post(data, "old");
                })
            resolve(); // hoặc reject(error) nếu có lỗi xảy ra
        }, 1000);
    });
}

function clickCommentBtn(event) {
    event.stopPropagation();

    posts_id = event.target.getAttribute('posts_id');
    image_id = 1

    url = '/posts/page/?posts_id=' + posts_id + '&image_id=' + image_id;

    window.open(window.location.origin + url, '_blank');
}

let viewedPosts = [];

function checkPostInView() {
    // Lặp qua mỗi bài đăng
    document.querySelectorAll('.status-field-container').forEach(post => {
        if (post.getAttribute('is_watched') === 'true') {
            return;
        }
        // Kiểm tra xem bài đăng có nằm trong phạm vi hiển thị không
        const rect = post.getBoundingClientRect();
        if (
            rect.top >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight)
        ) {
            // Bài đăng hiện được hiển thị trên màn hình, đánh dấu nó là đã xem
            const postId = post.getAttribute('posts_id');
            viewedPosts.push(postId);
            markPostsAsViewed([postId]);
            post.setAttribute('is_watched', 'true');
        }
    });
}

// Gửi danh sách các bài đăng đã xem đến server khi người dùng thoát khỏi trang
window.addEventListener('beforeunload', function (event) {
    if (viewedPosts.length > 0) {
        markPostsAsViewed(viewedPosts);
    }
});

function markPostsAsViewed(postIds) {
    // Gửi yêu cầu AJAX đến máy chủ để đánh dấu bài đăng đã xem

    formData = new FormData();
    postIds.forEach(postId => {
        formData.append('post_ids[]', postId);
    });

    fetch(url_mark_as_watched, {
        'method': 'POST',
        'body': formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
}

get_posts();