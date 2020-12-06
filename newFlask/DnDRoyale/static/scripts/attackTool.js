function figureAtkParams(opt) {
    // the selected weapon from list
    var w = $("#weapon").val();
    var th = $("#attack_hit").val();
    var dMod = $("#attack_dmgmod").val();
    var dice = $('[value="'+ w +'"]').attr('data-die')

    if (dice) {
        $("#attack_dicedmg").val(dice);
        $("#attack_dicedmg").prop("disabled", true);
    } else {
        // custom weapon, take user input
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

    var r = '"' + w + '", ' + th + ", " + dMod + ", " + dice;
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
