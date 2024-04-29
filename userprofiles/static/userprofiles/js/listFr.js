// function friend_list(event){
//     event.target.parentNode.classList.toggle("list_setting_btn_toggle");
//     var a = document.querySelector(".card-list");
//     a.remove();
//     show_list_friend();
// }
// var id_user = data.userprofile['user_id'];
// function getListFriends(id_user) {
//     fetch('/friends/get_listfriendofuserother/?id=' + id_user)
//     .then(response => {
//         if (response.ok) {
//             return response.json();
//         } else {
//             throw new Error('Failed to fetch friend list');
//         }
//     })
//     .then(data => {
//         console.log(data);
//         const listFriendsDiv = document.querySelector('.list-friends');

//         data.data.forEach(friend => {
//             var url = `/userprofiles/?id=${friend.friend_profile.id}`;
//             var b = ` 
//                 <a href="${url}" style="text-decoration: none;color:black;">
//                     <div class="card" id="${friend.friend_profile.id}">
//                         <div class="card-img">
//                             <img style="display: flex; width: 100%; height: 100%;" src="${friend.friend_profile.avatar}" alt="Card Image">
//                         </div>
//                         <div class="card-content">
//                             <h3>${friend.friend_profile.name}</h3>
//                         </div>
//                     </div>
//                 </a>`;
//                 var newCard = document.createElement("div");
//                 newCard.innerHTML = b;
//                 listFriendsDiv.appendChild(newCard);
//         });
//     })
//     .catch(error => {
//         console.error('Error:', error);

//     });
// }

// getListFriends(id_user);
var id_user = data.userprofile['user_id'];

function show_list_friend(){
    fetch('/friends/get_listfriendofuserother/?id=' + id_user)
    .then(response => response.json())
    .then(data => {
        console.log("friend_ship:",data);
        var list_friend = document.createElement("div");
        list_friend.className = "card-list";
        var Friend_list = document.querySelector(".list-friends");
        console.log("abc",Friend_list);
        Friend_list.appendChild(list_friend);
        data.data.forEach(function(friend){
            var url = `/userprofiles/?id=${friend.friend_profile.id}`;
            var a =`
            <a href="${url}" style="text-decoration: none;color:black;">
                <div class="card" id="${friend.friend_profile.id}">
                    <div class="card-img">
                        <img style="display: flex; width: 20px; height: 20px;" src="${friend.friend_profile.avatar}" alt="Card Image">
                    </div>
                    <div class="card-content">
                        <h3>${friend.friend_profile.name}</h3>
                    </div>
                </div>
            </a>`;
            
            var newCard = document.createElement("div");
            newCard.innerHTML = a;
            list_friend.appendChild(newCard);
        })
    })
}
show_list_friend();