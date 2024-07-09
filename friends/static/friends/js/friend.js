// const moreButton = document.getElementById('moreButton');
// moreButton.textContent = "More";
// moreButton.href = "#";
// const moreSuggestBtn = document.getElementById('moreSuggestButton');
// moreSuggestBtn.textContent = "More Suggest";
// moreSuggestBtn.href = "#";
// const moreAddtBtn = document.getElementById('moreAddButton');
// moreAddtBtn.textContent = "More Friend Request";
// moreAddtBtn.href = "#";
// var list_friend = document.getElementById('list_friends');
// console.log("acb",list_friend.className);
var request_list = document.querySelector(".request-list");
var friend_list = document.querySelector(".card-list");
console.log(friend_list);
var suggest_list = document.querySelector(".suggest_list");
//Xử lí denine button
function denine_button(event){
    var a = event.target.parentNode.parentNode.id;

    const formdata = new FormData();
    formdata.append("st", "denined");
    formdata.append("id", a);
    formdata.append("csrfmiddlewaretoken", csrftoken);
    url = "/friends/denine_friendrequest/";
    fetch(url,{
        method:'POST',
        body: formdata,
    })
    if(event.target.textContent === "Từ chối") {
        event.target.textContent = "Đã từ chối";
    }
    event.target.parentNode.parentNode.querySelector(".button1").remove();

}

//xử lí accept button
function accept_button(event){
    if(event.target.textContent === "Xác nhận") {
        event.target.textContent = "Đã xác nhận";
        event.target.style.backgroundColor = '#B8BABE';
    }
    var a = event.target.parentNode.parentNode.id;

    var formdata = new FormData();

    formdata.append("st", "accepted");
    formdata.append("id", a);
    formdata.append("csrfmiddlewaretoken", csrftoken);

    url = "/friends/accept_friendrequest/"
    fetch(url,{
        method:'POST',
        body: formdata,
    })
    .then(response => response.json())
    .then(data => {
        console.log("acb:",data);
        data.accepted_friend_request.forEach(function(friend){
            var url = `/userprofiles/?id=${friend.friend_profile.id}`;
            var b = ` 
                <a href="${url}" style="text-decoration: none;color:black;">
                    <div class="card" id="${friend.friend_profile.id}">
                        <div class="card-img">
                            <img style="display: flex; width: 100%; height: 100%;" src="${friend.friend_profile.avatar}" alt="Card Image">
                        </div>
                        <div class="card-content">
                            <h3>${friend.friend_profile.name}</h3>
                        </div>
                    </div>
                </a>`;
                var newCard = document.createElement("div");
                newCard.innerHTML = b;
                friend_list.appendChild(newCard);
        })
    })
    event.target.parentNode.parentNode.querySelector(".button2").remove();
}

