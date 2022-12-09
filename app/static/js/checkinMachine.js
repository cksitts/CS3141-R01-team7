//Popup dialog for machine checkout
function showCheckinDialog(machine) {
    //Parse machine into dictionary
    machine = JSON.parse(machine.replaceAll("'",'"').replaceAll('True', '"True"').replaceAll('False','"False"'))

    //Get element references
    div = document.getElementById('checkinDialogDiv')
    machineInfo = div.children[1]
    form = div.children[4]

    //Set text
    div.style.display = 'block'
    machineInfo.innerHTML = "Would you like to check in mixer " + machine['machine-id'].split('_')[2] + " from " + getRoom(machine['machine-id']) + "?"

    //Set form action
    form.action = '/checkin/' + machine['machine-id']
}


//Close dialog box
function closeCheckinDialog() {
    div = document.getElementById('checkinDialogDiv')
    div.style.display = 'none'
}