document.getElementById('form-editProfile').addEventListener('submit', function(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  Promise.all([
     
  ]).then(() => {
    // make a Post request to the server
    fetch(event.target.action, {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data['success']) {
        console.log(data);
        alert(data['success']);
        localStorage.setItem('name', data['name'])
        window.location.href = data['redirect_url']
      } else {
        // handle error
        alert(data['warning']);
      }
    })
    .catch(error => console.error('Error:', error));
  });
});

var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();
// console.log(api_get_profile);

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
        // console.log(data);
      var avatarImage = document.getElementById('avatarImage');
      avatarImage.innerHTML += `<img src="${data.imageprofile['avatar']}" alt="avatarImage" class="d-block ui-w-80">`;

      var name_user = document.getElementById('name_user')
      name_user.innerHTML += `<h3 style="font-size: 20px; margin-left: 10px;">${data.userprofile['first_name'] + " " + data.userprofile['last_name']}</h3>`;

      var firstName = document.getElementById('firstName');
      firstName.value = `${data.userprofile['first_name']}`;

      var lastName = document.getElementById('lastName');
      lastName.value = `${data.userprofile['last_name']}`;

      var email = document.getElementById('email');
      email.value = `${data.user['email']}`;

      var phone = document.getElementById('phone');
      phone.value = `${data.userprofile['phone']}`;

      var birthdate = document.getElementById('birthdate');
      birthdate.value = `${data.userprofile['birth_date']}`;

      var linkFb = document.getElementById('linkFb');
      linkFb.value = '/http://127.0.0.1:8000/userprofiles/?id=' + (new URL(document.location)).searchParams.get('id').toString();

      });