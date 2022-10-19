//TODO make text full opacity when background isn't
//TODO filter functionality

//Element parameter is the button being clicked, this counteracts the fact that Jinja creates multiple buttons with the same ID
function toggle(element) {
    if(getComputedStyle(element).getPropertyValue("opacity") == 1) {
        //Toggle off
        element.style.opacity = 0.5
    } else {
        //Toggle on
        element.style.opacity = 1
    }
}