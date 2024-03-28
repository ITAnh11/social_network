//loại bỏ lời mời kết bạn và  lời gợi ý kết bạn
var button2 = document.querySelectorAll('.button2');
button2.forEach(function(button){
    button.onclick = function(){
        button.parentElement.parentElement.remove();
    }
})

//xử lý nút xác nhận và nút thêm bạn bè
var button1 = document.querySelectorAll('.button1');
button1.forEach(function(button){
    button.addEventListener('click', function() {
        if(button.textContent === "Xác nhận") {
            button.textContent = "Đã xác nhận";
            button.style.backgroundColor = '#B8BABE';
        }
        if(button.textContent === "Thêm bạn bè") {
            button.textContent = "Đã gửi yêu cầu";
        }
        else if(button.textContent === "Đã gửi yêu cầu") {
            button.textContent = "Thêm bạn bè";
        }
    });
})



