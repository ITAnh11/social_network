function show_list_reaction(event){
    var a = event.target.parentNode.parentNode.parentNode.querySelector(".list_reaction");
    a.classList.toggle("show_list_reaction");
}


function setCountReaction(forWhat, idWhat){
    formData = new FormData();
    what = (forWhat == 'posts') ? 'posts_id' : 'comment_id';
    otherWhat = (what == 'posts_id') ? 'comment_id' : 'posts_id';

    formData.append(what, idWhat);
    formData.append(otherWhat, -1);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(api_get_reactions, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        count = data.count;
        document.getElementById(`count-reaction-${forWhat}-${idWhat}`).textContent = count;
    })
}
