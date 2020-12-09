
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

function showModal() {
    $("#myModal").modal("toggle");
}
