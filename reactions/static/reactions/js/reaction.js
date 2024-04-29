function show_list_reaction_for_post(event){
    var a = event.target.parentNode.parentNode.parentNode.querySelector(".list_reactionPost");
    a.classList.toggle("show_list_reactionPost");
}


//lấy số reaction
url_get_reactions ="/reactions/get_reactions/";
function setCountReaction_for_post(forWhat, idWhat){
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
        document.getElementById(`count-reaction-${forWhat}-${idWhat}`).textContent = count;
        var iconTopReactionsContainer = document.getElementById(`icon-top-reactions-container-${idWhat}`);
        iconTopReactionsContainer.innerHTML = '';
        
        if(data.topMostReacted[0].total !== 0 && data.topMostReacted[1].total !== 0){

            var top2_react = document.createElement('img');
            top2_react.classList.add("top2-react-in-post");
            top2_react.src = `${baseUrl + `images/${data.topMostReacted[1].type}.png`}`;

            iconTopReactionsContainer.insertBefore(top2_react, iconTopReactionsContainer.firstChild);


            var top1_react = document.createElement('img');
            top1_react.classList.add("top1-react-in-post");
            top1_react.src = `${baseUrl + `images/${data.topMostReacted[0].type}.png`}`;
            
            iconTopReactionsContainer.insertBefore(top1_react, iconTopReactionsContainer.firstChild);
        }
        else if(data.topMostReacted[0].total !== 0){
            var top1_react = document.createElement('img');
            top1_react.classList.add("top1-react-in-post");
            top1_react.src = `${baseUrl + `images/${data.topMostReacted[0].type}.png`}`;

            iconTopReactionsContainer.insertBefore(top1_react, iconTopReactionsContainer.firstChild);
        }
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
        // console.log("myReaction:",data);
        if(data.is_reacted === true){
            a = document.getElementById(`reaction_img_${post_id}`);
            a.src = baseUrl + `images/${data.type}.png`;
            a.setAttribute("status",data.type);
        }
    })
}

url_creat_react = "/reactions/create_reaction/";
function create_reaction_for_post(event){
    var type = event.target.className;
    var b = event.target.parentNode.parentNode.parentNode.parentNode;

    formData = new FormData();
    formData.append('user_id',localStorage.getItem('id'));
    formData.append('user_name',localStorage.getItem('name'));
    formData.append('user_avatar',localStorage.getItem('avatar'));
    formData.append('posts_id',b.getAttribute('posts_id'));
    formData.append('comment_id',-1);
    formData.append('type',type);
    formData.append('csrfmiddlewaretoken', csrftoken);
    
    fetch(url_creat_react,{
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("da react:",data);
        a = document.getElementById(`reaction_img_${b.getAttribute('posts_id')}`);
        a.src = baseUrl + `images/${type}.png`;
        a.setAttribute("status",type);
        })
    .then(() => {
        setCountReaction_for_post('posts', b.getAttribute('posts_id'));
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

url_delete_react = "/reactions/delete_reaction/";
function delete_reaction_for_post(event){
    var b = event.target.parentNode.parentNode.parentNode.parentNode;
    formData = new FormData();
    formData.append('user_id',localStorage.getItem('id'));
    formData.append('user_name',localStorage.getItem('name'));
    formData.append('user_avatar',localStorage.getItem('avatar'));
    formData.append('posts_id',b.getAttribute('posts_id'));
    formData.append('comment_id',-1);
    formData.append('type',"like");
    formData.append('csrfmiddlewaretoken', csrftoken);

    a = document.getElementById(`reaction_img_${b.getAttribute('posts_id')}`);
  
    if(a.getAttribute('status') !== `default`){
        fetch(url_delete_react,{
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log("da huy:",data);
            a.src = baseUrl + `images/like3.png`;
            a.setAttribute("status","default");
        })
        .then(() => {
            setCountReaction_for_post('posts', b.getAttribute('posts_id'));
        })
    }
    else{
        fetch(url_creat_react,{
            method:"POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log("da react:",data);
            a.src = baseUrl + `images/like.png`;
            a.setAttribute("status","like");
        })
        .then(() => {
            setCountReaction_for_post('posts', b.getAttribute('posts_id'));
        })
    }
}
