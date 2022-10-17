function validateForm() {
    //validate email
    //TODO check if email is already taken in the database
    if(false) {
        alert("That email is already registered")
        return false
    }

    //validate username
    //Regex used: any combination of letters, numbers, and underscores. Min length 6 characters.
    const usernameRegex = /^[\w]{6,}$/
    if(!usernameRegex.test(document.getElementById('usernameInput').value)) {
        alert("Invalid username, please do not use special characters (minimum length 6)")
        return false
    }
    //TODO check if username is already taken in the database
    if(false) {
        alert("That username is already taken")
        return false
    }

    //validate password
    //Regex used: any combination of letters, numbers, and special characters. Min length 8 characters.
    const passwordRegex = /^.{8,}$/
    if(!passwordRegex.test(document.getElementById('passwordInput').value)) {
        alert("Invalid password, please do not use special characters (minimum length 8)")
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