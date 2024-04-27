const baseUrl = document.body.getAttribute('data-base-url');
function show_list_reaction(event){
    var a = event.target.parentNode.parentNode.parentNode.querySelector(".list_reaction");
    a.classList.toggle("show_list_reaction");
}


//lấy số reaction
url_get_reactions ="/reactions/get_reactions/";
function setCountReaction(forWhat, idWhat){
    formData = new FormData();
    what = (forWhat == 'posts') ? 'posts_id' : 'comment_id';
    otherWhat = (what == 'posts_id') ? 'comment_id' : 'posts_id';

    formData.append(what, idWhat);
    formData.append(otherWhat, -1);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(url_get_reactions, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("so luong react:",data);
        count = data.total;
        // document.getElementById(`count-reaction-${forWhat}-${idWhat}`).textContent = count;
    })
}

//sử lí kiểm tra xem đã react chưa
url_is_reacted = "/reactions/is_reacted/";
function is_reacted_for_post(post_id){

    formData = new FormData();
    formData.append('posts_id',post_id);
    formData.append('comment_id',-1);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(url_is_reacted,{
        method:"POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("myReaction:",data);
        if(data.is_reacted === true){
            a = document.getElementById(`reaction_img_${post_id}`);
            console.log(a);
            a.src = baseUrl + `images/${data.type}.png`;
        }
    })
}

url_creat_react = "/reactions/create_reaction/";
function create_reaction(event){
    var type = event.target.className;
    var b = event.target.parentNode.parentNode.parentNode.parentNode;
    console.log("nut",type);
    console.log("post",b.id);

    formData = new FormData();
    formData.append('user_id',localStorage.getItem('id'));
    formData.append('user_name',localStorage.getItem('name'));
    formData.append('user_avatar',localStorage.getItem('avatar'));
    formData.append('posts_id',b.id);
    formData.append('comment_id',-1);
    formData.append('type',type);
    formData.append('csrfmiddlewaretoken', csrftoken);
    
    fetch(url_creat_react,{
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("tao react:",data);
        a = document.getElementById(`reaction_img_${b.id}`);
        a.src = baseUrl + `images/${type}.png`;
    })
}

url_delete_react = "/reactions/delete_reaction/";
function delete_reaction(event){
    var b = event.target.parentNode.parentNode.parentNode.parentNode;
    console.log("post-id:",b.id);
    formData = new FormData();
    formData.append('posts_id',b.id);
    formData.append('comment_id',-1);
    formData.append('csrfmiddlewaretoken', csrftoken);
    
    fetch(url_delete_react,{
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("sau khi xoa react:",data);
        console.log("tao react:",data);
        a = document.getElementById(`reaction_img_${b.id}`);
    })
}
