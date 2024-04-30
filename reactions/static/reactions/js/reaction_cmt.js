var post_id = document.body.getAttribute('post_id');
setCountReaction_for_post("posts", post_id);
is_reacted_for_post(post_id);

url_get_reactions ="/reactions/get_reactions/";
function setCountReaction_for_cmt(forWhat, idWhat){
    formData = new FormData();
    what = (forWhat == 'posts') ? 'posts_id' : 'comment_id';
    otherWhat = (what == 'posts_id') ? 'comment_id' : 'posts_id';

    formData.append(what, idWhat);
    formData.append(otherWhat, post_id);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(url_get_reactions, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("so luong react cmt:",data);
        count = data.total;
        document.getElementById(`count-reaction-${forWhat}-${idWhat}`).textContent = count;
        var iconTopReactionsContainer = document.getElementById(`icon-top-reactions-comment-container-${idWhat}`);
        iconTopReactionsContainer.innerHTML = '';
        
        if(data.topMostReacted[0].total !== 0 && data.topMostReacted[1].total !== 0){

            var top2_react = document.createElement('img');
            top2_react.classList.add("top2-react-in-cmt");
            top2_react.src = `${baseUrl + `images/${data.topMostReacted[1].type}.png`}`;

            iconTopReactionsContainer.insertBefore(top2_react, iconTopReactionsContainer.firstChild);


            var top1_react = document.createElement('img');
            top1_react.classList.add("top1-react-in-cmt");
            top1_react.src = `${baseUrl + `images/${data.topMostReacted[0].type}.png`}`;
            
            iconTopReactionsContainer.insertBefore(top1_react, iconTopReactionsContainer.firstChild);
        }
        else if(data.topMostReacted[0].total !== 0){
            var top1_react = document.createElement('img');
            top1_react.classList.add("top1-react-in-cmt");
            top1_react.src = `${baseUrl + `images/${data.topMostReacted[0].type}.png`}`;

            iconTopReactionsContainer.insertBefore(top1_react, iconTopReactionsContainer.firstChild);
        }
    })
}

url_creat_react = "/reactions/create_reaction/";
function create_reaction_for_cmt(event){
    var type = event.target.className;
    var b = event.target.parentNode.parentNode;
    formData = new FormData();
    formData.append('user_id',localStorage.getItem('id'));
    formData.append('user_name',localStorage.getItem('name'));
    formData.append('user_avatar',localStorage.getItem('avatar'));
    formData.append('posts_id',post_id);
    formData.append('comment_id',b.getAttribute("comment_id"));
    formData.append('type',type);
    formData.append('csrfmiddlewaretoken', csrftoken);
    
    fetch(url_creat_react,{
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("da react cmt:",type,data);
        a = document.getElementById(`react-cmt-${b.getAttribute("comment_id")}`);
        a.setAttribute("status",type);
        })
    .then(() => {
        setCountReaction_for_cmt('comment', b.getAttribute("comment_id"));
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

url_is_reacted = "/reactions/is_reacted/";
function is_reacted_for_cmt(comment_id){

    formData = new FormData();
    formData.append('posts_id',post_id);
    formData.append('comment_id',comment_id);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(url_is_reacted,{
        method:"POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("myReaction:",data);
        if(data.is_reacted === true){
            a = document.getElementById(`react-cmt-${comment_id}`);
            a.setAttribute("status",data.type);
        }
    })
}

url_delete_react = "/reactions/delete_reaction/";
function delete_reaction_for_cmt(event){
    var b = event.target;
    formData = new FormData();
    formData.append('user_id',localStorage.getItem('id'));
    formData.append('user_name',localStorage.getItem('name'));
    formData.append('user_avatar',localStorage.getItem('avatar'));
    formData.append('posts_id',post_id);
    formData.append('comment_id',b.getAttribute("comment_id"));
    formData.append('type',"like");
    formData.append('csrfmiddlewaretoken', csrftoken);

    a = document.getElementById(`react-cmt-${b.getAttribute("comment_id")}`);
  
    if(a.getAttribute('status') !== `default`){
        fetch(url_delete_react,{
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log("da huy:",data);
            a.setAttribute("status","default");
        })
        .then(() => {
            setCountReaction_for_cmt('comment', b.getAttribute("comment_id"));
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
            a.setAttribute("status","like");
        })
        .then(() => {
            setCountReaction_for_cmt('comment', b.getAttribute("comment_id"));
        })
    }
}
