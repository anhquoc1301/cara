(function (global, theme) {
	"use strict";
  Chart.defaults.global.defaultColor = 'rgba(130,140,155,0.1)';
  Chart.defaults.global.defaultFontColor = 'rgba(130,140,155,0.65)';
  Chart.defaults.scale.gridLines.color = 
  Chart.defaults.scale.gridLines.zeroLineColor = 'rgba(130,140,155,0.05)';
  Chart.defaults.global.tooltips.cornerRadius = 3;
  Chart.defaults.global.maintainAspectRatio = false;
  
  var charted = function( target ) {
    return new RegExp('(\\s|^)' + 'chartjs-render-monitor' + '(\\s|$)').test(target.className);
  }

  var init = function(){
    var d_b = {
        labels: Utils.months({count: 7, section: 3}),
        datasets: [
            {
                label: 'Sales',
                data: Utils.numbers({count: 7, decimals: 2}),
                fill: true,
                backgroundColor: Utils.color(theme.color.info, 1),
                borderColor: theme.color.info,
                borderWidth: 1
            }
        ]
    };
    var ctx = document.getElementById('chart-bar');
    if( ctx && !charted(ctx) ){
      new Chart(ctx.getContext('2d'),
        {
          type: 'bar',
          data: d_b,
          options: {
            scales: {
              xAxes: [{
                barPercentage: 0.5,
                categoryPercentage: 0.5,
              }]
            }
          }
        }
      );
    }
  }

  // for ajax to init again
  global.chartjs = {init: init};

})(this, theme);
