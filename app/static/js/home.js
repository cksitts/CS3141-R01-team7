//Profile info dropdown animation
function dropdownDown() {
    document.getElementById('profileDropdown').style.animationName = 'dropdownAnimation';
    document.getElementById('profileDropdown').style.animationPlayState = 'running';

    setTimeout("document.getElementById('profileDropdown').style.display = 'block';", 500);
    
    //button style
    document.getElementById('dropdownButton').style.border = '2px solid var(--main-dark)';
}
function dropdownUp() {
    document.getElementById('profileDropdown').style.animationName = 'dropupAnimation';
    document.getElementById('profileDropdown').style.animationPlayState = 'running';

    setTimeout("document.getElementById('profileDropdown').style.display = 'none';", 500);
    
    //button style
    document.getElementById('dropdownButton').style.border = 'none';
}
