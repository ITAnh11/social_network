function clearLocalStorage() {
    localStorage.clear();
}

clearLocalStorage();

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    // collect form data
    const formData = new FormData(event.target);

    // make a POST request to the server
    fetch(event.target.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data['success']) {
            alert(data['success']);
            window.location.href = data['redirect_url'];
        } else {
            alert(data['warning']);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});