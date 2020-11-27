// hosted file

var num_entities = 0; // tracks the number of creatures currently in the roster. Not really needed now, but maybe when we test with a large amount of creatures.
var uniquenum = 0; // used to give each creature a unique number1
var lineup = [];// used to be window.lineup
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

//function duel_t() {
//    $.ajax({
//        method: "POST",
//        url: "",
//        data: []
//    })
//        .done(function (msg) {
//            alert("Data Saved: " + msg);
//        });
//}

function duel_t() {
    var lineup = sessionStorage.getItem('lineup')
    $.ajax({
        type: "POST",
        contentType: 'application/json',
        url: "/poster/",
        dataType: 'json',
        data: JSON.stringify(lineup)
    })
        .done(function (msg) {
            alert("Data Saved: " + msg);
        });
}


function Output(text) {
    // would like to add some logic here to only show error if unsuccessful simulation
    // Add 'sample encounter data' from output to be viewable somehow.
    let modal = $("#result");

    $("#result").show();
    $("#myModal").modal("toggle")
    $("#showInfo").show();
    modal.append('<div id="OUT_battles"></div>')
    modal.append('<div id="OUT_rounds"></div>')
    modal.append('<div id="OUT_prediction"></div>')
    modal.append('<div id="OUT_notes"></div>')
    modal.append('<div id="OUT_team"></div>')
    modal.append('<div id="OUT_combattant"></div>')

    $("#status").html("Calculations complete");
    flip("result", 0);
    console.log(text);
    reply = JSON.parse(text);

    header = {
        notes: "Notes",
        rounds: "Total number of rounds fought",
        battles: "Total number of battles fought",
        prediction: "Rought predictions",
    }
    for (k in header) {
        console.log("#OUT_" + k)
        $("#OUT_" + k).html(header[k] + ": " + reply[k]);
    }
    tmax = 100 / 4;
    t = "<table class=res><thead><tr>" +
        "<th width='" + tmax + "%'>Team name</th>" +
        "<th width='" + tmax + "%'>Number of victories</th>" +
        "<th width='" + tmax + "%'>Number of close calls</th>" +
        "<th width='" + tmax + "%'>Number of perfects</th>" + "</tr></thead><tbody>";
    for (ti = 0; ti < reply["team_names"].length; ti++) {
        t += "<tr><th width='" + tmax + " %'>" + reply["team_names"][ti] + "</th><td width='" + tmax + "%'>" +
            reply["team_victories"][ti] + "</td><td width='" + tmax + "%'>" +
            reply["team_close"][ti] + "</td><td width='" + tmax + "%'>" +
            reply["team_perfects"][ti] + "</td>" + "</tr>";
    }
    t += "</tbody></table>";
    $("#OUT_team").html(t);
    cmax = 100 / 6;
    c = "<table class='res table table-hover'><thead><tr>" +
        "<th width='" + cmax + "%'>Combattant</th>" +
        "<th width='" + cmax + "%'>Team</th>" +
        "<th width='" + cmax + "%'>avg damage</th>" +
        "<th width='" + cmax + "%'>avg hits</th>" +
        "<th width='" + cmax + "%'>avg misses</th>" +
        "<th width='" + cmax + "%'>avg rounds</th>" +
        "</tr></thead><tbody>";
    for (ci = 0; ci < reply["combattant_names"].length; ci++) {
        c += "<tr><th width='" + cmax + " %'>" + reply["combattant_names"][ci] + "</th><td width='" + cmax + " %'>" +
            reply["combattant_alignments"][ci] + "</td><td width='" + cmax + " %'>" +
            parseFloat(reply["combattant_damage_avg"][ci]).toFixed(2) + "</td><td width='" + cmax + " %'>" +
            parseFloat(reply["combattant_hit_avg"][ci]).toFixed(2) + "</td><td width='" + cmax + " %'>" +
            parseFloat(reply["combattant_miss_avg"][ci]).toFixed(2) + "</td><td width='" + cmax + " %'>" +
            parseFloat(reply["combattant_rounds"][ci]).toFixed(2) + "</td>" +
            "</tr>";
    }
    c += "</table>";
    $("#OUT_combattant").html(c);
    $("#OUT_sample").html(reply['sample_encounter']);
}

