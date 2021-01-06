//window.onload = function () {
//    updateGraph();
//}

function updateGraph(redPower, bluePower) {
    // get total value of 'power' from each team

    if (redPower + bluePower != 0) { // check if there's values to display

        var chart = new CanvasJS.Chart("chartContainer",
            {
                //title: {
                //    text: "Power Comparison"
                //},
                height: 50,
                axisY: {
                    interval: 10, 
                    suffix: "%",
                },
                toolTip: {
                    shared: true,
                },
                data: [
                    {
                        type: "stackedBar100",
                        showInLegend: false, 
                        name: "Red Team",
                        color: "red",
                        dataPoints: [
                            { y: redPower, label: "XP" },
                        ]
                    },
                    {
                        type: "stackedBar100",
                        showInLegend: false, 
                        name: "Blue Team",
                        color: "blue",
                        dataPoints: [
                            { y: bluePower, label: "XP" }
                        ]
                    },

                ]

            });
    chart.render();
    }
}