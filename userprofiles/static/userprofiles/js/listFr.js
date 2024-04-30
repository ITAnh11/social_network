var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();

// Định nghĩa hàm lấy id_user từ URL
function getUserIdFromUrl() {
    // Lấy URL hiện tại
    var currentUrl = window.location.href;

    // Phân tích URL để lấy các thông tin
    var urlParams = new URLSearchParams(currentUrl);

    // Lấy giá trị của tham số "id"
    var id_user = urlParams.get('id');
    console.log(id_user);

    return id_user;
}

// Định nghĩa hàm showListFriends() và truyền id_user vào nó
function showListFriends(id_user) {
    // Thực hiện fetch để lấy dữ liệu userprofile từ api_get_profile
    fetch(api_get_profile)
        .then(response => response.json())
        .then(data => {
            // Lấy id_user từ dữ liệu userprofile nếu không được truyền vào từ bên ngoài
            if (!id_user) {
                id_user = data.userprofile['user_id'];
            }
            // var id_user = data.userprofile['user_id'];
            // Thực hiện fetch để lấy danh sách bạn bè của user có id_user
            fetch('/friends/get_listfriendofuserother/?id=' + id_user)
                .then(response => response.json())
                .then(data => {
                    console.log("user_id:",id_user);
                    console.log("friend_list:",data);
                    // var list_friend = document.createElement("div");
                    // list_friend.className = "card-list";
                    // var Friend_list = document.querySelector(".list-friends");
                    var Friend_list = document.getElementById('list_friends_userprofile')
                    console.log("abc",Friend_list);
                    // Friend_list.appendChild(list_friend);
                    data.data.forEach(function(friend_ship){
                        var url = `/userprofiles/?id=${friend_ship.friend_profile.id}`;
                        var a =`<a href="${url}" style="text-decoration: none;color:black;">
                                    <div class="someFriends">
                                        <div class="card friend" id="${friend_ship.friend_profile.id}">
                                            <div class="imgFriend">
                                                <img src="${friend_ship.friend_profile.avatar}" alt="User Avatar Image">
                                            </div>
                                            <div class="in4Friend">
                                                <p>${friend_ship.friend_profile.name}</p>
                                            </div>
                                        </div>
                                    </div>                            
                                </a>`;
                        
                        // var newCard = document.createElement("div");
                        // newCard.innerHTML = a;
                        // list_friend.appendChild(newCard);
                        Friend_list.innerHTML += a;
                    })  
                });
        });
}

// Xử lý khi trang đã load
document.addEventListener("DOMContentLoaded", function() {
    var id_user = getUserIdFromUrl();

    showListFriends(id_user);
});

