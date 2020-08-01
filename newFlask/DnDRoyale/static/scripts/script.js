// hosted file

// dictionary to hold weapons and their damage dice type. used to compile the new version of attack parameters
var armory = {
    'club': 4,
    'great club': 8,
    'dagger': 4,
    'short sword': 6,
    'long sword': 8,
    'bastard sword': 10,
    'great sword': 12,
    'rapier': 8,
    'scimitar': 6,
    'sickle': 4,
    'hand axe': 6,
    'battle axe': 8,
    'war axe': 10,
    'great axe': 12,
    'javelin': 6,
    'spear': 6,
    'flail': 8,
    'glaive': 10,
    'halberd': 10,
    'lance': 12,
    'pike': 10,
    'trident': 6,
    'war pick': 8,
    'light hammer': 4,
    'mace': 6,
    'war hammer': 8,
    'quaterstaff': 6,
    'morningstar': 8,
    'whip': 4,
    'claws': 8,
    'bite': 10
};

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
    
    let modal = $("#result");
    // does this work???
    modal.onclick = function () {
        modal.style.display = "none";
    }
    modal.append('<div id="OUT_battles"></div>')
    modal.append('<div id="OUT_rounds"></div>')
    modal.append('<div id="OUT_prediction"></div>')
    modal.append('<div id="OUT_notes"></div>')
    modal.append('<div id="OUT_team"></div>')
    modal.append('<div id="OUT_combattant"></div>')
    //$("#OUT_battles").html("");
    //$("#OUT_rounds").html("");
    //$("#OUT_prediction").html("");
    //$("#OUT_notes").html("");
    //$("#OUT_team").html("");
    //$("#OUT_combattant").html("");
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
    c = "<table class=res><thead><tr>" +
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

function figureAtkParams() {
    var w = $("#weapon").val();
    var th = $("#attack_hit").val();
    var dMod = $("#attack_dmgmod").val();
    var dice = armory[w];

    if (dice) {
        $("#attack_dicedmg").val(dice);
        $("#attack_dicedmg").prop("disabled", true);
    } else {
        $("#attack_dicedmg").prop("disabled", false);
        dice = $("#attack_dicedmg").val();
    }

    // if there's a value in the To Hit field, they must want that one to be used, so we will leave it alone.
    if (th == "") {
        // call method to figure to hit from st or dx (should add... somthing to indicate which one... slapdash for the moment)
        // getToHit(); // for a later implementation
        th = 0;
    }

    if (dMod == "") {
        dMod = 0;
    }

    var r = w + ", " + th + ", " + dMod + ", " + dice;
    $('#aParams').text("[" + r + "]");
    // call method to figure Damage modifier for a later implementation
}

function clearWeapons() {
    $("#weapon").val("");
}

function weaponDice() {
    var w = $("#weapon").val();
    for (var arm in armory) {
        if (arm == w) {
            $("#attack_dicedmg").val(armory[w]);
            return
        }
    }
}

// for a later implementation
function getToHit() {
    //get st score...for now. worry about dx melee later
    //calculate modifier
}

function queueAttack() {
    // move new attack parameter to attack list
    var c = '';
    if ($("#attacks").text().length > 1) {
        c = ','
    }
    $("#attacks").append(c + $("#aParams").text());
}

function saveAttack() {
    // move attack list to attack parameters field in custom combatant
    var s = '[' + $("#attacks").text() + ']';
    $("#attack_parameters").val(s);
}

function clearAttacks() {
    // clears the attack queue
    $("#attacks").text("");
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

// is called after simulation is run (prett sure anyways)
//function give_lineup_results(result) {
//    /// accepts 2 lists/dictionaries/arrays (not sure), one of combatants and their alignment, one of the unique alignments
//    Plotly.newPlot('lineup_graph', result.sides, { title: 'HP per side (the 2nd crudest metric of balance)' }); // xp may be a better metric as CR is a little abstract

//    // create empty table in lineup_side
//    $('#lineup_side').html('<table style="width: 100%"><thead><tr><th>Name</th></tr></thead><tbody></tbody></table>');
//    $('#lineup_code').html(JSON.stringify(lineup));
//    var sides = result.sides[0].labels;
//    // Add 'other' as team option
//    if (!sides.includes('other')) { sides.push('other'); }
//    sides.forEach(function (side) {
//        $('#lineup_side thead tr').append('<th>' + side + '</th>');
//    });
//    result.combatants.forEach(function (combatant, index) {
//        // add new row to table
//        $('#lineup_side tbody').append('<tr></tr>');
//        // add combattant to bottom/last row of table
//        $('#lineup_side tr:last').append('<td>' + combatant.name + ' <span class="kill_me" onclick="removeCombattant(' + index + ')"><i class="far fa-trash"></i></span></td>');
//        // add team selection radio buttons for each available team
//        sides.forEach(function (side) {
//            var clean = combatant.name.split(' #')[0] + 'x'.repeat(parseInt(combatant.name.split(' #')[1]));
//            $('#lineup_side tr:last').append('<td><input type="radio" name="' + clean + '" value="' + side + '" class="combatant_side" data-fullname="' + combatant.name + '" ></td>');
//            $(':radio[name="' + clean + '"][value="' + combatant.side + '"]').prop("checked", true);
//        });
//        $('.combatant_side').change(function () {
//            if ($(this).prop("checked", true)) {
//                for (var i = 0; i < lineup.length; i++) {
//                    if (!!lineup[i].sub) { //string
//                        if (lineup[i] == $(this).attr('data-fullname')) {
//                            lineup[i] = { base: $(this).attr('data-fullname'), alignment: $(this).attr('value'), name: $(this).attr('data-fullname') }
//                        }
//                    } else { // dict.
//                        if (lineup[i]['name'] == $(this).attr('data-fullname')) {
//                            lineup[i]['alignment'] = $(this).attr('value');
//                        }
//                    }
//                }
//            }
//            update_lineup();
//        });
//    });
//}

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
    /// doing a look up by name of each combatant. Returns an array (2 arrays?) that contain name and alignment, and another of each alignment involved 
    // we may be able to skip a lot of this if we always only have 2 teams to assign members to (esp if we don't care about alignments)
    //fix_doubles();

    display_rosters(lineup);
    // should make a dict {name: team: number:} for each combatant in the linup.
    // make use of fix_doubles() to ensure that nothing bad happens when the user adds a creature that's already been added
    // ie : ape, ant, ape


    // Then... we just need to add the new member to the lineup, change the give_lineup_results function to run the names in lineup
    // and create a radio box for each combatant (god help us for large armies)... This is where preselecting the team team will save a lot of time and effort for the user
    //var proportions = {}; // did nothing...??

    //$.ajax({
    //    url: "ajax_lineup",
    //    type: 'POST',
    //    dataType: 'json',
    //    data: JSON.stringify(lineup),
    //    success: give_lineup_results,
    //    error: function () {
    //        $("#status").html('<div class="alert alert-danger" role="alert"><i class="far fa-skull-crossbones"></i> Oh Snap. Nothing back.</div>');
    //    }
    //});
}

$(document).ready(function () {
    initial();
}); 