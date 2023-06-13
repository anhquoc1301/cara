(function (global) {
  "use strict";
  var init = function(){
	var c_b = document.querySelector('#chartist-bar');
	c_b && new Chartist.Bar(c_b, {
		labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
		series: [
		    {value: [5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8], className: 'ct-series-a ct-stroke-4', meta: 'Facebook'},
		    {value: [3, 2, 9, 5, 4, 6, 4, 6, 7, 8, 7, 4], className: 'ct-series-g ct-stroke-4', meta: 'Twitter'}
		]
	},{
		seriesBarDistance: 8,
		plugins: [
		    Chartist.plugins.tooltip(),
	    	Chartist.plugins.animate()
		]
	});

  }

  global.chartist = {init: init};

})(this);
