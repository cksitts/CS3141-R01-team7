function toggleDropdown() {
    if(getComputedStyle(document.getElementById('profileDropdown')).getPropertyValue("display") == 'block') {
        document.getElementById('profileDropdown').style.animationName = 'dropupAnimation';
        document.getElementById('profileDropdown').style.animationPlayState = 'running';

        setTimeout("document.getElementById('profileDropdown').style.display = 'none';", 500);
        
        //button style
        document.getElementById('dropdownButton').style.border = 'none';
    } else {
        document.getElementById('profileDropdown').style.animationName = 'dropdownAnimation';
        document.getElementById('profileDropdown').style.animationPlayState = 'running';

        setTimeout("document.getElementById('profileDropdown').style.display = 'block';", 500);
        
        //button style
        document.getElementById('dropdownButton').style.border = '2px solid var(--main-dark)';
    }
}