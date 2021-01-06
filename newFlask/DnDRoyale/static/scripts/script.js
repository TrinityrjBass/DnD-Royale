
var num_entities = 0; // tracks the number of creatures currently in the roster. Not really needed now, but maybe when we test with a large amount of creatures.
var uniquenum = 0; // used to give each creature a unique number1
var lineup = [];// used to be window.lineup
var powerdict = {};
var selectedCreature = 0; // used when deleting creatures from the roster table

function flip(name, way) {
    if (way == 1) {
        $("#OFF_" + name).show();
        $("#ON_" + name).hide();
        $("#DIV_" + name).hide('slow');
    }
    else {
        $("#OFF_" + name).hide();
        $("#ON_" + name).show();
        $("#DIV_" + name).show('slow');
    }
}

//function duel_t() { // deprecated
//    var lineup = sessionStorage.getItem('lineup')
//    $.ajax({
//        type: "POST",
//        contentType: 'application/json',
//        url: "/poster/",
//        dataType: 'json',
//        data: JSON.stringify(lineup)
//    })
//        .done(function (msg) {
//            alert("Data Saved: " + msg);
//        });
//}

function duel() {
    flip("result", 1)
    //var options = getOptions();
    var list = expandLineup();
    list.unshift(getOptions());

    document.getElementById("status").innerHTML = "<i class='fa fa-spinner fa-pulse'></i> Simulation in progress.";
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) { Output(xmlhttp.responseText); }
    }
    xmlhttp.open("POST", "/poster/", true); 
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify(list));
}

function expandLineup() {
    let noobs = []; // new list
    let amount = 0; // number of creatures to by copied

    for (var h = 0; h < lineup.length; h++) {
        let c = lineup[h];
        let keys = Object.keys(c);
        amount = c.amount;

        if (keys.includes("amount")) {
            let i = keys.lastIndexOf("amount")// find index of amount in list
            keys.splice(i, 1); // remove amount from list.
            //print("amount found at index " + i);
        }
        for (var a = 0; a < amount; a++) { // dup creature 'a' times

            var newCreature = {};
            for (var index = 0; index < keys.length; index++) { // add attributes
                newCreature[keys[index]] = c[keys[index]];
            }
            newCreature['uid'] = getUid();
            noobs.push(newCreature);
        }
    }
    print("noobs : " + noobs);
    return noobs;
}

function getOptions() {
    let options = [];
    $("#DIV_options").find('input:checked').each(function () { // get all options that are selected
        options.push($(this).attr('name'));
    })
    return options;
}

function getUid() {
    let uid = uniquenum;
    uniquenum++;
    return uid;
}

//function Add(newbie) {
//    var lineup = JSON.parse(sessionStorage.getItem('lineup'));
//    lineup.push(newbie);
//    sessionStorage.setItem('lineup', JSON.stringify(lineup));
//    $("#lineup").html(JSON.stringify(lineup));
//}
// new function for adding teams

function Add(newbie) {
    // uniquenum++;
    lineup.push(newbie);
    print("added creature " + newbie.uid);
}

function AddA() {
    var newbie = $("#drop").val();
    var numberOf = $("#numberOfA").val();
    var team = $("input[name='team']:checked").val()
    num_entities += parseInt(numberOf);

    if (num_entities >= 1000) {
        // call alert/warning
        m = "Please be aware that adding more than 1000 combatants will impact performance. Keep this in mind when running the simulation.";
        showAlert(m);
    }
    $("#confA").show("slow");

    noob = { amount: numberOf, base: newbie, name: newbie, team: team , uid: getUid()}; 
    Add(noob);

    update_lineup();
    $("#confA").hide("slow");
}

// Generic function for showing Alerts
function showAlert(s) {
    alert(s);
}

function AddB() {
    var numberOf = $("#numberOfB").val();
    num_entities += parseInt(numberOf);

    $("#confC").show("slow");
    let newbie = getCustomCreature();
    newbie.team = $("input[name='team']:checked").val();
    newbie.uid = getUid();
    newbie.amount = numberOf;
    //print("new creature uid: " + newbie.uid);
    Add(newbie);
    
    update_lineup();
    $("#confC").hide("slow");
}

//function AddB() {
//    var numberOf = $("#numberOfB").val();
//    num_entities += parseInt(numberOf);

//    $("#confC").show("slow");
//    for (var x = 0; x < numberOf; x++) {
//        let newbie = getCustomCreature();
//        newbie.team = $("input[name='team']:checked").val();
//        newbie.uid = uniquenum;
//        //print("new creature uid: " + newbie.uid);
//        Add(newbie);
//    }
//    update_lineup();
//    $("#confC").hide("slow");
//}

