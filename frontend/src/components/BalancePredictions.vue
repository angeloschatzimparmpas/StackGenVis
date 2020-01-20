<template>
    <div>
        <div id="my_dataviz"></div>
    </div>
</template>

<script>
    import { EventBus } from '../main.js'
    import * as d3Base from 'd3'

    // attach all d3 plugins to the d3 library
    const d3 = Object.assign(d3Base)

    export default {
        name: 'BalancePredictions',
        data () {
            return {
            resultsfromOverview: 0,
            WH: []
            }
        },
        methods: {
            Balance () {

            // Clear Heatmap first
            var svg = d3.select("#my_dataviz");
            svg.selectAll("*").remove();

            var widthInitial = this.WH[0]*3 // interactive visualization
            var heightInitial = this.WH[1]/1.6 // interactive visualization

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

            // get the data
            d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_doubleHist.csv").then( function(data) {
            // add the x Axis
            var x = d3.scaleLinear()
                .domain([-10,15])
                .range([0, width]);
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            // add the first y Axis
            var y1 = d3.scaleLinear()
                        .range([height/2, 0])
                        .domain([0, 0.12]);
            svg.append("g")
                .attr("transform", "translate(-20,0)")
                .call(d3.axisLeft(y1).tickValues([0.05, 0.1]));

            // add the first y Axis
            var y2 = d3.scaleLinear()
                        .range([height/2, height])
                        .domain([0, 0.12]);
            svg.append("g")
                .attr("transform", "translate(-20,0)")
                .call(d3.axisLeft(y2).ticks(2).tickSizeOuter(0));

            // Compute kernel density estimation
            var kde = kernelDensityEstimator(kernelEpanechnikov(7), x.ticks(60))
            var density1 =  kde( data.filter( function(d){return d.type === "variable 1"} ).map(function(d){  return d.value; }) )
            var density2 =  kde( data.filter( function(d){return d.type === "variable 2"} ).map(function(d){  return d.value; }) )

            // Plot the area
            svg.append("path")
                .attr("class", "mypath")
                .datum(density1)
                .attr("fill", "#000")
                .attr("opacity", "1")
                .attr("stroke", "#000")
                .attr("stroke-width", 1)
                .attr("stroke-linejoin", "round")
                .attr("d",  d3.line()
                    .curve(d3.curveBasis)
                    .x(function(d) { return x(d[0]); })
                    .y(function(d) { return y1(d[1]); })
                );

            // Plot the area
            svg.append("path")
                .attr("class", "mypath")
                .datum(density2)
                .attr("fill", "#D3D3D3")
                .attr("opacity", "1")
                .attr("stroke", "#000")
                .attr("stroke-width", 1)
                .attr("stroke-linejoin", "round")
                .attr("d",  d3.line()
                    .curve(d3.curveBasis)
                    .x(function(d) { return x(d[0]); })
                    .y(function(d) { return y2(d[1]); })
                );

            }).catch(function(error){
                // handle error   
            })

            // Handmade legend
            var heightforText = 175
            svg.append("circle").attr("cx",80).attr("cy",heightforText).attr("r", 6).style("fill", "#000")
            svg.append("circle").attr("cx",300).attr("cy",heightforText).attr("r", 6).style("fill", "#D3D3D3")
            svg.append("text").attr("x", 100).attr("y", heightforText).text("Entire distribution").style("font-size", "15px").attr("alignment-baseline","middle")
            svg.append("text").attr("x", 320).attr("y", heightforText).text("Selected points").style("font-size", "15px").attr("alignment-baseline","middle")

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
            EventBus.$on('Responsive', data => {
            this.WH = data})
            EventBus.$on('ResponsiveandChange', data => {
            this.WH = data})
        }
    }
</script>