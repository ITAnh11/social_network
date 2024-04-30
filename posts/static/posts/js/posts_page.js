const parramQuery = window.location.search;
const urlParams = new URLSearchParams(parramQuery);
const IMAGE_ID = urlParams.get('image_id');
const POST_ID = urlParams.get('posts_id');
const USER_ID = localStorage.getItem("id");
const USER_NAME = localStorage.getItem("name");
const USER_AVATAR = localStorage.getItem("avatar");

let slideIndex = parseInt(IMAGE_ID);
// let slideIndex = 3;

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "flex";
}

showSlides(slideIndex);