function getCustomCreature() {
    let newCreature = {};
    $("#table").find('input').each(function (index, element) {
        key = $(this).attr('id');
        var v = $("#" + key).val();
        // if the value is not null
        if (!!v) {
            if (key != "numberOfB") {
                newCreature[key] = v;
            }
        }
    });
    return newCreature;
}

function calcBR(v) { // deprecating. CR is more important for the general app. BR can be figured IF user wants to use the morale system.
    if (v > 4) {
        var t = 1;
        // sans equation, so have to do with a switch to find BR.
        switch (v) {
            case "5":
                t = 5
            case "6":
                t = 7;
                break;
            case "7":
                t = 8;
                break;
            case "8":
                t = 9;
                break;
            case "9":
                t = 10.5;
                break;
            case "10":
                t = 12;
                break;
            case "11":
                t = 14;
                break;
            case "12":
                t = 15;
                break;
            case "13":
                t = 16.5;
                break;
            case "14":
                t = 18;
                break;
            case "15":
                t = 20;
                break;
            case "16":
                t = 22;
                break;
            case "17":
                t = 24;
                break;
            case "18":
                t = 27;
                break;
            case "19":
                t = 30;
                break;
            case "20":
                t = 33;
                break;
            case "21":
                t = 36;
                break;
            case "22":
                t = 40;
                break;
            case "23":
                t = 44;
                break;
            case "24":
                t = 48;
                break;
            case "25":
                t = 55;
                break;
            case "26":
                t = 68;
                break;
            case "27":
                t = 81;
                break;
            case "28":
                t = 95;
                break;
            case "29":
                t = 110;
                break;
            case "30":
                t = 126;
                break;
        }

        v = t;
    }
    return v;
}

function clearB() {
    // Resets the input values to default value, if one is assined else, makes field blank.

    $("#table").find('input').each(function (index, element) {
        key = $(this).attr('id');
        defaultVal = $(this).attr('value');

        // if the field has a default value, reset it
        if (!!defaultVal) {
            $("#" + key).val(defaultVal);
        }
        else { $("#" + key).val(""); } // else clear value
    })
}

function updateCustomBase() {
    let baseCreature = $('#drop').val();
    if (baseCreature == 'cthulhu') {
        $('#base').val('commoner');
    } else 
        $('#base').val(baseCreature);
}

function initial() {
    $("#def").keyup(function (event) { if (event.keyCode == 13) { AddB(); } });
    $("#confA").hide();
    $("#confB").hide();
    $("#failB").hide();
    sessionStorage.setItem('lineup', JSON.stringify([]));
    $("#OFF_more").hide();
    $("#OFF_work").hide();
    $("#OFF_limits").hide();
    $("#OFF_link").hide();
    $("#OFF_motive").hide();
    $("#OFF_tool").hide();
    $("#OFF_future").hide();
    $("#OFF_setup").hide();
    $("#ON_result").hide();
    $("#DIV_result").hide();
    $("#OUT_sample").hide();
    $("#showInfo").hide();
    $("#OFF_roster").hide();
    $("#ON_options").hide();
    $("#DIV_options").hide();
    // create roster table and set some variables
    rosterTable("hard");
    // iniitalize tooltips
    $('[data-toggle="tooltip]').tooltip();
    // initialize power chart
    loadPowerDict();
    updateGraph();
}

function loadPowerDict() {
    $("#drop").find('option').each(function (index, item) { // get all options that are selected
        print(item.value); //testing if the list loads before it's looked for.
        powerdict[item.value] = parseInt(item.getAttribute('data-xp'));
        // opt.forEach(function(item, index){ powerdict[item.value] = parseInt(item.getAttribute("data-xp"))}) 
    })
}

// deprecating... but might be able to be used with Plotly
function fix_doubles() {
    // is making a dict of combatants, numbering them per type and therefore making them unique for identification
    // I'm thinking there's got to be a more efficient way of ensuring uniqueness
    var unique = {};// this var is counting the number of unique creatures in the lineup. i'm assuming in the case of adding x A creatures, x B creatures, then going back and adding more A creatures
    for (var i = 0; i < lineup.length; i++) {
        if (!!lineup[i].replace) { //is string-like
            if (!!unique[lineup[i]]) {
                unique[lineup[i]]++;
                lineup[i] = { base: lineup[i], name: lineup[i] + ' #' + unique[lineup[i]].toString() };
            } else {
                // This is the first creature of it's type in unique[]
                unique[lineup[i]] = 1;
            }
        } else { // is dictionary.
            if (!lineup[i]['name']) {
                lineup[i]['name'] = 'Nameless'
            }
            var name = '';
            if (lineup[i]['name'].indexOf(' #') != -1) {
                name = lineup[i]['name'].split(' #')[0]
            } else {
                name = lineup[i]['name'];
            }
            if (unique[name]) {
                unique[name]++;
                lineup[i]['name'] = name + ' #' + unique[name].toString();
            } else {
                // this is the first 
                unique[lineup[i]['name']] = 1;
            }
        }
    }
}

