<template>
  <div id="Heatmap"></div>
</template>

<script>
import * as d3Base from 'd3'
import { EventBus } from '../main.js'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default {
  name: "Heatmap",
  data () {
    return {
      GetResultsAll: '',
    }
  },
  methods: {
    Heatmap () {
      // Clear Heatmap first
      var svg = d3.select("#Heatmap");
      svg.selectAll("*").remove();

      var FeaturesAccuracy = JSON.parse(this.GetResultsAll[6])
      var Features= JSON.parse(this.GetResultsAll[7])
      const limit = JSON.parse(this.GetResultsAll[12])
      var Classifiers = JSON.parse(this.GetResultsAll[8])
        
      if (Classifiers != '') { 
        var limitList = []
        if (limit == '') {
          for (let i = 0; i < Classifiers.length; i++) {
              limitList.push(Classifiers[i])
          }
        } else {
            limitList = []
            for (let i = 0; i < limit.length; i++) {
                for (let j = 0; j < Classifiers.length; j++) {
                    if (Number(limit[i].match(/\d+/)[0]) == Classifiers[j]) {
                        limitList.push(Number(limit[i].match(/\d+/)[0]))
                    }
                }
            }
        }

        let len = Features.length
        let indicesYAxis = new Array(len)
        for (let i = 0; i < len; i++) {
            indicesYAxis[i] = i
        } 

        // set the dimensions and margins of the graph
        var margin = {top: 30, right: 30, bottom: 30, left: 30},
        width = 300 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

        // append the svg object to the body of the page
        var svg = d3.select("#Heatmap")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
        
        let len2 = limitList.length
        let indicesXAxis = new Array(len)
        for (let i = 0; i < len2; i++) {
            indicesXAxis[i] = i
        } 

        // Labels of row and columns
        var myGroups = indicesXAxis
        var myVars = indicesYAxis

        // Build X scales and axis:
        var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(myGroups)
        .padding(0.01);
        svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))

        // Build X scales and axis:
        var y = d3.scaleBand()
        .range([ height, 0 ])
        .domain(myVars)
        .padding(0.01);
        svg.append("g")
        .call(d3.axisLeft(y));

        // Build color scale
        var myColor = d3.scaleLinear().range(["#deebf7", "#08306b"])
            .domain([1,100])

        var data = []
        var counter = 0 
        for (let j = 0; j < len2; j++) {
            for (let i = 0; i <len; i++) {
                data.push({'group':indicesXAxis[j], 'variable':indicesYAxis[i],'value':FeaturesAccuracy[counter][0]*100})
                counter++
            }
        }

        // add the squares
        svg.selectAll()
            .data(data, function(d) {return d.group+':'+d.variable;})
            .enter()
            .append("rect")
            .attr("x", function(d) { return x(d.group) })
            .attr("y", function(d) { return y(d.variable) })
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            .style("fill", function(d) { return myColor(d.value)} )

      }
    }
  },
  mounted () {
        EventBus.$on('emittedEventCallingHeatmapView', data => { this.GetResultsAll = data })
        EventBus.$on('emittedEventCallingHeatmapView', this.Heatmap)
    }
}
</script>