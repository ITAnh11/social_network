var api_get_profile = '/userprofiles/get_profile/?id=' + (new URL(document.location)).searchParams.get('id').toString();
// console.log(api_get_profile);

fetch(api_get_profile)
    .then(response => response.json())
    .then(data => {
    //   console.log(data);
      set_user_data(data);

      var avatarImage = document.getElementById('avatarImage');
      avatarImage.innerHTML += `<img src="${data.imageprofile['avatar']}" alt="avatarImage" class="d-block ui-w-80">`;

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
      linkFb.value = '/http:/127.0.0.1:8000/userprofiles/?id=' + (new URL(document.location)).searchParams.get('id').toString();

      })
      function set_user_data(data){
          localStorage.setItem('name', data.userprofile['first_name'] + " " + data.userprofile['last_name']);
          localStorage.setItem('avatar', data.imageprofile['avatar']);
      }