function removeCombattant(i) {
    // needed to use a global variable to that that findCreatureByUid can use any number that was passed and not a static value
    selectedCreature = i;
    // get the index of the creature with the uid that matches the one that was passed.
    var index = lineup.findIndex(findCreatureByUid);
    // remove creature from lineup 
    lineup.splice(index, 1);
    num_entities -= 1;
    // redraw the roster table.
    update_lineup();
}
// find the index of the creature with the specified uid
function findCreatureByUid(creature) {
    return creature.uid == selectedCreature;
}

// in/decrement amount of specified group of creatures in lineup
function changeAmount(uid) {
    // TODO change the total of num_entities
    var numOf = $("#" + uid).val();
    num_entities = 0;
    let redPower = 0;
    let bluePower = 0;
    jQuery.each(lineup, function (index, c) {
        
        if (c.uid == uid) {
            c.amount = numOf;
        }
        num_entities += c.amount; // recount number of creatures
        // refigure power of teams
        if (c.team == "Red") {
            redPower += powerdict[c.name] * c.amount;
        }
        else {
            bluePower += powerdict[c.name] * c.amount;
        }
    });
    updateGraph(redPower, bluePower);
}

// generic print function for debugging
function print(s) {
    console.log(s);
}

function display_rosters(lineup) {
    // grab data for plotly graph... for later
    var redPower = 0;
    var bluePower = 0;
    // clear roster table so there aren't duplicates.
    rosterTable("soft");
    // display creatures in lineup -- for debugging purposes
    $('#lineup').html(JSON.stringify(lineup));

    // add creatures to roster
    jQuery.each(lineup, function (index, creature) {

        // add new row to table for the new creature
        $('#roster tbody').append('<tr></tr>');
        // populate new row with creature
        $('#roster tr:last').append('<td><input class="input-sm roster-input" value="' + creature.amount + '" type="number" min="0" style="width: 4em;" id="' + creature.uid + '" onChange="changeAmount(' + creature.uid + ')"> ' + creature.name + ' <span class="kill_me" onclick="removeCombattant(' + creature.uid + ')"><i class="fas fa-trash"></i></span></td>');
        // add team selection radio buttons for each available team
        $('#roster tr:last').append('<td> <input type="radio" name="' + creature.uid + '" value="' + "Red" + '" class="combatant_team" data-fullname="' + creature.name + '" onClick= changeTeam(' + creature.uid + ',"Red") ></td>');
        $('#roster tr:last').append('<td> <input type="radio" name="' + creature.uid + '" value="' + "Blue" + '" class="combatant_team" data-fullname="' + creature.name + '" onClick= changeTeam(' + creature.uid + ',"Blue") ></td>');
        
        let xp = powerdict[creature.base] * creature.amount;
        if (creature.team == "Red") {
            $(':radio[name="' + creature.uid + '"][value="Red"]').prop("checked", true);
            // add xp or power value to red 
            redPower += xp;
        }
        else {
            $(':radio[name="' + creature.uid + '"][value="Blue"]').prop("checked", true);
            // add xp or power value to blue
            bluePower += xp;
        }

    });
    updateGraph(redPower, bluePower);
}

function newRoster(lineup) {
    //new function for better ui
    rosterTable("soft");
    $('#lineup').html(JSON.stringify(lineup));

}

// Change creature to the other team
function changeTeam(uid, team) {
    print("change team. Current team is : " + team);
    selectedCreature = uid;
    // find creature by uid
    let index = lineup.findIndex(findCreatureByUid);
    let creature = lineup[index];
    // change team to other team
    if (team == "Blue") {
        creature.team = "Blue";
        $(':radio[name="' + creature.uid + '"][value="Blue"]').prop("checked", true);
        print("changed creature " + uid + "'s team from Red to Blue");        
    }
    else {
        creature.team = "Red";
        $(':radio[name="' + creature.uid + '"][value="Red"]').prop("checked", true);
        print("changed creature " + uid + "'s team from Blue to Red");
    }
    // update roster
    update_lineup();
}

function rosterTable(s) {
    // clear lineup
    if (s == "hard") {
        lineup = [];
        $("#lineup").html('');
    }
    // create new roster table
    $("#roster").html('<table style="width: 100%"><thead><tr><th>Name</th><th>Red</th><th>Blue</th></tr></thead><tbody></tbody></table>');
}


function update_lineup() {
    display_rosters(lineup);
}

$(document).ready(function () {
    initial();
}); 