//xử lí friend request button
function request_button(event){
    var a = event.target.parentNode.parentNode.id;
    if(event.target.textContent === "Thêm bạn bè") {
        event.target.textContent = "Thu hồi";
        var formdata = new FormData();
        formdata.append("st", "pending");
        formdata.append("id", a);
        formdata.append("csrfmiddlewaretoken", csrftoken);

        url_sent_friendrequest = "/friends/sent_friendrequest/";
        fetch(url_sent_friendrequest,{
            method:'POST',
            body: formdata,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if(data.error){
                alert(data.error);
            } 
        })
    }
    else{
        event.target.textContent = "Thêm bạn bè";
        var formdata = new FormData();
        formdata.append("st","revoke");
        formdata.append("id",a);
        formdata.append("csrfmiddlewaretoken", csrftoken);

        url_revoke_friendrequest = "/friends/revoke_friendrequest/";
        fetch(url_revoke_friendrequest,{
            method:'POST',
            body: formdata,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
    }
}


//xử lí remove_btn_friendrequest
function remove_btn_friendrequest(event){
    event.target.parentNode.parentNode.remove();
}

//xử lí chọn danh sách button
const list_setting_btn = document.querySelector(".list_setting_btn");
const choose_list_btn = document.querySelector(".setting-btn");
choose_list_btn.addEventListener("click", function() {
    list_setting_btn.classList.toggle("list_setting_btn_toggle");
});

function friend_list(event){
    event.target.parentNode.classList.toggle("list_setting_btn_toggle");
    var a = document.querySelector(".card-list");
    a.remove();
    show_list_friend();
}

function sent_friend_request_list(event){
    event.target.parentNode.classList.toggle("list_setting_btn_toggle");
    var a = document.querySelector(".card-list");
    console.log(a);
    a.remove();
    show_get_sentfriendrequest();
}

//hiện lời mời kết bạn
url_addfriend = "/friends/get_receivedfriendrequest/";
var url_next_add = url_addfriend;
function addfriend() {
    if (url_next_add) {

    fetch(url_next_add)
    .then(response => response.json())
    .then(data => {
        if (data.next) {
            url_next_add = data.next;

        } else {
            // moreAddtBtn.style.display = 'none';
            url_next_add = null;
        }
        console.log("friend_request: ", data);
        data.results.data.forEach(function(request){
            if(request.friend_request_received.status === "pending"){
                var url = `/userprofiles/?id=${request.friend_request_profile.id}`;
                var a = `<div class="card1" id="${request.friend_request_received.id}">
                <div class="card1-img">
                    <img style="object-fit: cover;width: 100%;height: 100%;" src="${request.friend_request_profile.avatar}" alt="Card Image" >
                </div>
                <a href="${url}" style="text-decoration: none;color:black;flex:1">
                    <div class="card1-content">
                        <h3>${request.friend_request_profile.name}</h3>
                    </div>
                </a>
                <div class="card1-button">
                    <button class="button1" onclick="accept_button(event)">Xác nhận</button>
                    <button class="button2" onclick="denine_button(event)">Từ chối</button>
                </div>
            </div>`;
            var newDiv = document.createElement("div");
            newDiv.innerHTML = a;
    
            request_list.appendChild(newDiv);
            }
        })
    })
}
}
request_list.addEventListener('scroll', function(event) {
    // Kiểm tra nếu cuộn đã đạt đến cuối của div
    if (request_list.scrollTop + request_list.clientHeight >= request_list.scrollHeight) {
        event.preventDefault();
        addfriend();
    }
});
addfriend();

//hiện danh sách bạn bè
url_list_friend = "/friends/get_listfriend/";

var nextPageUrl = url_list_friend;

function show_list_friend(){
    if (nextPageUrl) {
    fetch(nextPageUrl)
    .then(response => response.json())
    .then(data => {
        if (data.next) {
            nextPageUrl = data.next;
        } else {
            // moreButton.style.display = 'none';
            nextPageUrl = null;
        }
        console.log("friend_list:",data);
        
        data.results.data.forEach(function(friend){
            var url = `/userprofiles/?id=${friend.friend_profile.id}`;
            var a = `
            <a href="${url}" style="text-decoration: none;color:black;">
                <div class="card0" id="${friend.friend_profile.id}">
                    <div class="card0-img">
                        <img style="display: flex; width: 100%; height: 100%;" src="${friend.friend_profile.avatar}" alt="Card Image">
                    </div>
                    <div class="card0-content">
                        <h3>${friend.friend_profile.name}</h3>
                    </div>
                </div>
            </a>`;
            var newCard = document.createElement("div");
            newCard.innerHTML = a;
            friend_list.appendChild(newCard);
        })
    })
}
}


friend_list.addEventListener('scroll', function(event) {
    // Kiểm tra nếu cuộn đã đạt đến cuối của div
    if (friend_list.scrollTop + friend_list.clientHeight >= friend_list.scrollHeight) {
        event.preventDefault();
        show_list_friend();
    }
});

show_list_friend();

//hiện danh sách gợi ý

url_list_suggest_friend = "/friends/get_suggestionfriend/";
var url_next_suggest = url_list_suggest_friend;

function show_suggest_friend(){
    if (url_next_suggest) {
        console.log("next link: ", url_next_suggest)
    fetch(url_next_suggest)
    .then(response => response.json())
    .then(data => {
        if (data.next) {
            url_next_suggest = data.next;
            console.log("new link: ", url_next_suggest);
        } else {
            // moreSuggestBtn.style.display = 'none';
            url_next_suggest = null;
        }
        console.log("suggest_friend_list:",data);
        data.results.suggestions.forEach(function(suggestions){
            console.log(suggestions.suggestions_friend.id);
            var url = `/userprofiles/?id=${suggestions.suggestions_friend.id}`;
            var a = `
            <div class="card1" id="${suggestions.suggestions_friend.id}">
                <div class="card1-img">
                    <img style="object-fit: cover;width: 100%;height: 100%;" src="${suggestions.suggestions_friend.avatar}" alt="Card Image" >
                </div>
                <a href="${url}" style="text-decoration: none;color:black;flex:1">
                    <div class="card1-content">
                        <h3>${suggestions.suggestions_friend.name}</h3>
                    </div>
                </a>
                <div class="card1-button">
                    <button class="button1" onclick="request_button(event)">Thêm bạn bè</button>
                    <button class="button2" onclick="remove_btn_friendrequest(event)">Xóa</button>
                </div>
            </div>`
            var newDiv = document.createElement("div");
            newDiv.innerHTML = a;
    
            suggest_list.appendChild(newDiv);
        })
    })
    }
}

suggest_list.addEventListener('scroll', function(event) {
    // Kiểm tra nếu cuộn đã đạt đến cuối của div
    if (suggest_list.scrollTop + suggest_list.clientHeight >= suggest_list.scrollHeight) {
        event.preventDefault();
        show_suggest_friend();
    }
});

show_suggest_friend();



//danh sach gửi lời mời chờ chấp nhận
url_get_sentfriendrequest = "/friends/get_sentfriendrequest/";
function show_get_sentfriendrequest(){
    fetch(url_get_sentfriendrequest)
    .then(response => response.json())
    .then(data => {
        console.log("abc:",data);
        var list_friend = document.createElement("div");
        list_friend.className = "card-list";
        var Friend_list = document.querySelector(".list");
        Friend_list.appendChild(list_friend);
        var p = document.createElement("div");
        p.innerHTML =`<div style="font-size: large; color: rgb(0, 110, 255); margin: 10px;text-decoration: underline;"> Người bạn đã gửi lời mời </div>`;
        list_friend.appendChild(p);
        data.data.forEach(function(friend){
            if(friend.friend_request_sent.status ==="pending"){
                var url = `/userprofiles/?id=${friend.friend_request_profile.id}`;
                var a = `
                <a href="${url}" style="text-decoration: none;color:black;">
                    <div class="card" id="${friend.friend_request_profile.id}">
                        <div class="card-img">
                            <img style="display: flex; width: 100%; height: 100%;" src="${friend.friend_request_profile.avatar}" alt="Card Image">
                        </div>
                        <div class="card-content">
                            <h3>${friend.friend_request_profile.name}</h3>
                        </div>
                    </div>
                </a>`;
                var newCard = document.createElement("div");
                newCard.innerHTML = a;
                list_friend.appendChild(newCard);
            }
        })
    })
}
