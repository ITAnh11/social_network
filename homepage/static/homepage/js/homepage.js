var list_all_user = document.querySelector(".right-sidebar");

url_all_users = "search/@"; // Assuming this is the correct endpoint to fetch all users

function show_all_users() {
    fetch(url_all_users)
    .then(response => response.json())
    .then(data => {
        // console.log("all_users:", data);
        data.list_users.forEach(function(user) {
            var url = ""; // You might want to define a URL to link to each user's profile
            var fullName = user.first_name + " " + user.last_name;

            var avatarUrl = ""; // Provide the URL for the user's avatar image
            
            var a = `<div class="online-list" id="${user.id}">
                        <div class="online">
                            <img src="${avatarUrl}" alt="${fullName}">
                        </div>
                        <p>${fullName}</p>
                    </div>`;
            var newCard = document.createElement("div");
            newCard.innerHTML = a;

            list_all_user.appendChild(newCard);
            // console.log(newCard)
        });
    })
    .catch(error => {
        console.error('Error fetching users:', error);
        // Handle errors, such as displaying an error message to the user
    });
}

show_all_users();
