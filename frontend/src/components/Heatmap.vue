<template>
  <div id="Heatmap"></div>
</template>

<script>
import * as d3Base from 'd3'
import { EventBus } from '../main.js'
import $ from 'jquery'
import * as colorbr from 'colorbrewer'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)
const colorbrewer = Object.assign(colorbr)

export default {
  name: "Heatmap",
  data () {
    return {
      GetResultsAll: '',
      Toggles: '',
      limitation: 0,
      flag: false,
      classesNumber: 10,
      cellSize: 20,
      ModelsIDHeatStack: [],
      highlighted: []
    }
  },
  methods: {
    Refresh () {
      EventBus.$emit('SendSelectedFeaturesEvent', '')
    },
    reset () {
      var svg = d3.select("#Heatmap");
      svg.selectAll("*").remove();
    },
    Heatmap () {
      // Clear Heatmap first
      var svg = d3.select("#Heatmap");
      svg.selectAll("*").remove();
    
      var FeaturesAccuracy = JSON.parse(this.GetResultsAll[5])
      var Features = JSON.parse(this.GetResultsAll[6])
      var PermImpEli = JSON.parse(this.GetResultsAll[10])
      var featureUni = JSON.parse(this.GetResultsAll[11])
      var modelIds = JSON.parse(this.GetResultsAll[13])

      var len2 = modelIds.length

      var maxUni = Math.max.apply(Math, featureUni.map(function(o) { return o.Score; }))
      var minUni = Math.min.apply(Math, featureUni.map(function(o) { return o.Score; }))
      let len = Features.length
      let indicesYAxis = new Array(len)
      for (let i = 0; i < len; i++) {
          indicesYAxis[i] = [Features[i]]
      } 
      let indicesXAxis = new Array(len)
      var temp = []
      for (let i = 0; i < len2; i++) {
        temp = []
        temp.push("R")
        temp.push("Model "+modelIds[i].toString())
        indicesXAxis[i] = temp
      }

      if (this.ModelsIDHeatStack.length != 0) {

          var FeaturesAccuracyNew = []
          var PermImpEliNew = []
          indicesXAxis = new Array(len)

          for (let i = 0; i < modelIds.length; i++) {
              if (this.ModelsIDHeatStack.includes(modelIds[i])) {
              } else {
                  FeaturesAccuracyNew.push(FeaturesAccuracy[i])
                  PermImpEliNew.push(PermImpEli[i])
              }
          }
          FeaturesAccuracy = FeaturesAccuracyNew
          PermImpEli = PermImpEliNew
          len2 = this.ModelsIDHeatStack.length
          for (let i = 0; i < len2; i++) {
              temp = []
              temp.push("R")
              temp.push("Model "+this.ModelsIDHeatStack[i].toString())
              indicesXAxis[i] = temp
          }
        }

        temp = []
        temp.push("R")
        temp.push("Average")
        indicesXAxis[len2] = temp
        
        var values = []
        var msg = false
        var modelData = []
        for (let j = 0; j < len2; j++) {
          var data = []
          for (let i = 0; i <len; i++) {
              if (this.Toggles[0] == 1 && this.Toggles[1] == 1 && this.Toggles[2] == 1) {
                values[j] = ((((featureUni[i].Score-minUni)/(maxUni-minUni))*100)+(PermImpEli[j][i]*100+(FeaturesAccuracy[j][i]*100)))/3
              }
              else if (this.Toggles[0] == 1 && this.Toggles[1] == 1 && this.Toggles[2] == 0) {
                values[j] = ((((featureUni[i].Score-minUni)/(maxUni-minUni))*100)+(PermImpEli[j][i]*100))/2
              }
              else if (this.Toggles[0] == 1 && this.Toggles[1] == 0 && this.Toggles[2] == 1) {
                values[j] = ((((featureUni[i].Score-minUni)/(maxUni-minUni))*100)+(FeaturesAccuracy[j][i]*100))/2
              }
              else if (this.Toggles[0] == 0 && this.Toggles[1] == 1 && this.Toggles[2] == 1) {
                values[j] = ((PermImpEli[j][i]*100))/2
              }
              else if (this.Toggles[0] == 1 && this.Toggles[1] == 0 && this.Toggles[2] == 0) {
                values[j] = ((featureUni[i].Score-minUni)/(maxUni-minUni))*100
              }
              else if (this.Toggles[0] == 0 && this.Toggles[1] == 1 && this.Toggles[2] == 0) {
                values[j] = PermImpEli[j][i]*100
              }
              else if (this.Toggles[0] == 0 && this.Toggles[1] == 0 && this.Toggles[2] == 1) {
                values[j] = FeaturesAccuracy[j][i]*100
              } else {
                alert('Please, keep at least one metric active') // Fix this!
                values[j] = ((((featureUni[i].Score-minUni)/(maxUni-minUni))*100)+(PermImpEli[j][i]*100+(FeaturesAccuracy[j][i]*100)))/3
              }
              data.push(values[j]/100)
          }
          modelData.push(data)
        }
      var transposedArray = []
      transposedArray = modelData[0].map((col, i) => modelData.map(row => row[i]))

      let sum = 0
      let avg = 0
      for (let i = 0; i < transposedArray.length; i++) {
        sum = 0
        sum = (transposedArray[i].reduce((previous, current) => current += previous))
        avg = sum / transposedArray[i].length
        transposedArray[i][transposedArray[i].length] = avg
      }
      var dataAll = {"columns":indicesXAxis,"index":indicesYAxis,"data":transposedArray}
      this.heatmap_display(dataAll, "#Heatmap");

    },
    heatmap_display(data, heatmapId) {
    var cellSize = this.cellSize
    //##########################################################################
    // Patrick.Brockmann@lsce.ipsl.fr
    //##########################################################################
    
    //==================================================
    // References
    // http://bl.ocks.org/Soylent/bbff6cc507dca2f48792
    // http://bost.ocks.org/mike/selection/
    // http://bost.ocks.org/mike/join/
    // http://stackoverflow.com/questions/9481497/understanding-how-d3-js-binds-data-to-nodes
    // http://bost.ocks.org/mike/miserables/
    // http://bl.ocks.org/ianyfchang/8119685

    //==================================================
    var tooltip = d3.select(heatmapId)
        .append("div")
        .style("position", "absolute")
        .style("visibility", "hidden");

    //==================================================
    // http://bl.ocks.org/mbostock/3680958
    /* function zoom() {
      console.log(d3.event.translate)
      console.log(d3.event.scale)
      svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }*/

    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    const zoom = d3.zoom()
                        .scaleExtent([0.1, 3]) //zoom limit
                        .on('zoom', () => {
                            svg.attr('transform', d3.event.transform) // updated for d3 v4
                        })
    //==================================================
    var viewerWidth = $(document).width()/2.2;
    var viewerHeight = $(document).height()/5.5;
    var viewerPosTop = 125;
    var viewerPosLeft = 100;

    var legendElementWidth = cellSize * 2;

    // http://bl.ocks.org/mbostock/5577023
    var colors = colorbrewer.RdYlGn[this.classesNumber];

    // http://bl.ocks.org/mbostock/3680999
    var svg;

    //==================================================
      var arr = data.data;
      var row_number = arr.length;
      var col_number = arr[0].length;

      var colorScale = d3.scaleQuantize()
          .domain([0.0, 1.0])
          .range(colors);

      svg = d3.select(heatmapId).append("svg")
          .attr("width", viewerWidth)
          .attr("height", viewerHeight)
          .call(zoom)
            //.call(zoom.transform, d3.zoomIdentity.translate(200, 20).scale(0.25)) //initial size
            .append('svg:g')
            .attr("transform", "translate(" + viewerPosLeft + "," + viewerPosTop + ")");

      svg.append('defs')
          .append('pattern')
          .attr('id', 'diagonalHatch')
          .attr('patternUnits', 'userSpaceOnUse')
          .attr('width', 4)
          .attr('height', 4)
          .append('path')
          .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
          .attr('stroke', '#000000')
          .attr('stroke-width', 1);

      var rowSortOrder = false;
      var colSortOrder = false;

      var rowLabels = svg.append("g")
          .attr("class", "rowLabels")
          .selectAll(".rowLabel")
          .data(data.index)
          .enter().append("text")
          .text(function(d) {
              return d.count > 1 ? d.join("/") : d;
          })
          .attr("x", 0)
          .attr("y", function(d, i) {
              return (i * cellSize);
          })
          .style("text-anchor", "end")
          .attr("transform", function(d, i) {
              return "translate(-3," + cellSize / 1.5 + ")";
          })
          .attr("class", "rowLabel mono")
          .attr("id", function(d, i) {
              return "rowLabel_" + i;
          })
          .on('mouseover', function(d, i) {
              d3.select('#rowLabel_' + i).classed("hover", true);
          })
          .on('mouseout', function(d, i) {
              d3.select('#rowLabel_' + i).classed("hover", false);
          })
          .on("click", function(d, i) {
              rowSortOrder = !rowSortOrder;
              sortByValues("r", i, rowSortOrder);
              d3.select("#order").property("selectedIndex", 0);
              //$("#order").jqxComboBox({selectedIndex: 0});
          });

      var colLabels = svg.append("g")
          .attr("class", "colLabels")
          .selectAll(".colLabel")
          .data(data.columns)
          .enter().append("text")
          .text(function(d) {
              d.shift();
              return d.count > 1 ? d.reverse().join("/") : d.reverse();
          })
          .attr("x", 0)
          .attr("y", function(d, i) {
              return (i * cellSize);
          })
          .style("text-anchor", "left")
          .style('font-weight',function(d,i){
              /*if (d[0] === "Average") {
                return "bold"
              }*/
          })
          .attr("transform", function(d, i) {
              return "translate(" + cellSize / 2 + ", -3) rotate(-90) rotate(45, 0, " + (i * cellSize) + ")";
          })
          .attr("class", "colLabel mono")
          .attr("id", function(d, i) {
              return "colLabel_" + i;
          })
          .on('mouseover', function(d, i) {
              d3.select('#colLabel_' + i).classed("hover", true);
          })
          .on('mouseout', function(d, i) {
              d3.select('#colLabel_' + i).classed("hover", false);
          })
          .on("click", function(d, i) {
              colSortOrder = !colSortOrder;
              sortByValues("c", i, colSortOrder);
              d3.select("#order").property("selectedIndex", 0);
          });

      var row = svg.selectAll(".row")
          .data(data.data)
          .enter().append("g")
          .attr("id", function(d) {
            return d.idx;
          })
          .attr("class", "row");
      var heatMap = row.selectAll(".cell")
          .data(function(d) {
              return d;
          })
          .enter().append("svg:rect")
          .attr("id", function(d, i, j){
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return k.toString()+i.toString();
          })
          .attr("x", function(d, i) {
              return i * cellSize;
          })
          .attr("y", function(d, i, j) {
            var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return k * cellSize;
          })
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("class", function(d, i, j) {
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return "cell bordered cr" + k + " cc" + i;
          })
          .attr("row", function(d, i, j) {
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return k;
          })
          .attr("col", function(d, i, j) {
              return i;
          })
          .attr("width", cellSize)
          .attr("height", cellSize)
          .style("fill", function(d) {
              if (d != null) return colorScale(d);
              else return "url(#diagonalHatch)";
          })
          .on('mouseover', function(d, i, j) {
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              d3.select('#colLabel_' + i).classed("hover", true);
              d3.select('#rowLabel_' + k).classed("hover", true);
              if (d != null) {
                  tooltip.style("visibility", "visible");
                  tooltip.html('<div class="heatmap_tooltip">' + d.toFixed(3) + '</div>');
              } else
                  tooltip.style("visibility", "hidden");
          })
          .on('mouseout', function(d, i, j) {
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              d3.select('#colLabel_' + i).classed("hover", false);
              d3.select('#rowLabel_' + k).classed("hover", false);
              tooltip.style("visibility", "hidden");
          })
          .on("mousemove", function(d, i) {
              tooltip.style("top", (d3.mouse(this)[1]+75) + "px").style("left", (d3.mouse(this)[0]+87) + "px");
          })
          .on('click', function(d, i, j) {
            var rowsExtracted = svg.selectAll(".row")._groups[0]
            var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
            d3.select(this).style("fill", function(d) {
            if (d3.select(this).style("fill") === "url(\"#diagonalHatch\")"){
                return colorScale(d)
            } else {
                return "url(#diagonalHatch)"
            }
            })
            if (i+1 === j.length) {
                if(d3.select(this).style("fill") === "url(\"#diagonalHatch\")") {
                    row.selectAll(".cr"+k).style("fill", "url(#diagonalHatch)")
                } else {
                    row.selectAll(".cr"+k).style("fill", function(d) {
                        return colorScale(d)
                    })
                }
            }
            var finalresults = []
            for (let i = 0; i < rowsExtracted[0].childNodes.length - 1; i++) {
                var results = []
                for (let j = 0; j < rowsExtracted.length; j++) {
                    if (rowsExtracted[j].childNodes[i].style.fill === "url(\"#diagonalHatch\")") {
                    } else {
                        results.push(j)
                    }
                }
                finalresults.push(results)
            }
            EventBus.$emit('SendSelectedFeaturesEvent', finalresults)
          });

      var legend = svg.append("g")
          .attr("class", "legend")
          .attr("transform", "translate(0,-240)")
          .selectAll(".legendElement")
          .data([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
          .enter().append("g")
          .attr("class", "legendElement");

      legend.append("svg:rect")
          .attr("x", function(d, i) {
              return legendElementWidth * i;
          })
          .attr("y", viewerPosTop)
          .attr("class", "cellLegend bordered")
          .attr("width", legendElementWidth)
          .attr("height", cellSize / 2)
          .style("fill", function(d, i) {
              return colors[i];
          });

      legend.append("text")
          .attr("class", "mono legendElement")
          .text(function(d) {
              return "≥" + Math.round(d * 100) / 100;
          })
          .attr("x", function(d, i) {
              return legendElementWidth * i;
          })
          .attr("y", viewerPosTop + cellSize);

      //==================================================
      // Change ordering of cells
      function sortByValues(rORc, i, sortOrder) {
          var t = svg.transition().duration(1000);
          var values = [];
          var sorted;
          d3.selectAll(".c" + rORc + i)
              .filter(function(d) {
                  if (d != null) values.push(d);
                  else values.push(-999); // to handle NaN
              });
          //console.log(values);		
          if (rORc == "r") { // sort on cols
              sorted = d3.range(col_number).sort(function(a, b) {
                  if (sortOrder) {
                      return values[b] - values[a];
                  } else {
                      return values[a] - values[b];
                  }
              });
              t.selectAll(".cell")
                  .attr("x", function(d) {
                      var col = parseInt(d3.select(this).attr("col"));
                      return sorted.indexOf(col) * cellSize;
                  });
              t.selectAll(".colLabel")
                  .attr("y", function(d, i) {
                      return sorted.indexOf(i) * cellSize;
                  })
                  .attr("transform", function(d, i) {
                      return "translate(" + cellSize / 2 + ", -3) rotate(-90) rotate(45, 0, " + (sorted.indexOf(i) * cellSize) + ")";
                  });
          } else { // sort on rows
              sorted = d3.range(row_number).sort(function(a, b) {
                  if (sortOrder) {
                      return values[b] - values[a];
                  } else {
                      return values[a] - values[b];
                  }
              });
              t.selectAll(".cell")
                  .attr("y", function(d) {
                      var row = parseInt(d3.select(this).attr("row"));
                      return sorted.indexOf(row) * cellSize;
                  });
              t.selectAll(".rowLabel")
                  .attr("y", function(d, i) {
                      return sorted.indexOf(i) * cellSize;
                  })
                  .attr("transform", function(d, i) {
                      return "translate(-3," + cellSize / 1.5 + ")";
                  });
              }
          }

          //==================================================
          d3.select("#order").on("change", function() {
            var newOrder = d3.select("#order").property("value");	
            this.changeOrder(newOrder, heatmapId);
          });

          //==================================================
          d3.select("#palette")
            .on("keyup", function() {
              var newPalette = d3.select("#palette").property("value");
              if (newPalette != null)						// when interfaced with jQwidget, the ComboBox handles keyup event but value is then not available ?
                this.changePalette(newPalette, heatmapId);
            })
            .on("change", function() {
            var newPalette = d3.select("#palette").property("value");
              this.changePalette(newPalette, heatmapId);
            });

        //==================================================
    },
    changeOrder(newOrder, heatmapId) {
  var svg = d3.select(heatmapId);
  var cellSize = this.cellSize
  var t = svg.transition().duration(1000);
  if (newOrder == "sortinit_col") { // initial sort on cols (alphabetically if produced like this)
      t.selectAll(".cell")
          .attr("x", function(d) {
              var col = parseInt(d3.select(this).attr("col"));
              return col * cellSize;
          });
      t.selectAll(".colLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(" + cellSize / 2 + ", -3) rotate(-90) rotate(45, 0, " + (i * cellSize) + ")";
          });
  } else if (newOrder == "sortinit_row") { // initial sort on rows (alphabetically if produced like this)
      t.selectAll(".cell")
          .attr("y", function(d) {
              var row = parseInt(d3.select(this).attr("row"));
              return row * cellSize;
          });
      t.selectAll(".rowLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(-3," + cellSize / 1.5 + ")";
          });
  } else if (newOrder == "sortinit_col_row") { // initial sort on rows and cols (alphabetically if produced like this)
      t.selectAll(".cell")
          .attr("x", function(d) {
              var col = parseInt(d3.select(this).attr("col"));
              return col * cellSize;
          })
          .attr("y", function(d) {
              var row = parseInt(d3.select(this).attr("row"));
              return row * cellSize;
          });
      t.selectAll(".colLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(" + cellSize / 2 + ", -3) rotate(-90) rotate(45, 0, " + (i * cellSize) + ")";
          });
      t.selectAll(".rowLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(-3," + cellSize / 1.5 + ")";
          });
        }
    },
    reset () {
      var svg = d3.select("#Heatmap");
      svg.selectAll("*").remove();
    },
    brush () {
        var columnLabels = document.getElementsByClassName('colLabels')[0];
        var modelIds = JSON.parse(this.GetResultsAll[13])

        var selectedIds = []
        for (let i = 0; i < this.highlighted.length; i++) {
            let looping = this.highlighted[i]
            selectedIds.push(looping)
        }
        for (let i = 0; i < modelIds.length; i++) {
            columnLabels.childNodes[i].style.fill = "#000";
        }
        for (let i = 0; i < selectedIds.length; i++) {
            let index = modelIds.indexOf(selectedIds[i])
            columnLabels.childNodes[index].style.fill = "#AF4427";
        }
    }
  },
  mounted () {
      EventBus.$on('NewHeatmapAccordingtoNewStack', data => { this.ModelsIDHeatStack = data })
      EventBus.$on('NewHeatmapAccordingtoNewStack', this.Heatmap)
      EventBus.$on('emittedEventCallingToggles', data => { this.Toggles = data })
      EventBus.$on('emittedEventCallingHeatmapView', data => { this.GetResultsAll = data; this.flag = false })
      EventBus.$on('emittedEventCallingHeatmapView', this.Heatmap)
      EventBus.$on('emittedEventCallingTogglesUpdate', data => { this.Toggles = data; this.flag = true })
      EventBus.$on('emittedEventCallingTogglesUpdate', this.Refresh)
      EventBus.$on('emittedEventCallingTogglesUpdate', this.Heatmap)
      EventBus.$on('resetViews', this.reset)
      EventBus.$on('SendSelectedPointsToBrushHeatmap', data => { this.highlighted = data; })
      EventBus.$on('SendSelectedPointsToBrushHeatmap', this.brush)

      // reset the views
      EventBus.$on('resetViews', this.reset)
    }
}
</script>

