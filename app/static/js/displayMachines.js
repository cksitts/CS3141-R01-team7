//TODO make text full opacity when background isn't
//TODO filter functionality
//TODO make the unavailable and available buttons work separately (they have the same ID which does not work)
function toggleWasher() {
    if(getComputedStyle(document.getElementById('washerToggle')).getPropertyValue("opacity") == 1) {
        //Toggle off
        document.getElementById('washerToggle').style.opacity = 0.5
        console.log("toggle washer off")
    } else {
        //Toggle on
        document.getElementById('washerToggle').style.opacity = 1
        console.log("toggle washer on")
    }
}

function toggleDryer() {
    console.log(getComputedStyle(document.getElementById('dryerToggle')).getPropertyValue("opacity"))
    if(getComputedStyle(document.getElementById('dryerToggle')).getPropertyValue("opacity") == 1) {
        //Toggle off
        console.log("A")
        document.getElementById('dryerToggle').style.opacity = 0.5
        console.log("toggle dryer off")
    } else {
        //Toggle on
        console.log("B")
        document.getElementById('dryerToggle').style.opacity = 1
        console.log("toggle dryer on")
    }
}