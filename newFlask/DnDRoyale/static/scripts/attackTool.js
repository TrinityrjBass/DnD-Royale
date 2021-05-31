function figureAtkParams(opt) {
    // the selected weapon from list
    var w = $("#weapon").val();
    var th = $("#attack_hit").val();
    var dMod = $("#attack_dmgmod").val();
    var dice = $('[value="' + w + '"]').attr('data-die');
    var dmgtype = $('#attack_dmgtype').val();
    var magical = $("#magicalAttack").prop("checked");
    var isMagical = ', "isMagical": ' + magical;

    if (opt == 'weapon') {
        dmgtype = getDmgType(w);
        $('#attack_dmgtype').val(dmgtype);
    }

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
        // call method to figure to hit from st or dx (should add... something to indicate which one... slapdash for the moment)
        // getToHit(); // for a later implementation
        th = 0;
    }

    if (dMod == "") {
        dMod = 0;
    }

    if (dice == "") {
        dice = 0;
    }

    var r = '"name": ' + w + '", "attack": ' + th + ', "damage modifier": ' + dMod + ', "damage": ' + dice + ', "type": ' + '"' + dmgtype + '"' + isMagical ;
    $('#aParams').text("{" + r + "}");
    // call method to figure Damage modifier for a later implementation
}

function getDmgType(w) {
    switch (w) {
        case "dagger":
        case "javelin":
        case "spear":
        case "crossbow":
        case "dart":
        case "short bow":
        case "lance":
        case "morningstar":
        case "pike":
        case "rapier":
        case "short sword":
        case "war pick":
        case "blowgun":
        case "hand crossbow":
        case "heavy crossbow":
        case "longbow":
        case "trident":
        case "bite":
            return "piercing";
        case "club":
        case "great club":
        case "maul":
        case "mace":
        case "light hammer":
        case "quarterstaff":
        case "sling":
        case "flail":
        case "warhammer":
        case "tentacle":
        case "hooves":
        case "fist":
        case "slam":
            return "bludgeoning"
        case "hand axe":
        case "axe":
        case "bastard sword":
        case "sickle":
        case "battle axe (1H)":
        case "battle axe (2H)":
        case "glaive":
        case "great axe":
        case "great sword":
        case "long sword":
        case "scimitar":
        case "whip":
        case "claws":
            return "slashing"
        default:
            return "";
    }
}

function clearOption(id) {
    $("#"+id).val("");
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

    // If it's a custom weapon AND there's no value, send alert.
    if (!$("#attack_dicedmg").is(":disabled") && $("#attack_dicedmg").val() == "") {
        alert("Attack Die field must not be empty. Please enter a number that represents the dice you would like to use for the Damage dice. For example a 4 represents a 4 sided die. Multiple dice are allowed, simply separate the numbers with a comma.")
    }
    else {
        var c = '';
        if ($("#attacks").text().length > 1) {
            c = ','
        }
        $("#attacks").append(c + $("#aParams").text());
    }

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