<style>
.heatmap {
  font-size: 8px;
  font-family: monospace;
}
rect.bordered {
  stroke: #E6E6E6;
  stroke-width:2px;   
}
text.mono {
  font-size: 8px;
  font-family: monospace;
  fill: #000;
}
text.legendElement {
  font-size: 10px;
}
text.hover {
  font-weight: bold;
  fill: #007bff;
  font-background: #000;
}
.heatmap_tooltip {
  text-align: center;
  font-family: monospace;
  font-size: 14pt;
  color: #000;
  position: relative;
  background: rgba(255, 255, 255, 0.8);
  border: 4px solid #007bff;
  padding: 5px;
  border-radius: 8px ;
  -webkit-border-top-left-radius: 8px;
  -webkit-border-top-right-radius: 8px;
  -webkit-border-bottom-right-radius: 8px;
  -webkit-border-bottom-left-radius: 8px;
  -khtml-border-top-left-radius: 8px;
  -khtml-border-top-right-radius: 8px;
  -khtml-border-bottom-right-radius: 8px;
  -khtml-border-bottom-left-radius: 8px;
  -moz-border-radius-topleft: 8px;
  -moz-border-radius-topright: 8px;
  -moz-border-radius-bottomright: 8px;
  -moz-border-radius-bottomleft: 8px;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  border-bottom-left-radius: 8px;
  width: 100px;
  z-index:10000;
  -webkit-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);
  -moz-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);
  box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);
}
.heatmap_tooltip:after, .heatmap_tooltip:before {
  top: 100%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}
.heatmap_tooltip:after {
  border-color: rgba(236, 240, 241, 0);
  border-top-color: #FFFFF;
  border-width: 10px;
  left: 50%;
  margin-left: -10px;
}
.heatmap_tooltip:before {
  border-color: rgba(44, 62, 80, 0);
  border-top-color: #007bff;
  border-width: 16px;
  left: 50%;
  margin-left: -16px;
}
</style>