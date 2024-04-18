/* user-settings */
var userSettings = document.querySelector(".user-settings");
var darkBtn = document.getElementById("dark-button");
var LoadMoreBackground =document.querySelector(".btn-LoadMore");
        function UserSettingToggle(){
            userSettings.classList.toggle("user-setting-showup-toggle");
        }

        function darkModeON(){
            darkBtn.classList.toggle("dark-mode-on");
        document.body.classList.toggle("dark-theme");
        };

        function LoadMoreToggle(){
            LoadMoreBackground.classList.toggle("loadMoreToggle");
        };

/* change-color */
const currentUrl = window.location.pathname;
// console.log(currentUrl);

if (currentUrl.includes("/")) {
    document.getElementById("home").classList.add("active");
} else if (currentUrl.includes("/friend")) {
    document.getElementById("friend").classList.add("active");
} else if (currentUrl.includes("/userprofiles")) {
    document.getElementById("home").classList.remove("active");
    document.getElementById("friend").classList.remove("active");
}

//Sử lý phần search
var search_list = document.querySelector(".search-list");
function remove_search_list(event){
    console.log("abc:",event.target.parentNode.parentNode);
    search_list.style.display = "none";
}
const searchInput = document.getElementById('search-input');
searchInput.addEventListener('keyup', function(event) {
  // Kiểm tra nếu phím nhấn là Enter (mã ASCII: 13)
  if (event.keyCode === 13) {
    console.log(searchInput.value);
    search_list.style.display = "flex";
  }
});

