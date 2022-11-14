//Element parameter is the button being clicked, this counteracts the fact that Jinja creates multiple buttons with the same ID
var checkStyleWasher = 0;
var checkStyleDryer = 0;
function toggle(element) {
    //Turn RGB background color into RGBA (Assumes room dropdown and toggle buttons are the same color)
    onColor = getComputedStyle(document.getElementById("roomDropdown")).getPropertyValue("background-color")
    offColor = onColor.slice(0, -1) + ", 0.4)"

    if(element.dataset.toggleOn == 'True') {
        //Toggle off
        element.dataset.toggleOn = 'False'
        element.style.backgroundColor = offColor

        if(element.dataset.filterType == "available") {
            machineBlocks = document.querySelectorAll('.availableMachineBlock')
        } else {
            machineBlocks = document.querySelectorAll('.unavailableMachineBlock')
        }
        
        machineBlocks.forEach((block) => {
            if (block.querySelector('p.machineType').innerHTML == element.id.substring(0, element.id.length - 6)) {
                block.dataset.showType = "False"
            }
        })
    } else {
        //Toggle on
        element.dataset.toggleOn = 'True'
        element.style.backgroundColor = onColor

        if(element.dataset.filterType == "available") {
            machineBlocks = document.querySelectorAll('.availableMachineBlock')
        } else {
            machineBlocks = document.querySelectorAll('.unavailableMachineBlock')
        }        

        machineBlocks.forEach((block) => {
            if (block.querySelector('p.machineType').innerHTML == element.id.substring(0, element.id.length - 6)) {
                block.dataset.showType = "True"
            }
        })
    }
    updateVisible()
}

//Updates room selection dropdown filter
function updateDropdownFilter(dropdown) {
    if(dropdown.value == 'all') {
        //Make all machines visible
        document.querySelectorAll('.availableMachineBlock, .unavailableMachineBlock').forEach((block) => {
            block.dataset.showLocation = "True"
        })
    } else {
        //Make only selected room visible
        document.querySelectorAll('.availableMachineBlock, .unavailableMachineBlock').forEach((block) => {
            if (block.querySelector('p.machineLocation').innerHTML.split("<br>")[1] != dropdown.value.split(" (")[0]) {
                block.dataset.showLocation = "False"
            } else {
                block.dataset.showLocation = "True"
            }
        })
    }

    updateVisible()
}

//Updates time slider filter
function updateSliderFilter(form) {
    document.querySelectorAll('.availableMachineBlock, .unavailableMachineBlock').forEach((block) => {
        if(block.querySelector('h3').innerHTML == 'Unavailable' && parseInt(block.querySelector('p.timeRemaining').innerHTML.split(' ')[0]) > parseInt(timeInput.value)) {
           block.dataset.showTime = "False"
        } else {
            block.dataset.showTime = "True" //filter doesn't affect available machines
        }
    })

    updateVisible()
}


function updateVisible() {
    document.querySelectorAll('.availableMachineBlock, .unavailableMachineBlock').forEach((block) => {
            if (block.dataset.showType == "True" && block.dataset.showLocation == "True" && block.dataset.showTime == "True") {
                block.style.display = 'block'
            } else {
                block.style.display = 'none'
            }
        })
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
