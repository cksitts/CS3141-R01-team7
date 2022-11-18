//Popup dialog for machine checkout
function showCheckoutDialog(machine) {
    //Parse machine into dictionary
    console.log(machine)
    machine = JSON.parse(machine.replaceAll('&#39;','"').replaceAll('True', '"True"').replaceAll('False','"False"'))

    //Get element references
    div = document.getElementById('checkoutDialogDiv')
    machineInfo = div.children[1]
    dueTime = div.children[2]
    form = div.children[5]

    //Determine what time is 1 hour from now
    var today = new Date()
    hour = today.getHours()
    minute = today.getMinutes()
    minute = minute < 10 ? '0'+minute.toString() : minute
    hour += 1
    if(hour > 12) {
        hour = hour - 12
        time = hour + ":" + minute + "pm"
    } else {
        time = hour + ":" + minute + "am"
    }

    //Set text
    div.style.display = 'block'
    machineInfo.innerHTML = "Would you like to check out " + machine['machine-type'].toLowerCase() + " " + machine['machine-id'].split('_')[2] + " from " + getRoom(machine['machine-id']) + " for one hour?"
    dueTime.innerHTML = "Due back at " + time

    //Set form action
    form.action = '/checkout/' + machine['machine-id']
}


//Close dialog box
function closeCheckoutDialog() {
    div = document.getElementById('checkoutDialogDiv')
    div.style.display = 'none'
}

var timeValue = 0;
function progressTimer() {
    var progressBar = document.getElementById('progressBar');
    setInterval( function() {
    if (timeValue < 61) {
        timeValue++;
        progressBar.value = timeValue
    }
    timer();
    }, 1000)
}