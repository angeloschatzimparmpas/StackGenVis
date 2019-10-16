<template>
    <div>
        <div id="overview"></div>
    </div>
</template>

<script>
import { EventBus } from '../main.js'

export default {
  name: 'Parameters',
  data () {
    return {
        WH: [],
    }
  },
  methods: {
     draw() {
          var widthinter = this.WH[0]*3 // interactive visualization
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

          svg.append("circle")
            .attr("r", maxBarHeight + 70)
            .classed("category-circle", true);

          svg.append("circle")
            .attr("r", maxBarHeight + 40)
            .classed("question-circle", true);

          svg.append("circle")
            .attr("r", maxBarHeight)
            .classed("chart-area-circle", true);

          svg.append("circle")
            .attr("r", innerRadius)
            .classed("center-circle", true);

            var data = [
                { algorithm: 'KNN', parameter: 'n_neighbors', percentage: 70 },
                { algorithm: 'KNN', parameter: 'metric', percentage: 50 },
                { algorithm: 'KNN', parameter: 'algorithm', percentage: 75 },
                { algorithm: 'KNN', parameter: 'weight', percentage: 50 },
                { algorithm: 'RF', parameter: 'n_estimators', percentage: 80 },
                { algorithm: 'RF', parameter: 'criterion', percentage: 50 }
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
              .innerRadius(maxBarHeight + 40)
              .outerRadius(maxBarHeight + 64);

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
              .outerRadius(maxBarHeight + 2);

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
              //console.log(d3.select(this)[0]);
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
              .attr("y2", -maxBarHeight - 40)
              .attr("transform", function(d, i) {
                return "rotate(" + (d.rotate) + ")";
              });

            // category lines
            svg.selectAll("line.y.major")
              .data(cats)
              .enter().append("line")
              .classed("gridlines major", true)
              .attr("y1", -innerRadius)
              .attr("y2", -maxBarHeight - 70)
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
        }
  },
  mounted () {
    EventBus.$on('emittedEventCallingOverview',this.draw)
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})
  }

}
</script>

<style>
/* Styles go here */

.category-circle {
  fill: #F4A636;
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
</style>