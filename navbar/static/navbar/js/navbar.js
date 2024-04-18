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
