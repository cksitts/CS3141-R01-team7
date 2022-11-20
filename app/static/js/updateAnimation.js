function updateAnimation(imgElement) {
    if(imgElement.classList.contains('running')) {
        //stop running animation
        imgElement.classList.remove('running')
        if(imgElement.getAttribute('src') == "/static/images/running_washer.gif") {
            imgElement.src = "/static/images/full_washer.png";
        } else if(imgElement.getAttribute('src') == "/static/images/running_dryer.gif") {
            imgElement.src = "/static/images/full_dryer.png";
        }
    } else {
        //start running animation
        imgElement.classList.add('running')
        if(imgElement.getAttribute('src') == "/static/images/full_washer.png") {
            imgElement.src = "/static/images/running_washer.gif";
        } else if(imgElement.getAttribute('src') == "/static/images/full_dryer.png") {
            imgElement.src = "/static/images/running_dryer.gif";
        }
    }
}

                        