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

import { legend } from 'd3-svg-legend'

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
    RadarChart(id, data, options) {
      var cfg = {
      w: 600,				//Width of the circle
      h: 600,				//Height of the circle
      margin: {top: 20, right: 20, bottom: 20, left: 20}, //The margins around the circle
      legendPosition: {x: 20, y: 20}, // the position of the legend, from the top-left corner of the svg
      levels: 3,				//How many levels or inner circles should there be drawn
      maxValue: 0, 				//What is the value that the biggest circle will represent
      labelFactor: 1.25, 			//How much farther than the radius of the outer circle should the labels be placed
      wrapWidth: 60, 			//The number of pixels after which a label needs to be given a new line
      opacityArea: 0.35, 			//The opacity of the area of the blob
      dotRadius: 4, 				//The size of the colored circles of each blog
      opacityCircles: 0.1, 			//The opacity of the circles of each blob
      strokeWidth: 2, 			//The width of the stroke around each blob
      roundStrokes: false,			//If true the area and stroke will follow a round path (cardinal-closed)
      color: d3.scale.category10(),		//Color function
      axisName: "axis",
      areaName:"areaName",
      value: "value",
      sortAreas: true,
      };
      
      //Put all of the options into a variable called cfg
      if('undefined' !== typeof options){
        for(var i in options){
        if('undefined' !== typeof options[i]){ cfg[i] = options[i]; }
        }//for i
      }//if

      //Map the fields specified in the configuration 
      // to the axis and value variables
      var axisName = cfg["axisName"],
          areaName = cfg["areaName"],
          value = cfg["value"];

      //If the supplied maxValue is smaller than the actual one, replace by the max in the data
	    var maxValue = Math.max(cfg.maxValue, d3.max(data, function(i){return d3.max(i.map(function(o){return o.value;}))}))
        
      var allAxis = (data[0].map(function(d, i){ return d[axisName] })),	//Names of each axis
        total = allAxis.length,					//The number of different axes
        radius = Math.min(cfg.w/2, cfg.h/2), 			//Radius of the outermost circle
        Format = d3.format('%'),			 	//Percentage formatting
        angleSlice = Math.PI * 2 / total;			//The width in radians of each "slice"

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
        .radius(function(d) { return rScale(d[value]); })
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
        .attr("class", function(d) {
          return "radarArea" + " " + d[0][areaName].replace(/\s+/g, '') //Remove spaces from the areaName string to make one valid class name
        })
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
        .attr("cx", function(d,i){ return rScale(d[value]) * Math.cos(angleSlice*i - Math.PI/2); })
        .attr("cy", function(d,i){ return rScale(d[value]) * Math.sin(angleSlice*i - Math.PI/2); })
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
        .attr("cx", function(d,i){ return rScale(d[value]) * Math.cos(angleSlice*i - Math.PI/2); })
        .attr("cy", function(d,i){ return rScale(d[value]) * Math.sin(angleSlice*i - Math.PI/2); })
        .style("fill", "none")
        .style("pointer-events", "all")
        .on("mouseover", function(d,i) {
          newX =  parseFloat(d3.select(this).attr('cx')) - 10;
          newY =  parseFloat(d3.select(this).attr('cy')) - 10;
              
          tooltip
            .attr('x', newX)
            .attr('y', newY)
            .text(Format(d[value]))
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
      /////////////////// Helper Functions ////////////////////
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

      // on mouseover for the legend symbol
      function cellover(d) {
          //Dim all blobs
          d3.selectAll(".radarArea")
            .transition().duration(200)
            .style("fill-opacity", 0.1); 
          //Bring back the hovered over blob
          d3.select("." + data[d][0][areaName].replace(/\s+/g, ''))
            .transition().duration(200)
            .style("fill-opacity", 0.7);	
      }

      // on mouseout for the legend symbol
      function cellout() {
        //Bring back all blobs
        d3.selectAll(".radarArea")
          .transition().duration(200)
          .style("fill-opacity", cfg.opacityArea);
      }

      /////////////////////////////////////////////////////////
      /////////////////// Draw the Legend /////////////////////
      /////////////////////////////////////////////////////////

      svg.append("g")
        .attr("class", "legendOrdinal")
        .attr("transform", "translate(" + cfg["legendPosition"]["x"] + "," + cfg["legendPosition"]["y"] + ")");

      var legendOrdinal = legend.color()
          .shape("path", d3.svg.symbol().type("circle").size(150)())
          .shapePadding(10)
          .scale(cfg.color)
          .labels(cfg.color.domain().map(function(d){
            return data[d][0][areaName];
          }))
          .on("cellover", function(d){ cellover(d); })
          .on("cellout", function(d) { cellout(); });

      svg.select(".legendOrdinal").call(legendOrdinal);
      
    },
    overview() {
       /* Radar chart design created by Nadieh Bremer - VisualCinnamon.com */
      // Clear Heatmap first
      var svg = d3.select("#overview");
      svg.selectAll("*").remove();

      var widthinter = this.WH[0]*2 // interactive visualization
      var heightinter = this.WH[1]*1.23 // interactive visualization

      const max = 576
      const KNNAll = 576
      const RFAll = 160
      var KNNSelection = 0
      var RFSelection = 0

      if (this.FlagKNN == 0 && this.FlagRF == 0) {
        this.storeActiveModels = []
        this.allActiveKNN = []
        this.allActiveRF = []
      }

      if (this.storeActiveModels.length != 0) {
        var countkNNRelated = []
        var countKNN = 0
        var countRFRelated = []
        var countRF = 0
        for (let i = 0; i < this.storeActiveModels.length; i++) {
          if (this.storeActiveModels[i] < this.KNNModels) {
            countkNNRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
            countKNN = countKNN + 1
          } else {
            countRFRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
            countRF = countRF + 1
          }
        }
        if (this.storeActiveModels[0] < this.KNNModels) {
          this.allActiveKNN = countkNNRelated.slice()
        } else {
          this.allActiveRF = countRFRelated.slice()
        }

        KNNSelection = countKNN
        RFSelection = countRF
      }


      if (this.FlagKNN == 1 && this.allActiveKNN.length == 0) {
        KNNSelection = 576
      }

      if (this.FlagRF == 1 && this.allActiveRF.length == 0) {
        RFSelection = 160
      }

    ////////////////////////////////////////////////////////////// 
    //////////////////////// Set-Up ////////////////////////////// 
    ////////////////////////////////////////////////////////////// 

      var margin = {top: 50, right: 120, bottom: 50, left: 60},
        legendPosition = {x: 425, y: 185},
				width = Math.min(510, window.innerWidth - 10) - margin.left - margin.right,
				height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);
					
			////////////////////////////////////////////////////////////// 
			////////////////////////// Data ////////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var data = [
					  [
						{axis:"KNN [Models 576]",legend:"Entire",value:KNNAll/max},
            {axis:"RF [Models 160]",legend:"Entire",value:RFAll/max},
            {axis:"Alg3",legend:"Entire",value:0.55},
            {axis:"Alg4",legend:"Entire",value:0.68},
            {axis:"Alg5",legend:"Entire",value:0.22},
            {axis:"Alg6",legend:"Entire",value:0.28},
            {axis:"Alg7",legend:"Entire",value:0.55},
            {axis:"Alg8",legend:"Entire",value:0.68},
            {axis:"Alg9",legend:"Entire",value:0.22},
            {axis:"Alg10",legend:"Entire",value:0.28},
            {axis:"Alg11",legend:"Entire",value:0.28},
            ],[
						{axis:"KNN [Models 576]",legend:"Selection",value:KNNSelection/max},
            {axis:"RF [Models 160]",legend:"Selection",value:RFSelection/max},
            {axis:"Alg3",legend:"Selection",value:0.25},
            {axis:"Alg4",legend:"Selection",value:0.28},
            {axis:"Alg5",legend:"Selection",value:0.22},
            {axis:"Alg6",legend:"Selection",value:0.18},
            {axis:"Alg7",legend:"Selection",value:0.45},
            {axis:"Alg8",legend:"Selectionn",value:0.18},
            {axis:"Alg9",legend:"Selection",value:0.22},
            {axis:"Alg10",legend:"Selection",value:0.18},
            {axis:"Alg11",legend:"Selection",value:0.18},
					  ],
					];
			////////////////////////////////////////////////////////////// 
			//////////////////// Draw the Chart ////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var color = d3.scale.ordinal()
				.range(["#808000","#008080"]);
      
			var radarChartOptions = {
			  w: width,
			  h: height,
        margin: margin,
        legendPosition: legendPosition,
			  maxValue: 0.5,
			  levels: 5,
			  roundStrokes: true,
        color: color,
        axisName: "axis",
        areaName: "legend",
        value: "value"
			};
			//Call function to draw the Radar chart
			this.RadarChart("#overview", data, radarChartOptions);
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