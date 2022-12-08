setInterval(function updateProgressBar() {
    document.querySelectorAll('progress.timeRemaining').forEach(bar => {
        if(bar.value < 60) {
            bar.value = bar.value + 1
        } else {
            stopRunningAnimation(bar.parentElement.querySelector('img'))
        }
    }) 
    document.querySelectorAll('p.timeRemaining').forEach(p => {
        var timeRemaining = p.innerHTML.split(' ')[0]
        if(timeRemaining > 0) {
            p.innerHTML = `${timeRemaining - 1} minutes remaining`
        } else {
            p.innerHTML = "Done"
        }
    })
}, 60*1000)

function startRunningAnimation(imgElement) {
    imgElement.classList.add('running')
        if(imgElement.getAttribute('src') == "/static/images/full_washer.png") {
            imgElement.src = "/static/images/running_washer.gif";
        } else if(imgElement.getAttribute('src') == "/static/images/full_dryer.png") {
            imgElement.src = "/static/images/running_dryer.gif";
        }
}
function stopRunningAnimation(imgElement) {
    imgElement.classList.remove('running')
        if(imgElement.getAttribute('src') == "/static/images/running_washer.gif") {
            imgElement.src = "/static/images/full_washer.png";
        } else if(imgElement.getAttribute('src') == "/static/images/running_dryer.gif") {
            imgElement.src = "/static/images/full_dryer.png";
        }
}
