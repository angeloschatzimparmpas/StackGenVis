<template>
    <div>
        <div id="my_dataviz"></div>
    </div>
</template>

<script>
    import { EventBus } from '../main.js'
    import * as d3Base from 'd3'
    import { counter } from '@fortawesome/fontawesome-svg-core'

    // attach all d3 plugins to the d3 library
    const d3 = Object.assign(d3Base)

    export default {
        name: 'BalancePredictions',
        data () {
            return {
            resultsfromOverview: '',
            newResultsFromSelection: '',
            responsiveWidthHeight: []
            }
        },
        methods: {
          reset () {
            var svg = d3.select("#my_dataviz");
            svg.selectAll("*").remove();
          },
          Balance () {
            // erase histogram
            var svg = d3.select("#my_dataviz");
            svg.selectAll("*").remove();

            // responsive visualizations
            var widthInitial = this.responsiveWidthHeight[0]*6.5
            var heightInitial = this.responsiveWidthHeight[1]*0.5

            var performancePerModel = JSON.parse(this.resultsfromOverview[0])
            var performancePerModelSelection = []
            console.log(this.newResultsFromSelection)
            if (this.newResultsFromSelection.length != 0) {
              var performancePerModelSelection = JSON.parse(this.newResultsFromSelection[0]) 
            }
            var modelId = JSON.parse(this.resultsfromOverview[13])
            var data = []

            performancePerModel.forEach(element => {
              let el = {}
              el.type = "variable 1"
              el.value = element
              data.push(el)
            })

            if (performancePerModelSelection.length == 0) {
              performancePerModel.forEach(element => {
                let el = {}
                el.type = "variable 2"
                el.value = element
                data.push(el)
              })
            } else {
              performancePerModelSelection.forEach(element => {
                let el = {}
                el.type = "variable 2"
                el.value = element
                data.push(el)
              })
            }

            // set the dimensions and margins of the graph
            var margin = {top: 10, right: 30, bottom: 50, left: 60},
                width = widthInitial - margin.left - margin.right,
                height = heightInitial - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#my_dataviz")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

            // add the x Axis
            var x = d3.scaleLinear()
                .domain([0,100])
                .range([0, width]);
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            // set the parameters for the histogram
            var histogram = d3.histogram()
                .value(function(d) { return +d.value; })   // I need to give the vector of value
                .domain(x.domain())  // then the domain of the graphic
                .thresholds(x.ticks(20)); // then the numbers of bins

            // And apply twice this function to data to get the bins.
            var bins1 = histogram(data.filter( function(d){return d.type === "variable 1"} ));
            var bins2 = histogram(data.filter( function(d){return d.type === "variable 2"} ));

            // Y axis: scale and draw:
            var y1 = d3.scaleLinear()
                .range([height/2, 0])
                .domain([0, d3.max(bins1, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
            svg.append("g")
                .attr("transform", "translate(-20,0)")
                .call(d3.axisLeft(y1).ticks(5).tickSizeOuter(0));

            // Y axis: scale and draw:
            var y2 = d3.scaleLinear()
                .range([height/2, height])
                .domain([0, d3.max(bins2, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
            svg.append("g")
                .attr("transform", "translate(-20,0)")
                .call(d3.axisLeft(y2).ticks(5).tickSizeOuter(0));

             // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
            // Its opacity is set to 0: we don't see it by default.
            var tooltip = d3.select("#my_dataviz")
              .append("div")
              .style("opacity", 0)
              .attr("class", "tooltip")
              .style("background-color", "black")
              .style("color", "white")
              .style("border-radius", "5px")
              .style("padding", "10px")

            // A function that change this tooltip when the user hover a point.
            // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
            var showTooltip = function(d) {
              tooltip
                .transition()
                .duration(100)
                .style("opacity", 1)
              tooltip
                .html("Range: " + d.x0 + " - " + d.x1)
                .style("left", (d3.mouse(this)[0]+20) + "px")
                .style("top", (d3.mouse(this)[1]) + "px")
            }
            var moveTooltip = function(d) {
              tooltip
              .style("left", (d3.mouse(this)[0]+20) + "px")
              .style("top", (d3.mouse(this)[1]) + "px")
            }
            // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
            var hideTooltip = function(d) {
              tooltip
                .transition()
                .duration(100)
                .style("opacity", 0)
            }

            // append the bars for series 1
            svg.selectAll("rect")
                .data(bins1)
                .enter()
                .append("rect")
                  .attr("x", 1)
                  .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y1(d.length) + ")"; })
                  .attr("width", function(d) { return x(d.x1) - x(d.x0) - 1 ; })
                  .attr("height", function(d) { return height/2 - y1(d.length); })
                  .attr("stroke-linejoin", "round")
                  .style("fill", "#000000")
                  .style("opacity", 1)
                  .on("mouseover", showTooltip )
                  .on("mousemove", moveTooltip )
                  .on("mouseleave", hideTooltip )

            // append the bars for series 2
           svg.selectAll("rect2")
                .data(bins2)
                .enter()
                .append("rect")
                  .attr("x", 1)
                  .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + height/2 + ")"; })
                  .attr("width", function(d) { return x(d.x1) - x(d.x0) - 1 ; })
                  .attr("height", function(d) { return y2(d.length) - height/2; })
                  .attr("stroke-linejoin", "round")
                  .style("fill", "#D3D3D3")
                  .style("opacity", 1)
                  // Show tooltip on hover
                  .on("mouseover", showTooltip )
                  .on("mousemove", moveTooltip )
                  .on("mouseleave", hideTooltip )

                  

            // Handmade legend
            var heightforText = 215
            svg.append("circle").attr("cx", 215).attr("cy", heightforText-1.5).attr("r", 6).style("fill", "#000")
            svg.append("circle").attr("cx", 785).attr("cy", heightforText-1.5).attr("r", 6).style("fill", "#D3D3D3")
            svg.append("text").attr("x", 230).attr("y", heightforText).text("All Points").style("font-size", "16px").attr("alignment-baseline","middle")
            svg.append("text").attr("x", 515).attr("y", heightforText-6).text("# Performance (%) #").style("font-size", "16px").attr("alignment-baseline","top")
            svg.append("text").attr("x", 800).attr("y", heightforText).text("Selected Points").style("font-size", "16px").attr("alignment-baseline","middle")
            svg.append("text").attr("transform", "rotate(-90)").attr("x", -89).attr("y", -45).style("text-anchor", "middle").style("font-size", "16px").text("Number of Models"); 

            // Function to compute density
            function kernelDensityEstimator(kernel, X) {
              return function(V) {
                return X.map(function(x) {
                  return [x, d3.mean(V, function(v) { return kernel(x - v); })];
                });
              };
            }
            function kernelEpanechnikov(k) {
              return function(v) {
                  return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
              };
            }
          }
        },
        mounted () {
          EventBus.$on('emittedEventCallingBalanceView', data => { this.resultsfromOverview = data} )
          EventBus.$on('emittedEventCallingBalanceView', this.Balance)
          EventBus.$on('UpdateBalanceView', data => { this.newResultsFromSelection = data} )
          EventBus.$on('UpdateBalanceView', this.Balance)
          EventBus.$on('Responsive', data => {
          this.responsiveWidthHeight = data})
          EventBus.$on('ResponsiveandChange', data => {
          this.responsiveWidthHeight = data})

          // reset view
          EventBus.$on('resetViews', this.reset)
        }
    }
</script>

<style>
.hover {
  fill: #69c;
}
</style>