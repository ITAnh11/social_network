document.getElementById('form-editStory').addEventListener('submit', function(event) {
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
        window.location.href = data['redirect_url']
      } else {
        // handle error
        alert(data['warning']);
      }
    })
    .catch(error => console.error('Error:', error));
  });
});