function duel() {
    flip("result", 1)
    document.getElementById("status").innerHTML = "<i class='fa fa-spinner fa-pulse'></i> Simulation in progress.";
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) { Output(xmlhttp.responseText); }
    }
    xmlhttp.open("POST", "/poster/", true); 
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify(lineup));
}

//function Add(newbie) {
//    var lineup = JSON.parse(sessionStorage.getItem('lineup'));
//    lineup.push(newbie);
//    sessionStorage.setItem('lineup', JSON.stringify(lineup));
//    $("#lineup").html(JSON.stringify(lineup));
//}
// new function for adding teams

function Add(newbie) {
    uniquenum++;
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
        m = "Please be aware that adding more than 100 combatants will impact performance. Keep this in mind when running the simulation.";
        showAlert(m);
    }
    $("#confA").show("slow");
    for (var x = 0; x < numberOf; x++) {
        noob = { base: newbie, name: newbie, team: team , uid: uniquenum }; 
        Add(noob);
    }
    update_lineup();
    $("#confA").hide("slow");
}

// Generic function for showing Alerts
function showAlert(s) {
    alert(s);
}

function AddB() {
    var numberOf = $("#numberOfC").val();
    num_entities += parseInt(numberOf);

    $("#confC").show("slow");
    for (var x = 0; x < numberOf; x++) {
        let newbie = getCustomCreature();;
        newbie.team = $("input[name='team']:checked").val();
        newbie.uid = uniquenum;
        print("new creature uid: " + newbie.uid);
        Add(newbie);
    }
    update_lineup();
    $("#confC").hide("slow");
}

function getCustomCreature() {
    let newCreature = {};
    $("#table").find('input').each(function (index, element) {
        key = $(this).attr('id');
        var v = $("#" + key).val();
        // if the value is not null
        if (!!v) {
            // get value of BR/Morale from CR and store value
            if (key == "CR") {
                key = "BR"; //this could also be "morale"
                v = calcBR(v);
                // newbie[key] = v;
            }
            ;
            // skip the value of input field
            if (key != "numberOfC") {
                newCreature[key] = v;
            }

        }

    });
    return newCreature;
}

function calcBR(v) {
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
    $("#confC").hide();
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
    // create roster table and set some variables
    rosterTable("hard");
    // iniitalize tooltips
    $('[data-toggle="tooltip]').tooltip();
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
// generic print function for debugging
function print(s) {
    console.log(s);
}

function showModal() {
    $("#myModal").modal("toggle");
}

function display_rosters(lineup) {
    // grab data for plotly graph... for later

    // clear roster table so there aren't duplicates.
    rosterTable("soft");
    // display creatures in lineup
    $('#lineup').html(JSON.stringify(lineup));

    // add creatures to roster
    jQuery.each(lineup, function (index, creature) {

        // add new row to table for the new creature
        $('#roster tbody').append('<tr></tr>');
        // populate new row with creature
        $('#roster tr:last').append('<td>' + creature.name + ' <span class="kill_me" onclick="removeCombattant(' + creature.uid + ')"><i class="fas fa-trash"></i></span></td>');
        
        $('#roster tr:last').append('<td> <input type="radio" name="' + creature.uid + '" value="' + "Red" + '" class="combatant_team" data-fullname="' + creature.name + '" onClick= changeTeam('+ creature.uid + ',"Red") ></td>');
        $('#roster tr:last').append('<td> <input type="radio" name="' + creature.uid + '" value="' + "Blue" + '" class="combatant_team" data-fullname="' + creature.name + '" onClick= changeTeam(' + creature.uid + ',"Blue") ></td>');
            // add team selection radio buttons for each available team
            if (creature.team == "Red") {
                $(':radio[name="' + creature.uid + '"][value="Red"]').prop("checked", true);
            }
            else {
                $(':radio[name="' + creature.uid + '"][value="Blue"]').prop("checked", true);
        }
        
    });
    
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