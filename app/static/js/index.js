window.onresize = function() {
    positionMessage();
}

function positionMessage() {
    const errorMessage = document.getElementById('invalidMessage');
    
    if(errorMessage) {
        errorMessage.style.position = 'fixed';
        errorMessage.style.width = '100%';
        errorMessage.style.fontSize = '0.8em';
        errorMessage.style.textAlign = 'center';
        errorMessage.style.top = `${document.getElementById('usernameInput').getBoundingClientRect().bottom}px`;
    }
}