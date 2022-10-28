function positionMessage() { //BUG message doesn't move when screen resizes
    const errorMessage = document.getElementById('invalidMessage');
    
    errorMessage.style.position = 'absolute';
    errorMessage.style.width = '100%';
    errorMessage.style.fontSize = '0.8em';
    errorMessage.style.textAlign = 'center';
    errorMessage.style.marginTop = '35px';
    errorMessage.style.top = `${document.getElementById('usernameInput').getBoundingClientRect().top}px`;
}