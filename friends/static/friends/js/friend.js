//loại bỏ lời mời kết bạn và  lời gợi ý kết bạn
var button2 = document.querySelectorAll('.button2');
button2.forEach(function(button){
    button.onclick = function(){
        button.parentElement.parentElement.remove();
    }
})

//xử lí button1
function button1_click(event){
    if(event.target.textContent === "Xác nhận") {
        event.target.textContent = "Đã xác nhận";
        event.target.style.backgroundColor = '#B8BABE';
    }
    if(event.target.textContent === "Thêm bạn bè") {
        event.taget.textContent = "Đã gửi yêu cầu";
    }
    else if(event.target.textContent === "Đã gửi yêu cầu") {
        event.target.textContent = "Thêm bạn bè";
    }
}

//xử lí lời mời kết bạn
var request_list = document.querySelector(".request-list");
url_addfriend = "/friends/get_receivedfriendrequest/";
function addfriend() {
    fetch(url_addfriend)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.data.forEach(function(request){
            var a = `<div class="card1">
            <div class="card1-img">
                <img style="object-fit: cover;width: 100%;height: 100%;" src="${request.friend_request_profile.avatar}" alt="Card Image" >
            </div>
            <div class="card1-content">
                <h3>${request.friend_request_profile.name}</h3>
            </div>
            <div class="card1-button">
                <button class="button1" onclick="button1_click(event)">Xác nhận</button>
                <button class="button2">Xóa</button>
            </div>
        </div>`;
        var newDiv = document.createElement("div");
        newDiv.innerHTML = a;

        request_list.appendChild(newDiv);
        })
    })
}

addfriend();



