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


//Takes in machine ID and returns machine number
function getNumber(id) {
    return id.split('_')[2]
}