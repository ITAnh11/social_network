const TIME_DELAY_LOAD_IMAGE = 222;

function createLayoutImages(images, galleryContainerElement, posts_id) {
    const length = images.length;
    if (length === 1) {
        layout1(images, galleryContainerElement, posts_id);
    } else if (length === 2) {
        layout2(images, galleryContainerElement, posts_id);
    } else if (length === 3) {
        layout3(images, galleryContainerElement, posts_id);
    } else if (length === 4) {
        layout4(images, galleryContainerElement, posts_id);
    } else if (length === 5) {
        layout5(images, galleryContainerElement, posts_id);
    } else if (length > 5) {
        layoutMoreThan5(images, galleryContainerElement, posts_id);
    }
}

function layout1(images, galleryContainerElement, posts_id) {
    galleryContainerElement.innerHTML += `<img
                class="gallery-image gallery-normal-image"
                src="${images[0].media}"
                alt="Image"
                image_id="1"
                posts_id="${posts_id}"
                onclick="clickImage(event)"
            />`
}

function layout2(images, galleryContainerElement, posts_id) {

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
                                                class="gallery-image gallery-three-grid-cells"
                                                src="${images[0].media}"
                                                alt="Image"
                                                image_id="1"
                                                posts_id="${posts_id}"
                                                onclick="clickImage(event)"
                                            />`
    }, TIME_DELAY_LOAD_IMAGE * 1);


    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
                                                class="gallery-image gallery-three-grid-cells"
                                                src="${images[1].media}"
                                                alt="Image"
                                                image_id="2"
                                                posts_id="${posts_id}"
                                                onclick="clickImage(event)"
                                            />`
    }, TIME_DELAY_LOAD_IMAGE * 2);
}

function layout3(images, galleryContainerElement, posts_id) {

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img class="gallery-image gallery-four-grid-cells"
        src="${images[0].media}"
        alt="Image"
        image_id="1"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img class="gallery-image gallery-two-grid-cells"
        src="${images[1].media}"
        alt="Image"
        image_id="2"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img class="gallery-image gallery-two-grid-cells"
        src="${images[2].media}"
        alt="Image"
        image_id="3"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);
}

function layout4(images, galleryContainerElement, posts_id) {
    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-three-grid-cells"
        src="${images[0].media}"
        alt="Image"
        image_id="1"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-three-grid-cells"
        src="${images[1].media}"
        alt="Image"
        image_id="2"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image gallery-three-grid-cells"
        src="${images[2].media}"
        alt="Image"
        image_id="3"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image gallery-three-grid-cells"
        src="${images[3].media}"
        alt="Image"
        image_id="4"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 4);
}

function layout5(images, galleryContainerElement, posts_id) {
    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[0].media}"
        alt="Image"
        image_id="1"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[1].media}"
        alt="Image"
        image_id="2"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[2].media}"
        alt="Image"
        image_id="3"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[3].media}"
        alt="Image"
        image_id="4"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 4);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[4].media}"
        alt="Image"
        image_id="5"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 5);
}

function layoutMoreThan5(images, galleryContainerElement, posts_id) {
    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[0].media}"
        alt="Image"
        image_id="1"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[1].media}"
        alt="Image"
        image_id="2"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[2].media}"
        alt="Image"
        image_id="3"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[3].media}"
        alt="Image"
        image_id="4"
        posts_id="${posts_id}"
        onclick="clickImage(event)"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 4);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `
        <div class="gallery-image-container gallery-image">
            <img 
                class="gallery-image"
                src="${images[4].media}"
                alt="Image"
                image_id="5"
                posts_id="${posts_id}"
                onclick="clickImage(event)"
            />
            <div class="gallery-image-overlay gallery-image" image_id="5" posts_id="${posts_id}" onclick="clickImage(event)">
                <p class="gallery-plus">+${images.length - 5}</p>
            </div>
        </div>
        `
    }, TIME_DELAY_LOAD_IMAGE * 5);
}


function clickImage(event) {
    event.stopPropagation();
    console.log(event.target.getAttribute('posts_id'));
    console.log(event.target.getAttribute('image_id'));

    posts_id = event.target.getAttribute('posts_id');
    image_id = event.target.getAttribute('image_id');

    url = 'posts/page/?posts_id=' + posts_id + '&image_id=' + image_id;

    window.location.href = url;
}