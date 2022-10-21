function validateForm() {
    //validate username
    //Regex used: any combination of letters, numbers, and underscores. Min length 6 characters.
    const usernameRegex = /^[\w]{6,}$/
    if(!usernameRegex.test(document.getElementById('usernameInput').value)) {
        alert("Invalid username, please do not use special characters (minimum length 6)")
        return false
    }

    //validate password
    //Regex used: any combination of letters, numbers, and special characters. Min length 8 characters.
    const passwordRegex = /^.{8,}$/
    if(!passwordRegex.test(document.getElementById('passwordInput').value)) {
        alert("Invalid password, minimum length 8")
        return false
    }

    //ensure password and confirm password match
    if(document.getElementById('passwordInput').value != document.getElementById('confirmPassword').value) {
        alert("Password and confirmation do not match")
        return false
    }

    //if everything else has been validated
    return true
}