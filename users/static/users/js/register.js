document.getElementById('form-register').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    // collect form data
    const formData = new FormData(event.target);

    const day = formData.get('day');
    const month = formData.get('month');
    const year = formData.get('year');
    const birth_date = `${year}-${month}-${day}`;

    formData.append('birth_date', birth_date);

    Promise.all([
        
    ]).then(() => {
        // make a POST request to the server
        fetch(event.target.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data['success']) {
                console.log(data);
                alert(data['success']);
                window.location.href = data['redirect_url'];
            } else {
                // handle error
                alert(data['warning']);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
