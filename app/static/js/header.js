//Profile info dropdown animation
window.onload = () => {
    if ("ontouchstart" in document.documentElement) {
        console.log("Mobile")
        document.getElementById('dropdownButton').addEventListener("click", dropdownDown)
        
    } else {
        console.log("Desktop")
        document.getElementById('dropdownButton').addEventListener("mouseenter", dropdownDown)
        document.getElementById('profileDropdown').addEventListener("mouseleave", dropdownUp)
    }
}

function dropdownDown() {
    document.getElementById('profileDropdown').style.animationName = 'dropdownAnimation';
    document.getElementById('profileDropdown').style.animationPlayState = 'running';

    setTimeout("document.getElementById('profileDropdown').style.display = 'block';", 500);
    
    //button style
    document.getElementById('dropdownButton').style.border = '2px solid var(--main-dark)';

    //handle mobile
    if ("ontouchstart" in document.documentElement) {
        document.getElementById('dropdownButton').removeEventListener("click", dropdownDown)
        document.getElementById('dropdownButton').addEventListener("click", dropdownUp)
    }
}
function dropdownUp() {
    document.getElementById('profileDropdown').style.animationName = 'dropupAnimation';
    document.getElementById('profileDropdown').style.animationPlayState = 'running';

    setTimeout("document.getElementById('profileDropdown').style.display = 'none';", 500);
    
    //button style
    document.getElementById('dropdownButton').style.border = 'none';

    //handle mobile
    if ("ontouchstart" in document.documentElement) {
        document.getElementById('dropdownButton').removeEventListener("click", dropdownUp)
        document.getElementById('dropdownButton').addEventListener("click", dropdownDown)
    }
}
