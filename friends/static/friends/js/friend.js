var request_list = document.querySelector(".request-list");
var friend_list = document.querySelector(".card-list");
var suggest_list = document.querySelector(".suggest_list");

//Xử lí denine button
function denine_button(event){
    var a = event.target.parentNode.parentNode.id;

    const formdata = new FormData();
    formdata.append("st", "denined");
    formdata.append("id", a);
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
                <a href="${url}" style="text-decoration: none;">
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
        url_sent_friendrequest = "/friends/sent_friendrequest/";
        fetch(url_sent_friendrequest,{
            method:'POST',
            body: formdata,
        })
    }
    else{
        event.target.textContent = "Thêm bạn bè";
        var formdata = new FormData();
        formdata.append("st","revoke");
        formdata.append("id",a);
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

//hiện lời mời kết bạn
url_addfriend = "/friends/get_receivedfriendrequest/";
function addfriend() {
    fetch(url_addfriend)
    .then(response => response.json())
    .then(data => {
        console.log("friend_request: ", data);
        data.data.forEach(function(request){
            if(request.friend_request_received.status === "pending"){
                var a = `<div class="card1" id="${request.friend_request_received.id}">
                <div class="card1-img">
                    <img style="object-fit: cover;width: 100%;height: 100%;" src="${request.friend_request_profile.avatar}" alt="Card Image" >
                </div>
                <div class="card1-content">
                    <h3>${request.friend_request_profile.name}</h3>
                </div>
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
            friend_list.appendChild(newCard);
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
        data.suggestions.forEach(function(suggest_friend){
            console.log(suggest_friend.other_user_profile.id);
            var a = `
            <div class="card1" id="${suggest_friend.other_user_profile.id}">
                <div class="card1-img">
                    <img style="object-fit: cover;width: 100%;height: 100%;" src="${suggest_friend.other_user_profile.avatar}" alt="Card Image" >
                </div>
                <div class="card1-content">
                    <h3>${suggest_friend.other_user_profile.name}</h3>
                </div>
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