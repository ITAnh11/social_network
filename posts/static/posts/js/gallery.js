const TIME_DELAY_LOAD_IMAGE = 222;

export function createLayoutImages(images, galleryContainerElement) {
    const length = images.length;
    if (length === 1) {
        layout1(images, galleryContainerElement);
    } else if (length === 2) {
        layout2(images, galleryContainerElement);
    } else if (length === 3) {
        layout3(images, galleryContainerElement);
    } else if (length === 4) {
        layout4(images, galleryContainerElement);
    } else if (length === 5) {
        layout5(images, galleryContainerElement);
    } else if (length > 5) {
        layoutMoreThan5(images, galleryContainerElement);
    }
}

function layout1(images, galleryContainerElement) {
    galleryContainerElement.innerHTML += `<img
                class="gallery-image gallery-normal-image"
                src="${images[0].media}"
                alt="Image"
            />`
}

function layout2(images, galleryContainerElement) {

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
                                                class="gallery-image gallery-three-grid-cells"
                                                src="${images[0].media}"
                                                alt="Image"
                                            />`
    }, TIME_DELAY_LOAD_IMAGE * 1);


    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
                                                class="gallery-image gallery-three-grid-cells"
                                                src="${images[1].media}"
                                                alt="Image"
                                            />`
    }, TIME_DELAY_LOAD_IMAGE * 2);
}

function layout3(images, galleryContainerElement) {

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img class="gallery-image gallery-four-grid-cells"
        src="${images[0].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img class="gallery-image gallery-two-grid-cells"
        src="${images[1].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img class="gallery-image gallery-two-grid-cells"
        src="${images[2].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);
}

function layout4(images, galleryContainerElement) {
    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-three-grid-cells"
        src="${images[0].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-three-grid-cells"
        src="${images[1].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image gallery-three-grid-cells"
        src="${images[2].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image gallery-three-grid-cells"
        src="${images[3].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 4);
}

function layout5(images, galleryContainerElement) {
    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[0].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[1].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[2].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[3].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 4);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[4].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 5);
}

function layoutMoreThan5(images, galleryContainerElement)  {
    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[0].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 1);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img
        class="gallery-image gallery-wide-image"
        src="${images[1].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 2);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[2].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 3);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `<img 
        class="gallery-image"
        src="${images[3].media}"
        alt="Image"
    />`
    }, TIME_DELAY_LOAD_IMAGE * 4);

    setTimeout(() => {
        galleryContainerElement.innerHTML += `
        <div class="gallery-image-container gallery-image">
            <img 
                class="gallery-image"
                src="${images[4].media}"
                alt="Image"
            />
            <div class="gallery-image-overlay gallery-image">
                <p class="gallery-plus">+${images.length - 5}</p>
            </div>
        </div>
        `
    }, TIME_DELAY_LOAD_IMAGE * 5);
}