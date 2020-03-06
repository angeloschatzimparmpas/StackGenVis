<template>
    <div>
      <b-row class="md-3">
        <b-col cols="12">
          <div id="overview"></div>
        </b-col>
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
      allActiveSVC: [],
      allActiveGausNB: [],
      allActiveMLP: [],
      allActiveLR: [],
      allActiveLDA: [],
      allActiveQDA: [],
      allActiveRF: [],
      allActiveExtraT: [],
      allActiveAdaB: [],
      allActiveGradB: [],
      storeParameters: [],
      keepState: 0,
      FlagKNN: 0,
      FlagSVC: 0,
      FlagGausNB: 0,
      FlagMLP: 0,
      FlagLR: 0,
      FlagLDA: 0,
      FlagQDA: 0,
      FlagRF: 0,
      FlagExtraT: 0,
      FlagAdaB: 0,
      FlagGradB: 0,
      FlagBrushAll: 0,
      SVCModels: 576,
      GausNBModels: 736, 
      MLPModels: 1236,
      LRModels: 1356, 
      LDAModels: 1996,
      QDAModels: 2196,
      RFModels: 2446,
      ExtraTModels: 2606,
      AdaBModels: 2766,
      GradBModels: 2926,
      countkNNRelated: [],
      countKNN: 0,
      countSVCRelated: [],
      countSVC: 0,
      countGausNBRelated: [],
      countGausNB: 0,
      countMLPRelated: [],
      countMLP: 0,
      countLRRelated: [],
      countLR: 0,
      countLDARelated: [],
      countLDA: 0,
      countQDARelated: [],
      countQDA: 0,
      countRFRelated: [],
      countRF: 0,
      countExtraTRelated: [],
      countExtraT: 0,
      countAdaBRelated: [],
      countAdaB: 0,
      countGradBRelated: [],
      countGradB: 0,
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
      margin: {top: 60, right: 20, bottom: 20, left: 120}, //The margins around the circle
      legendPosition: {x: 20, y: 20}, // the position of the legend, from the top-left corner of the svg
      levels: 3,				//How many levels or inner circles should there be drawn
      maxValue: 0, 				//What is the value that the biggest circle will represent
      labelFactor: 1.25, 			//How much farther than the radius of the outer circle should the labels be placed
      wrapWidth: 60, 			//The number of pixels after which a label needs to be given a new line
      opacityArea: 0.35, 			//The opacity of the area of the blob
      dotRadius: 2, 				//The size of the colored circles of each blog
      opacityCircles: 0.1, 			//The opacity of the circles of each blob
      strokeWidth: 2, 			//The width of the stroke around each blob
      roundStrokes: false,			//If true the area and stroke will follow a round path (cardinal-closed)
      color: d3.scale.category10(),		//Color function
      axisName: "axis",
      areaName:"areaName",
      value: "value",
      sortAreas: true,
      colorsDiff: ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#b15928']
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
        .attr("transform", "translate(5,5)")
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
        .attr("x", 10)
        .attr("y", function(d){return -d*radius/cfg.levels;})
        .attr("dy", "0.4em")
        .style("font-size", "16px")
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
        .attr("transform", "translate(5,5)")
        .attr("x2", function(d, i){ return rScale(maxValue*1.2) * Math.cos(angleSlice*i - Math.PI/2); })
        .attr("y2", function(d, i){ return rScale(maxValue*1.2) * Math.sin(angleSlice*i - Math.PI/2); })
        .attr("class", "line")
        .style("stroke", "white")
        .style("stroke-width", "2px");

      axis.append("rect")
        .attr("text-anchor", "left")
        .attr("dy", "0.35em")
        .attr("x", function(d, i){ return (rScale(maxValue * cfg.labelFactor) * Math.cos(angleSlice*i - Math.PI/2)) - 25; })
        .attr("y", function(d, i){ return rScale(maxValue * cfg.labelFactor) * Math.sin(angleSlice*i - Math.PI/2); })
        .text(function(d){return d})
        .attr("width", 15)
        .attr("height", 15)
        .style("fill", function(d,i) { return cfg.colorsDiff[i]; })

      //Append the labels at each axis
      axis.append("text")
        .attr("class", "legend")
        .style("font-size", "16px")
        .attr("text-anchor", "middle")
        .attr("dy", "0em")
        .style("font-size", "16px")
        .attr("x", function(d, i){ return (rScale(maxValue * cfg.labelFactor) * Math.cos(angleSlice*i - Math.PI/2)) + 15; })
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
        .attr("transform", "translate(5,5)")
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
          var newX
          var newY
          newX =  parseFloat(d3.select(this).attr('cx')) - 10;
          newY =  parseFloat(d3.select(this).attr('cy')) - 10;
              
          tooltip
            .attr('x', newX+5)
            .attr('y', newY+5)
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

      const max = 640
      const KNNAll = 576
      const SVCAll = 160
      const GausNBAll = 500
      const MLPAll = 120
      const LRAll = 640
      const LDAAll = 200
      const QDAAll = 250
      const RFAll = 160
      const ExtraTAll = 160
      const AdaBAll = 160
      const GradBAll = 180

      var KNNSelection = 0
      var SVCSelection = 0
      var GausNBSelection = 0
      var MLPSelection = 0
      var LRSelection = 0
      var LDASelection = 0
      var QDASelection = 0
      var RFSelection = 0
      var ExtraTSelection = 0
      var AdaBSelection = 0
      var GradBSelection = 0

      if (this.FlagBrushAll == 0 && this.FlagKNN == 0 && this.FlagSVC == 0 && this.FlagGausNB == 0 && this.FlagMLP == 0 && this.FlagLR == 0 && this.FlagLDA == 0 && this.FlagQDA == 0 && this.FlagRF == 0 && this.FlagExtraT == 0 && this.FlagAdaB == 0 && this.FlagGradB == 0) {
        this.storeActiveModels = []
        this.allActiveKNN = []
        this.allActiveSVC = []
        this.allActiveGausNB = []
        this.allActiveMLP = []
        this.allActiveLR = []
        this.allActiveLDA = []
        this.allActiveQDA = []
        this.allActiveRF = []
        this.allActiveExtraT = []
        this.allActiveAdaB = []
        this.allActiveGradB = []
        this.countkNNRelated = []
        this.countKNN = 0
        this.countSVCRelated = []
        this.countSVC = 0
        this.countGausNBRelated = []
        this.countGausNB = 0
        this.countMLPRelated = []
        this.countMLP = 0
        this.countLRRelated = []
        this.countLR = 0
        this.countLDARelated = []
        this.countLDA = 0
        this.countQDARelated = []
        this.countQDA = 0
        this.countRFRelated = []
        this.countRF = 0
        this.countExtraTRelated = []
        this.countExtraT = 0
        this.countAdaBRelated = []
        this.countAdaB = 0
        this.countGradBRelated = []
        this.countGradB = 0
      }

      if(JSON.stringify(this.keepState)!=JSON.stringify(this.storeActiveModels)) {
        if (this.storeActiveModels.length != 0) {
          var intersection = this.compare(this.keepState,this.storeActiveModels)
          for (let k = 0; k < intersection.length; k++) {
            if (intersection[k] > this.GradBModels) {
              this.countGradB = 0
            } else if (intersection[k] > this.AdaBModels) {
              this.countAdaB = 0
            } else if (intersection[k] > this.ExtraTModels) {
              this.countExtraT = 0
            } else if (intersection[k] > this.RFModels) {
              this.countRF = 0
            } else if (intersection[k] > this.QDAModels) {
              this.countQDA = 0
            } else if (intersection[k] > this.LDAModels) {
              this.countLDA = 0
            } else if (intersection[k] > this.LRModels) {
              this.countLR = 0
            } else if (intersection[k] > this.MLPModels) {
              this.countMLP = 0
            } else if (intersection[k] > this.GausNBModels) {
              this.countGausNB = 0
            } else if (intersection[k] > this.SVCModels) {
              this.countSVC = 0
            } else {
              this.countKNN = 0
            }
          }
         
          for (let i = 0; i < this.storeActiveModels.length; i++) {
            if (this.storeActiveModels[i] > this.GradBModels) {
              this.countGradBRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countGradB++
            } else if (this.storeActiveModels[i] > this.AdaBModels) {
              this.countAdaBRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countAdaB++
            } else if (this.storeActiveModels[i] > this.ExtraTModels) {
              this.countExtraTRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countExtraT++
            } else if (this.storeActiveModels[i] > this.RFModels) {
              this.countRFRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countRF++
            } else if (this.storeActiveModels[i] > this.QDAModels) {
              this.countQDARelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countQDA++
            } else if (this.storeActiveModels[i] > this.LDAModels) {
              this.countLDARelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countLDA++
            } else if (this.storeActiveModels[i] > this.LRModels) {
              this.countLRRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countLR++
            } else if (this.storeActiveModels[i] > this.MLPModels) {
              this.countMLPRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countMLP++
            } else if (this.storeActiveModels[i] > this.GausNBModels) {
              this.countGausNBRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countGausNB++
            } else if (this.storeActiveModels[i] > this.SVCModels) {
              this.countSVCRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countSVC++
            } else {
              this.countkNNRelated.push(JSON.parse(this.storeParameters[this.storeActiveModels[i]]))
              this.countKNN++
            }
          }
        }
        if (this.storeActiveModels[0] > this.GradBModels) {
          this.allActiveGradB = this.countGradBRelated.slice()
        } else if (this.storeActiveModels[0] > this.AdaBModels) {
          this.allActiveAdaB = this.countAdaBRelated.slice()
        } else if (this.storeActiveModels[0] > this.ExtraTModels) {
          this.allActiveExtraT = this.countExtraTRelated.slice()
        } else if (this.storeActiveModels[0] > this.RFModels) {
          this.allActiveRF = this.countRFRelated.slice()
        } else if (this.storeActiveModels[0] > this.QDAModels) {
          this.allActiveQDA = this.countQDARelated.slice()
        } else if (this.storeActiveModels[0] > this.LDAModels) {
          this.allActiveLDA = this.countLDARelated.slice()
        } else if (this.storeActiveModels[0] > this.LRModels) {
          this.allActiveLR = this.countLRRelated.slice()
        } else if (this.storeActiveModels[0] > this.MLPModels) {
          this.allActiveMLP = this.countMLPRelated.slice()
        } else if (this.storeActiveModels[0] > this.GausNBModels) {
          this.allActiveGausNB = this.countGausNBRelated.slice()
        } else if (this.storeActiveModels[0] > this.SVCModels) {
          this.allActiveSVC = this.countSVCRelated.slice()
        } else {
          this.allActiveKNN = this.countkNNRelated.slice()
        }
      }

      KNNSelection = this.countKNN
      SVCSelection = this.countSVC
      GausNBSelection = this.countGausNB
      MLPSelection = this.countMLP
      LRSelection = this.countLR
      LDASelection = this.countLDA
      QDASelection = this.countQDA
      RFSelection = this.countRF
      ExtraTSelection = this.countExtraT
      AdaBSelection = this.countAdaB
      GradBSelection = this.countGradB

      this.keepState = JSON.parse(JSON.stringify(this.storeActiveModels))

      if (this.FlagKNN == 1 && this.allActiveKNN.length == 0) {
        KNNSelection = 576
      }
      if (this.FlagSVC == 1 && this.allActiveSVC.length == 0) {
        SVCSelection = 160
      }
      if (this.FlagGausNB == 1 && this.allActiveGausNB.length == 0) {
        GausNBSelection = 500
      }
      if (this.FlagMLP == 1 && this.allActiveMLP.length == 0) {
        MLPSelection = 120
      }
      if (this.FlagLR == 1 && this.allActiveLR.length == 0) {
        LRSelection = 640
      }
      if (this.FlagLDA == 1 && this.allActiveLDA.length == 0) {
        LDASelection = 200
      }
      if (this.FlagQDA == 1 && this.allActiveQDA.length == 0) {
        QDASelection = 250
      }
      if (this.FlagRF == 1 && this.allActiveRF.length == 0) {
        RFSelection = 160
      }
      if (this.FlagExtraT == 1 && this.allActiveExtraT.length == 0) {
        ExtraTSelection = 160
      }
      if (this.FlagAdaB == 1 && this.allActiveAdaB.length == 0) {
        AdaBSelection = 160
      }
      if (this.FlagGradB == 1 && this.allActiveGradB.length == 0) {
        GradBSelection = 180
      }

    ////////////////////////////////////////////////////////////// 
    //////////////////////// Set-Up ////////////////////////////// 
    ////////////////////////////////////////////////////////////// 

      var margin = {top: 50, right: 120, bottom: 55, left: 65},
        legendPosition = {x: 425, y: 25},
				width = Math.min(520, window.innerWidth - 10) - margin.left - margin.right,
        height = Math.min(width + 12, window.innerHeight + 12 - margin.top - margin.bottom);
        
			////////////////////////////////////////////////////////////// 
			////////////////////////// Data ////////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var data = [
					  [
						{axis:"KNN [576]",legend:"Entire",value:KNNAll/max},
            {axis:"SVC [160]",legend:"Entire",value:SVCAll/max},
            {axis:"GauNB [500]",legend:"Entire",value:GausNBAll/max},
            {axis:"MLP [120]",legend:"Entire",value:MLPAll/max},
            {axis:"LR [640]",legend:"Entire",value:LRAll/max},
            {axis:"LDA [200]",legend:"Entire",value:LDAAll/max},
            {axis:"QDA [250]",legend:"Entire",value:QDAAll/max},
            {axis:"RF [160]",legend:"Entire",value:RFAll/max},
            {axis:"ExtraT [160]",legend:"Entire",value:ExtraTAll/max},
            {axis:"AdaB [160]",legend:"Entire",value:AdaBAll/max},
            {axis:"GradB [180]",legend:"Entire",value:GradBAll/max},
            ],[
						{axis:"KNN [576]",legend:"Selection",value:KNNSelection/max},
            {axis:"SVC [160]",legend:"Selection",value:SVCSelection/max},
            {axis:"GauNB [500]",legend:"Selection",value:GausNBSelection/max},
            {axis:"MLP [120]",legend:"Selection",value:MLPSelection/max},
            {axis:"LR [640]",legend:"Selection",value:LRSelection/max},
            {axis:"LDA [200]",legend:"Selection",value:LDASelection/max},
            {axis:"QDA [250]",legend:"Selection",value:QDASelection/max},
            {axis:"RF [160]",legend:"Selectionn",value:RFSelection/max},
            {axis:"ExtraT [160]",legend:"Selection",value:ExtraTSelection/max},
            {axis:"AdaB [160]",legend:"Selection",value:AdaBSelection/max},
            {axis:"GradB [180]",legend:"Selection",value:GradBSelection/max},
					  ],
					];
			////////////////////////////////////////////////////////////// 
			//////////////////// Draw the Chart ////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var color = d3.scale.ordinal()
				.range(["#ffed6f","#000000"]);
      
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
      this.FlagSVC = 0
      this.FlagGausNB = 0
      this.FlagMLP = 0
      this.FlagLR = 0
      this.FlagLDA = 0
      this.FlagQDA = 0
      this.FlagRF = 0
      this.FlagExtraT = 0
      this.FlagAdaB = 0
      this.FlagGradB = 0
    },
    compare(arr1,arr2){
      
    const finalarray =[];

    arr1.forEach((e1) => arr2.forEach((e2) =>
      {if(e1 === e2){
        finalarray.push(e1)
      }
    }
      
    ))
    return finalarray
    }
  },
  mounted () {
    EventBus.$on('updateFlagKNN', data => { this.FlagKNN = data })
    EventBus.$on('updateFlagSVC', data => { this.FlagSVC = data })
    EventBus.$on('updateFlagGauNB', data => { this.FlagGausNB = data })
    EventBus.$on('updateFlagMLP', data => { this.FlagMLP = data })
    EventBus.$on('updateFlagLR', data => { this.FlagLR = data })
    EventBus.$on('updateFlagLDA', data => { this.FlagLDA = data })
    EventBus.$on('updateFlagQDA', data => { this.FlagQDA = data })
    EventBus.$on('updateFlagRF', data => { this.FlagRF = data })
    EventBus.$on('updateFlagExtraT', data => { this.FlagExtraT = data })
    EventBus.$on('updateFlagAdaB', data => { this.FlagAdaB = data })
    EventBus.$on('updateFlagGradB', data => { this.FlagGradB = data })

    EventBus.$on('flagBrushedAll', data => { this.FlagBrushAll = data })

    EventBus.$on('updateFlagKNN', this.overview)
    EventBus.$on('updateFlagSVC', this.overview)
    EventBus.$on('updateFlagGauNB', this.overview)
    EventBus.$on('updateFlagMLP', this.overview)
    EventBus.$on('updateFlagLR', this.overview)
    EventBus.$on('updateFlagLDA', this.overview)
    EventBus.$on('updateFlagQDA', this.overview)
    EventBus.$on('updateFlagRF', this.overview)
    EventBus.$on('updateFlagExtraT', this.overview)
    EventBus.$on('updateFlagAdaB', this.overview)
    EventBus.$on('updateFlagGradB', this.overview)

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
  transform: translate(5px, 5px);
}

.center-circle {
  fill: #fff;
  transform: translate(5px, 5px);
}

.bars {
  fill: url(#gradient-bars);
}

.gridlines {
  fill: none;
  stroke: #fff;
  transform: translate(5px, 5px);
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
  font-size: 16px;
  fill: #fff;
}

.question-label-text {
  font-size: 16px;
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
  font-size: 16px;
  fill: #fff;
}

.filled {
  fill: url(#mainGradient);
}

#overview {
  min-height: 450px;
}
</style>