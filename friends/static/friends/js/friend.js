var request_list = document.querySelector(".request-list");
// var friend_list = document.querySelector(".card-list");
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
function addfriend() {
    fetch(url_addfriend)
    .then(response => response.json())
    .then(data => {
        console.log("friend_request: ", data);
        data.data.forEach(function(request){
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

addfriend();

//hiện danh sách bạn bè
url_list_friend = "/friends/get_listfriend/";
function show_list_friend(){
    fetch(url_list_friend)
    .then(response => response.json())
    .then(data => {
        console.log("friend_list:",data);
        var list = document.createElement("div");
        list.className = "card-list";
        var Friend_list = document.querySelector(".Friends_List");
        Friend_list.appendChild(list);
        var p = document.createElement("div");
        p.innerHTML =`<div style="font-size: large; color: rgb(0, 110, 255); margin: 10px;text-decoration: underline;"> Tất cả bạn bè </div>`;
        list.appendChild(p);
        data.data.forEach(function(friend){
            var url = `/userprofiles/?id=${friend.friend_profile.id}`;
            var a = `
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
            newCard.innerHTML = a;
            list.appendChild(newCard);
        })
    })
}
show_list_friend();

//hiện danh sách gợi ý
url_list_suggest_friend = "/friends/get_suggestionfriend/";
function show_suggest_friend(){
    fetch(url_list_suggest_friend)
    .then(response => response.json())
    .then(data => {
        console.log("suggest_friend_list:",data);
        data.suggestions.forEach(function(suggestions){
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
                    <button class="button2">Xóa</button>
                </div>
            </div>`
            var newDiv = document.createElement("div");
            newDiv.innerHTML = a;
    
            suggest_list.appendChild(newDiv);
        })
    })
    
}
show_suggest_friend();


//danh sach gửi lời mời chờ chấp nhận
url_get_sentfriendrequest = "/friends/get_sentfriendrequest/";
function show_get_sentfriendrequest(){
    fetch(url_get_sentfriendrequest)
    .then(response => response.json())
    .then(data => {
        console.log("abc:",data);
        var list = document.createElement("div");
        list.className = "card-list";
        var Friend_list = document.querySelector(".Friends_List");
        Friend_list.appendChild(list);
        var p = document.createElement("div");
        p.innerHTML =`<div style="font-size: large; color: rgb(0, 110, 255); margin: 10px;text-decoration: underline;"> Người bạn đã gửi lời mời </div>`;
        list.appendChild(p);
        data.data.forEach(function(friend){
            if(friend.friend_request_sent.status ="pending"){
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
                list.appendChild(newCard);
            }
        })
    })
}
//show_get_sentfriendrequest();