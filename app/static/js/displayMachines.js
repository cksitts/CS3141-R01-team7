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


//Takes in machine ID and returns room and building
function getRoom(id) {
    id = id.split('_')
    switch(id[1]) {
    case 'WH':
        id[1] = "Wads"
        break;
    case 'MH':
        id[1] = "McNair"
        break;
    // case 'DHH':
    //     id[1] = "DHH"
    //     break;
    }
    id = id[0] + " " + id[1]
    return id
}