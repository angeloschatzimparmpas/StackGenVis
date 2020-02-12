<template>
    <div>
      <b-row class="md-3">
        <b-col cols="12">
          <div id="overview"></div>
        </b-col>
        <!--
        <b-col cols="4"> 
          <div id="encodings"></div>
        </b-col>-->
      </b-row>
    </div>
</template>

<script>
import { EventBus } from '../main.js'

export default {
  name: 'Parameters',
  data () {
    return {
      WH: [],
      storeActiveModels: [],
      allActiveKNN: [],
      allActiveRF: [],
      storeParameters: [],
      FlagKNN: 0,
      FlagRF: 0,
      KNNModels: 576, //KNN models
    }
  },
  methods: {
    reset () {
      setTimeout(() => {
         var svg = d3.select("#overview");
        svg.selectAll("*").remove();
      }, 50);
    },
    /////////////////////////////////////////////////////////
/////////////// The Radar Chart Function ////////////////
/////////////// Written by Nadieh Bremer ////////////////
////////////////// VisualCinnamon.com ///////////////////
/////////// Inspired by the code of alangrafu ///////////
/////////////////////////////////////////////////////////
	
 RadarChart(id, data, options) {
	var cfg = {
	 w: 600,				//Width of the circle
	 h: 600,				//Height of the circle
	 margin: {top: 20, right: 20, bottom: 20, left: 20}, //The margins of the SVG
	 levels: 3,				//How many levels or inner circles should there be drawn
	 maxValue: 0, 			//What is the value that the biggest circle will represent
	 labelFactor: 1.25, 	//How much farther than the radius of the outer circle should the labels be placed
	 wrapWidth: 60, 		//The number of pixels after which a label needs to be given a new line
	 opacityArea: 0.35, 	//The opacity of the area of the blob
	 dotRadius: 4, 			//The size of the colored circles of each blog
	 opacityCircles: 0.1, 	//The opacity of the circles of each blob
	 strokeWidth: 2, 		//The width of the stroke around each blob
	 roundStrokes: false,	//If true the area and stroke will follow a round path (cardinal-closed)
	 color: d3.scale.category10()	//Color function
	};
	
	//Put all of the options into a variable called cfg
	if('undefined' !== typeof options){
	  for(var i in options){
		if('undefined' !== typeof options[i]){ cfg[i] = options[i]; }
	  }//for i
	}//if
	
	//If the supplied maxValue is smaller than the actual one, replace by the max in the data
	var maxValue = Math.max(cfg.maxValue, d3.max(data, function(i){return d3.max(i.map(function(o){return o.value;}))}));
		
	var allAxis = (data[0].map(function(i, j){return i.axis})),	//Names of each axis
		total = allAxis.length,					//The number of different axes
		radius = Math.min(cfg.w/2, cfg.h/2), 	//Radius of the outermost circle
		Format = d3.format('%'),			 	//Percentage formatting
		angleSlice = Math.PI * 2 / total;		//The width in radians of each "slice"
	
	//Scale for the radius
	var rScale = d3.scale.linear()
		.range([0, radius])
		.domain([0, maxValue]);
		
	/////////////////////////////////////////////////////////
	//////////// Create the container SVG and g /////////////
	/////////////////////////////////////////////////////////

	//Remove whatever chart with the same id/class was present before
	d3.select(id).select("svg").remove();
	
	//Initiate the radar chart SVG
	var svg = d3.select(id).append("svg")
			.attr("width",  cfg.w + cfg.margin.left + cfg.margin.right)
			.attr("height", cfg.h + cfg.margin.top + cfg.margin.bottom)
			.attr("class", "radar"+id);
	//Append a g element		
	var g = svg.append("g")
			.attr("transform", "translate(" + (cfg.w/2 + cfg.margin.left) + "," + (cfg.h/2 + cfg.margin.top) + ")");
	
	/////////////////////////////////////////////////////////
	////////// Glow filter for some extra pizzazz ///////////
	/////////////////////////////////////////////////////////
	
	//Filter for the outside glow
	var filter = g.append('defs').append('filter').attr('id','glow'),
		feGaussianBlur = filter.append('feGaussianBlur').attr('stdDeviation','2.5').attr('result','coloredBlur'),
		feMerge = filter.append('feMerge'),
		feMergeNode_1 = feMerge.append('feMergeNode').attr('in','coloredBlur'),
		feMergeNode_2 = feMerge.append('feMergeNode').attr('in','SourceGraphic');

	/////////////////////////////////////////////////////////
	/////////////// Draw the Circular grid //////////////////
	/////////////////////////////////////////////////////////
	
	//Wrapper for the grid & axes
	var axisGrid = g.append("g").attr("class", "axisWrapper");
	
	//Draw the background circles
	axisGrid.selectAll(".levels")
	   .data(d3.range(1,(cfg.levels+1)).reverse())
	   .enter()
		.append("circle")
		.attr("class", "gridCircle")
		.attr("r", function(d, i){return radius/cfg.levels*d;})
		.style("fill", "#CDCDCD")
		.style("stroke", "#CDCDCD")
		.style("fill-opacity", cfg.opacityCircles)
		.style("filter" , "url(#glow)");

	//Text indicating at what % each level is
	axisGrid.selectAll(".axisLabel")
	   .data(d3.range(1,(cfg.levels+1)).reverse())
	   .enter().append("text")
	   .attr("class", "axisLabel")
	   .attr("x", 4)
	   .attr("y", function(d){return -d*radius/cfg.levels;})
	   .attr("dy", "0.4em")
	   .style("font-size", "10px")
	   .attr("fill", "#737373")
	   .text(function(d,i) { return Format(maxValue * d/cfg.levels); });

	/////////////////////////////////////////////////////////
	//////////////////// Draw the axes //////////////////////
	/////////////////////////////////////////////////////////
	
	//Create the straight lines radiating outward from the center
	var axis = axisGrid.selectAll(".axis")
		.data(allAxis)
		.enter()
		.append("g")
		.attr("class", "axis");
	//Append the lines
	axis.append("line")
		.attr("x1", 0)
		.attr("y1", 0)
		.attr("x2", function(d, i){ return rScale(maxValue*1.1) * Math.cos(angleSlice*i - Math.PI/2); })
		.attr("y2", function(d, i){ return rScale(maxValue*1.1) * Math.sin(angleSlice*i - Math.PI/2); })
		.attr("class", "line")
		.style("stroke", "white")
		.style("stroke-width", "2px");

	//Append the labels at each axis
	axis.append("text")
		.attr("class", "legend")
		.style("font-size", "11px")
		.attr("text-anchor", "middle")
		.attr("dy", "0.35em")
		.attr("x", function(d, i){ return rScale(maxValue * cfg.labelFactor) * Math.cos(angleSlice*i - Math.PI/2); })
		.attr("y", function(d, i){ return rScale(maxValue * cfg.labelFactor) * Math.sin(angleSlice*i - Math.PI/2); })
		.text(function(d){return d})
		.call(wrap, cfg.wrapWidth);

	/////////////////////////////////////////////////////////
	///////////// Draw the radar chart blobs ////////////////
	/////////////////////////////////////////////////////////
	
	//The radial line function
	var radarLine = d3.svg.line.radial()
		.interpolate("linear-closed")
		.radius(function(d) { return rScale(d.value); })
		.angle(function(d,i) {	return i*angleSlice; });
		
	if(cfg.roundStrokes) {
		radarLine.interpolate("cardinal-closed");
	}
				
	//Create a wrapper for the blobs	
	var blobWrapper = g.selectAll(".radarWrapper")
		.data(data)
		.enter().append("g")
		.attr("class", "radarWrapper");
			
	//Append the backgrounds	
	blobWrapper
		.append("path")
		.attr("class", "radarArea")
		.attr("d", function(d,i) { return radarLine(d); })
		.style("fill", function(d,i) { return cfg.color(i); })
		.style("fill-opacity", cfg.opacityArea)
		.on('mouseover', function (d,i){
			//Dim all blobs
			d3.selectAll(".radarArea")
				.transition().duration(200)
				.style("fill-opacity", 0.1); 
			//Bring back the hovered over blob
			d3.select(this)
				.transition().duration(200)
				.style("fill-opacity", 0.7);	
		})
		.on('mouseout', function(){
			//Bring back all blobs
			d3.selectAll(".radarArea")
				.transition().duration(200)
				.style("fill-opacity", cfg.opacityArea);
		});
		
	//Create the outlines	
	blobWrapper.append("path")
		.attr("class", "radarStroke")
		.attr("d", function(d,i) { return radarLine(d); })
		.style("stroke-width", cfg.strokeWidth + "px")
		.style("stroke", function(d,i) { return cfg.color(i); })
		.style("fill", "none")
		.style("filter" , "url(#glow)");		
	
	//Append the circles
	blobWrapper.selectAll(".radarCircle")
		.data(function(d,i) { return d; })
		.enter().append("circle")
		.attr("class", "radarCircle")
		.attr("r", cfg.dotRadius)
		.attr("cx", function(d,i){ return rScale(d.value) * Math.cos(angleSlice*i - Math.PI/2); })
		.attr("cy", function(d,i){ return rScale(d.value) * Math.sin(angleSlice*i - Math.PI/2); })
		.style("fill", function(d,i,j) { return cfg.color(j); })
		.style("fill-opacity", 0.8);

	/////////////////////////////////////////////////////////
	//////// Append invisible circles for tooltip ///////////
	/////////////////////////////////////////////////////////
	
	//Wrapper for the invisible circles on top
	var blobCircleWrapper = g.selectAll(".radarCircleWrapper")
		.data(data)
		.enter().append("g")
		.attr("class", "radarCircleWrapper");
		
	//Append a set of invisible circles on top for the mouseover pop-up
	blobCircleWrapper.selectAll(".radarInvisibleCircle")
		.data(function(d,i) { return d; })
		.enter().append("circle")
		.attr("class", "radarInvisibleCircle")
		.attr("r", cfg.dotRadius*1.5)
		.attr("cx", function(d,i){ return rScale(d.value) * Math.cos(angleSlice*i - Math.PI/2); })
		.attr("cy", function(d,i){ return rScale(d.value) * Math.sin(angleSlice*i - Math.PI/2); })
		.style("fill", "none")
		.style("pointer-events", "all")
		.on("mouseover", function(d,i) {
			newX =  parseFloat(d3.select(this).attr('cx')) - 10;
			newY =  parseFloat(d3.select(this).attr('cy')) - 10;
					
			tooltip
				.attr('x', newX)
				.attr('y', newY)
				.text(Format(d.value))
				.transition().duration(200)
				.style('opacity', 1);
		})
		.on("mouseout", function(){
			tooltip.transition().duration(200)
				.style("opacity", 0);
		});
		
	//Set up the small tooltip for when you hover over a circle
	var tooltip = g.append("text")
		.attr("class", "tooltip")
		.style("opacity", 0);
	
	/////////////////////////////////////////////////////////
	/////////////////// Helper Function /////////////////////
	/////////////////////////////////////////////////////////

	//Taken from http://bl.ocks.org/mbostock/7555321
	//Wraps SVG text	
	function wrap(text, width) {
	  text.each(function() {
		var text = d3.select(this),
			words = text.text().split(/\s+/).reverse(),
			word,
			line = [],
			lineNumber = 0,
			lineHeight = 1.4, // ems
			y = text.attr("y"),
			x = text.attr("x"),
			dy = parseFloat(text.attr("dy")),
			tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
			
		while (word = words.pop()) {
		  line.push(word);
		  tspan.text(line.join(" "));
		  if (tspan.node().getComputedTextLength() > width) {
			line.pop();
			tspan.text(line.join(" "));
			line = [word];
			tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
		  }
		}
	  });
	}//wrap	
	
},
    overview() {
       /* Radar chart design created by Nadieh Bremer - VisualCinnamon.com */
      
			////////////////////////////////////////////////////////////// 
			//////////////////////// Set-Up ////////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var margin = {top: 50, right: 50, bottom: 50, left: 50},
				width = Math.min(420, window.innerWidth - 10) - margin.left - margin.right,
				height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);
					
			////////////////////////////////////////////////////////////// 
			////////////////////////// Data ////////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var data = [
					  [
						{axis:"KNN",value:1},
            {axis:"RF",value:0.30},
            {axis:"Alg3",value:0.55},
            {axis:"Alg4",value:0.68},
            {axis:"Alg5",value:0.22},
            {axis:"Alg6",value:0.28},
            {axis:"Alg7",value:0.55},
            {axis:"Alg9",value:0.68},
            {axis:"Alg9",value:0.22},
            {axis:"Alg10",value:0.28},
            ],[
						{axis:"KNN",value:0.05},
            {axis:"RF",value:0.18},
            {axis:"Alg3",value:0.25},
            {axis:"Alg4",value:0.28},
            {axis:"Alg5",value:0.22},
            {axis:"Alg6",value:0.18},
            {axis:"Alg7",value:0.45},
            {axis:"Alg9",value:0.18},
            {axis:"Alg9",value:0.22},
            {axis:"Alg10",value:0.18},
					  ],
					];
			////////////////////////////////////////////////////////////// 
			//////////////////// Draw the Chart ////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var color = d3.scale.ordinal()
				.range(["#EDC951","#CC333F","#00A0B0"]);
				
			var radarChartOptions = {
			  w: width,
			  h: height,
			  margin: margin,
			  maxValue: 0.5,
			  levels: 5,
			  roundStrokes: true,
			  color: color
			};
			//Call function to draw the Radar chart
			this.RadarChart("#overview", data, radarChartOptions);
    },
    draw () {
      // Clear Heatmap first
      var svg = d3.select("#overview");
      svg.selectAll("*").remove();

      var widthinter = this.WH[0]*2 // interactive visualization
      var heightinter = this.WH[1]*1.23 // interactive visualization
      var margin = 0,
        width = widthinter,
        height = heightinter,
        maxBarHeight = height / 2 - (margin + 70);
      var innerRadius = 0.1 * maxBarHeight; // innermost circle

      var svg = d3.select('#overview')
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("class", "chart")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

      var defs = svg.append("defs");

      var gradients = defs
        .append("linearGradient")
        .attr("id", "gradient-chart-area")
        .attr("x1", "50%")
        .attr("y1", "0%")
        .attr("x2", "50%")
        .attr("y2", "100%")
        .attr("spreadMethod", "pad");

      gradients.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", "#EDF0F0")
        .attr("stop-opacity", 1);

      gradients.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", "#ACB7BE")
        .attr("stop-opacity", 1);

      gradients = defs
        .append("linearGradient")
        .attr("id", "gradient-questions")
        .attr("x1", "50%")
        .attr("y1", "0%")
        .attr("x2", "50%")
        .attr("y2", "100%")
        .attr("spreadMethod", "pad");

      gradients.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", "#F6F8F9")
        .attr("stop-opacity", 1);

      gradients.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", "#D4DAE0")
        .attr("stop-opacity", 1);

      gradients = defs
        .append("radialGradient")
        .attr("id", "gradient-bars")
        .attr("gradientUnits", "userSpaceOnUse")
        .attr("cx", "0")
        .attr("cy", "0")
        .attr("r", maxBarHeight)
        .attr("spreadMethod", "pad");

      gradients.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", "#F3D5AA");

      gradients.append("stop")
        .attr("offset", "50%")
        .attr("stop-color", "#F4A636");

      gradients.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", "#AF4427");

      gradients = defs
        .append("linearGradient")
        .attr("id", "gradient-categorization")
        .attr("x1", "0%")
        .attr("y1", "50%")
        .attr("x2", "100%")
        .attr("y2", "50%")
        .attr("spreadMethod", "pad");

      gradients.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", "#8dd3c7")
        .attr("stop-opacity", 1);

      gradients.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", "#8da0cb")
        .attr("stop-opacity", 1);

      svg.append("circle")
        .attr("r", maxBarHeight + 30)
        .classed("category-circle", true);

      svg.append("circle")
        .attr("r", maxBarHeight + 15)
        .classed("question-circle", true);

      svg.append("circle")
        .attr("r", maxBarHeight)
        .classed("chart-area-circle", true);

      svg.append("circle")
        .attr("r", innerRadius)
        .classed("center-circle", true);

        var n_neighbors = 0
        var metric = 0
        var algorithm = 0
        var weight = 0
        var n_estimators = 0
        var criterion = 0

        if (this.FlagKNN == 0 && this.FlagRF == 0) {
          this.storeActiveModels = []
          this.allActiveKNN = []
          this.allActiveRF = []
        }

        if (this.storeActiveModels.length != 0) {
          var countkNNRelated = []
          var countRFRelated = []
          for (let i = 0; i < this.storeActiveModels.length; i++) {
            if (this.storeActiveModels[i] < this.KNNModels) {
              countkNNRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
            } else {
              countRFRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
            }
          }
          if (this.storeActiveModels[0] < this.KNNModels) {
            this.allActiveKNN = countkNNRelated.slice()
          } else {
            this.allActiveRF = countRFRelated.slice()
          }

          n_neighbors = ([... new Set(this.allActiveKNN.map(data => data.n_neighbors))].length / 25) * 100
          metric = ([... new Set(this.allActiveKNN.map(data => data.metric))].length / 4) * 100
          algorithm = ([... new Set(this.allActiveKNN.map(data => data.algorithm))].length / 3) * 100
          weight = ([... new Set(this.allActiveKNN.map(data => data.weight))].length / 2) * 100
          n_estimators = ([... new Set(this.allActiveRF.map(data => data.n_estimators))].length / 80) * 100
          criterion = ([... new Set(this.allActiveRF.map(data => data.criterion))].length / 2) * 100
        }

        if (this.FlagKNN == 1 && this.allActiveKNN.length == 0) {
          n_neighbors = 100
          metric = 100
          algorithm = 100
          weight = 100
        }

        if (this.FlagRF == 1 && this.allActiveRF.length == 0) {
          n_estimators = 100
          criterion = 100
        }

        var data = [
            { algorithm: 'RF', parameter: 'n_estimators', percentage: n_estimators },
            { algorithm: 'RF', parameter: 'criterion', percentage: criterion },
            { algorithm: 'KNN', parameter: 'n_neighbors', percentage: n_neighbors },
            { algorithm: 'KNN', parameter: 'metric', percentage: metric },
            { algorithm: 'KNN', parameter: 'algorithm', percentage: algorithm },
            { algorithm: 'KNN', parameter: 'weight', percentage: weight },
        ];

        var cats = data.map(function(d, i) {
          return d.algorithm;
        });

        var catCounts = {};
        for (var i = 0; i < cats.length; i++) {
          var num = cats[i];
          catCounts[num] = catCounts[num] ? catCounts[num] + 1 : 1;
        }
        // remove dupes (not exactly the fastest)
        cats = cats.filter(function(v, i) {
          return cats.indexOf(v) == i;
        });
        var numCatBars = cats.length;

        var angle = 0,
          rotate = 0;

        data.forEach(function(d, i) {
          // bars start and end angles
          d.startAngle = angle;
          angle += (2 * Math.PI) / numCatBars / catCounts[d.algorithm];
          d.endAngle = angle;

          // y axis minor lines (i.e. questions) rotation
          d.rotate = rotate;
          rotate += 360 / numCatBars / catCounts[d.algorithm];
        });

        // category_label
        var arc_category_label = d3.svg.arc()
          .startAngle(function(d, i) {
            return (i * 2 * Math.PI) / numCatBars;
          })
          .endAngle(function(d, i) {
            return ((i + 1) * 2 * Math.PI) / numCatBars;
          })
          .innerRadius(maxBarHeight + 32)
          .outerRadius(maxBarHeight + 0);

        var category_text = svg.selectAll("path.category_label_arc")
          .data(cats)
          .enter().append("path")
          .classed("category-label-arc", true)
          .attr("id", function(d, i) {
            return "category_label_" + i;
          }) //Give each slice a unique ID
          .attr("fill", "none")
          .attr("d", arc_category_label);

        category_text.each(function(d, i) {
          //Search pattern for everything between the start and the first capital L
          var firstArcSection = /(^.+?)L/;

          //Grab everything up to the first Line statement
          var newArc = firstArcSection.exec(d3.select(this).attr("d"))[1];
          //Replace all the commas so that IE can handle it
          newArc = newArc.replace(/,/g, " ");

          //If the whole bar lies beyond a quarter of a circle (90 degrees or pi/2)
          // and less than 270 degrees or 3 * pi/2, flip the end and start position
          var startAngle = (i * 2 * Math.PI) / numCatBars,
            endAngle = ((i + 1) * 2 * Math.PI) / numCatBars;

          if (startAngle > Math.PI / 2 && startAngle < 3 * Math.PI / 2 && endAngle > Math.PI / 2 && endAngle < 3 * Math.PI / 2) {
            var startLoc = /M(.*?)A/, //Everything between the capital M and first capital A
              middleLoc = /A(.*?)0 0 1/, //Everything between the capital A and 0 0 1
              endLoc = /0 0 1 (.*?)$/; //Everything between the 0 0 1 and the end of the string (denoted by $)
            //Flip the direction of the arc by switching the start and end point (and sweep flag)
            var newStart = endLoc.exec(newArc)[1];
            var newEnd = startLoc.exec(newArc)[1];
            var middleSec = middleLoc.exec(newArc)[1];

            //Build up the new arc notation, set the sweep-flag to 0
            newArc = "M" + newStart + "A" + middleSec + "0 0 0 " + newEnd;
          } //if

          //Create a new invisible arc that the text can flow along
          /*                            svg.append("path")
            .attr("class", "hiddenDonutArcs")
            .attr("id", "category_label_"+i)
            .attr("d", newArc)
            .style("fill", "none");*/

          // modifying existing arc instead
          d3.select(this).attr("d", newArc);
        });

        svg.selectAll(".category-label-text")
          .data(cats)
          .enter().append("text")
          .attr("class", "category-label-text")
          //.attr("x", 0)   //Move the text from the start angle of the arc
          //Move the labels below the arcs for those slices with an end angle greater than 90 degrees
          .attr("dy", function(d, i) {
            var startAngle = (i * 2 * Math.PI) / numCatBars,
              endAngle = ((i + 1) * 2 * Math.PI) / numCatBars;
            return (startAngle > Math.PI / 2 && startAngle < 3 * Math.PI / 2 && endAngle > Math.PI / 2 && endAngle < 3 * Math.PI / 2 ? -4 : 14);
          })
          .append("textPath")
          .attr("startOffset", "50%")
          .style("text-anchor", "middle")
          .attr("xlink:href", function(d, i) {
            return "#category_label_" + i;
          })
          .text(function(d) {
            return d;
          });

        // parameter
        var arc_parameter = d3.svg.arc()
          .startAngle(function(d, i) {
            return d.startAngle;
          })
          .endAngle(function(d, i) {
            return d.endAngle;
          })
          //.innerRadius(maxBarHeight + 2)
          .outerRadius(maxBarHeight - 9);

        var question_text = svg.selectAll("path.parameter_arc")
          .data(data)
          .enter().append("path")
          .classed("question-label-arc", true)
          .attr("id", function(d, i) {
            return "parameter_" + i;
          }) //Give each slice a unique ID
          .attr("fill", "none")
          .attr("d", arc_parameter);

        question_text.each(function(d, i) {
          //Search pattern for everything between the start and the first capital L
          var firstArcSection = /(^.+?)L/;

          //Grab everything up to the first Line statement
          var newArc = firstArcSection.exec(d3.select(this).attr("d"))[1];
          //Replace all the commas so that IE can handle it
          newArc = newArc.replace(/,/g, " ");

          //If the end angle lies beyond a quarter of a circle (90 degrees or pi/2)
          //flip the end and start position
          if (d.startAngle > Math.PI / 2 && d.startAngle < 3 * Math.PI / 2 && d.endAngle > Math.PI / 2 && d.endAngle < 3 * Math.PI / 2) {
            var startLoc = /M(.*?)A/, //Everything between the capital M and first capital A
              middleLoc = /A(.*?)0 0 1/, //Everything between the capital A and 0 0 1
              endLoc = /0 0 1 (.*?)$/; //Everything between the 0 0 1 and the end of the string (denoted by $)
            //Flip the direction of the arc by switching the start and end point (and sweep flag)
            var newStart = endLoc.exec(newArc)[1];
            var newEnd = startLoc.exec(newArc)[1];
            var middleSec = middleLoc.exec(newArc)[1];

            //Build up the new arc notation, set the sweep-flag to 0
            newArc = "M" + newStart + "A" + middleSec + "0 0 0 " + newEnd;
          } //if

          //Create a new invisible arc that the text can flow along
          /*                            svg.append("path")
            .attr("class", "hiddenDonutArcs")
            .attr("id", "parameter_"+i)
            .attr("d", newArc)
            .style("fill", "none");*/

          // modifying existing arc instead
          d3.select(this).attr("d", newArc);
        });

        question_text = svg.selectAll(".question-label-text")
          .data(data)
          .enter().append("text")
          .attr("class", "question-label-text")
          //.attr("x", 0)   //Move the text from the start angle of the arc
          //.attr("y", 0)
          //Move the labels below the arcs for those slices with an end angle greater than 90 degrees
          /*                        .attr("dy", function (d, i) {
            return (d.startAngle > Math.PI / 2 && d.startAngle < 3 * Math.PI / 2 && d.endAngle > Math.PI / 2 && d.endAngle < 3 * Math.PI / 2 ? 10 : -10);
            })*/
          .append("textPath")
          //.attr("startOffset", "50%")
          //.style("text-anchor", "middle")
          //.style("dominant-baseline", "central")
          .style('font-size', '7px')
          .style('font-family', 'sans-serif')
          .attr("xlink:href", function(d, i) {
            return "#parameter_" + i;
          })
          .text(function(d) {
            return d.parameter.toUpperCase();
          })
          .call(wrapTextOnArc, maxBarHeight);

        // adjust dy (labels vertical start) based on number of lines (i.e. tspans)
        question_text.each(function(d, i) {
          var textPath = d3.select(this)[0][0],
            tspanCount = textPath.childNodes.length;

          if (d.startAngle > Math.PI / 2 && d.startAngle < 3 * Math.PI / 2 && d.endAngle > Math.PI / 2 && d.endAngle < 3 * Math.PI / 2) {
            // set baseline for one line and adjust if greater than one line
            d3.select(textPath.childNodes[0]).attr("dy", 3 + (tspanCount - 1) * -0.6 + 'em');
          } else {
            d3.select(textPath.childNodes[0]).attr("dy", -2.1 + (tspanCount - 1) * -0.6 + 'em');
          }
        });

        /* bars */
        var arc = d3.svg.arc()
          .startAngle(function(d, i) {
            return d.startAngle;
          })
          .endAngle(function(d, i) {
            return d.endAngle;
          })
          .innerRadius(innerRadius);

        var bars = svg.selectAll("path.bar")
          .data(data)
          .enter().append("path")
          .classed("bars", true)
          .each(function(d) {
            d.outerRadius = innerRadius;
          })
          .attr("d", arc);

        bars.transition().ease("elastic").duration(1000).delay(function(d, i) {
            return i * 100;
          })
          .attrTween("d", function(d, index) {
            var i = d3.interpolate(d.outerRadius, x_scale(+d.percentage));
            return function(t) {
              d.outerRadius = i(t);
              return arc(d, index);
            };
          });

        var x_scale = d3.scale.linear()
          .domain([0, 100])
          .range([innerRadius, maxBarHeight]);


        var y_scale = d3.scale.linear()
          .domain([0, 100])
          .range([-innerRadius, -maxBarHeight]);

        svg.selectAll("circle.x.minor")
          .data(y_scale.ticks(10))
          .enter().append("circle")
          .classed("gridlines minor", true)
          .attr("r", function(d) {
            return x_scale(d);
          });

        // question lines
        svg.selectAll("line.y.minor")
          .data(data)
          .enter().append("line")
          .classed("gridlines minor", true)
          .attr("y1", -innerRadius)
          .attr("y2", -maxBarHeight - 15)
          .attr("transform", function(d, i) {
            return "rotate(" + (d.rotate) + ")";
          });

        // category lines
        svg.selectAll("line.y.major")
          .data(cats)
          .enter().append("line")
          .classed("gridlines major", true)
          .attr("y1", -innerRadius)
          .attr("y2", -maxBarHeight - 100)
          .attr("transform", function(d, i) {
            return "rotate(" + (i * 360 / numCatBars) + ")";
          });


      function wrapTextOnArc(text, radius) {
      // note getComputedTextLength() doesn't work correctly for text on an arc,
      // hence, using a hidden text element for measuring text length.
      var temporaryText = d3.select('svg')
        .append("text")
        .attr("class", "temporary-text") // used to select later
        .style("font", "7px sans-serif")
        .style("opacity", 0); // hide element

      var getTextLength = function(string) {
        temporaryText.text(string);
        return temporaryText.node().getComputedTextLength();
      };

      text.each(function(d) {
        var text = d3.select(this),
          words = text.text().split(/[ \f\n\r\t\v]+/).reverse(), //Don't cut non-breaking space (\xA0), as well as the Unicode characters \u00A0 \u2028 \u2029)
          word,
          wordCount = words.length,
          line = [],
          textLength,
          lineHeight = 1.1, // ems
          x = 0,
          y = 0,
          dy = 0,
          tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em"),
          arcLength = ((d.endAngle - d.startAngle) / (2 * Math.PI)) * (2 * Math.PI * radius),
          paddedArcLength = arcLength - 16;

        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(" "));
          textLength = getTextLength(tspan.text());
          tspan.attr("x", (arcLength - textLength) / 2);

          if (textLength > paddedArcLength && line.length > 1) {
            // remove last word
            line.pop();
            tspan.text(line.join(" "));
            textLength = getTextLength(tspan.text());
            tspan.attr("x", (arcLength - textLength) / 2);

            // start new line with last word
            line = [word];
            tspan = text.append("tspan").attr("dy", lineHeight + dy + "em").text(word);
            textLength = getTextLength(tspan.text());
            tspan.attr("x", (arcLength - textLength) / 2);
          }
        }
      });

        d3.selectAll("text.temporary-text").remove()
      }
      },
      drawEncodings () {
        // Clear Heatmap first
        var svg = d3.select("#encodings");
        svg.selectAll("*").remove();

        var widthinter = this.WH[0]*0.95 // interactive visualization
        var heightinter = this.WH[1]*0.5 // interactive visualization
        /*
          // Create the SVG element and set its dimensions.
          var width  = widthinter,
              height = heightinter,
              padding = 15;

          var div = d3.select('#encodings'),
              svg = div.append('svg');

          svg.attr('width', width).attr('height', height);

          // Create the svg:defs element and the main gradient definition.
          var svgDefs = svg.append('defs');

          var mainGradient = svgDefs.append('linearGradient')
            .attr("id", "mainGradient")
            .attr("x1", "0%")
            .attr("x2", "100%")
            .attr("y1", "0%")
            .attr("y2", "100%");

          mainGradient.append("stop")
            .attr('class', 'start')
            .attr("offset", "0%")
            .attr("stop-color", "red")
            .attr("stop-opacity", 1);

          mainGradient.append("stop")
            .attr('class', 'end')
            .attr("offset", "100%")
            .attr("stop-color", "blue")
            .attr("stop-opacity", 1);

          // Use the gradient to set the shape fill, via CSS.
          svg.append('rect')
              .classed('filled', true)
              .attr('x', padding)
              .attr('y', padding)
              .attr('width', width - 2 * padding)
              .attr('height', height - 2 * padding);
          */
      },
      updateFlags () {
        this.FlagKNN = 0
        this.FlagRF = 0
      }
  },
  mounted () {
    EventBus.$on('updateFlagKNN', data => { this.FlagKNN = data })
    EventBus.$on('updateFlagRF', data => { this.FlagRF = data })
    EventBus.$on('updateFlagKNN', this.overview)
    EventBus.$on('updateFlagRF', this.overview)
    EventBus.$on('sendParameters', data => { this.storeParameters = data })
    EventBus.$on('updateActiveModels', data => { this.storeActiveModels = data })
    EventBus.$on('updateActiveModels', this.overview)
    //EventBus.$on('updateActiveModels', this.drawEncodings)

    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})

    // reset the views
    EventBus.$on('resetViews', this.reset)

    EventBus.$on('alternateFlagLock', this.updateFlags)
    EventBus.$on('alternateFlagLock', this.overview)
  }

}
</script>

<style>
/* Styles go here */

.category-circle {
  fill: url(#gradient-categorization);
}

.question-circle {
  fill: url(#gradient-questions);
}

.chart-area-circle {
  stroke: #fff;
  stroke-width: 3px;
  fill: url(#gradient-chart-area);
}

.center-circle {
  fill: #fff;
}

.bars {
  fill: url(#gradient-bars);
}

.gridlines {
  fill: none;
  stroke: #fff;
}

.minor {
  stroke-width: 1px
}

.major {
  stroke-width: 6px
}

.question-label-arc {
  /*fill: white;
    stroke: #AAAAAA;
    fill: url(#gradient-questions);*/
}

.category-label-text {
  font-weight: bold;
  font-size: 14px;
  fill: #fff;
}

.question-label-text {
  font-size: 7px;
  font-weight: bold;
  fill: gray;
}

.question-labels {
  text-anchor: middle;
  font-weight: bold;
}

.category-labels {
  text-anchor: middle;
  font-weight: bold;
  font-size: 14px;
  fill: #fff;
}

.filled {
  fill: url(#mainGradient);
}

#overview {
  min-height: 430px;
}
</style>