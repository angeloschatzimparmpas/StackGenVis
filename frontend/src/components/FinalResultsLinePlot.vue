<template>
  <div id="LinePlot" class="LinePlot"></div>
</template>

<script>
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'FinalResultsLinePlot',
  data () {
    return {
      FinalResultsforLinePlot: 0,
      NumberofExecutions: 0,
      scoresMean: [],
      scoresSTD: [],
      scoresPositive : [], 
      scoresNegative: [],
      xaxis: []
    }
  },
  methods: {
    LinePlotView () {
      this.NumberofExecutions ++ 
      this.xaxis.push(this.NumberofExecutions)

      this.scoresMean.push((JSON.parse(this.FinalResultsforLinePlot[0])*100).toFixed(1))
      this.scoresSTD.push((JSON.parse(this.FinalResultsforLinePlot[1])*100).toFixed(1))

      this.scoresPositive.push(parseFloat(this.scoresMean[this.scoresMean.length - 1]) + parseFloat(this.scoresSTD[this.scoresSTD.length - 1]))
      this.scoresNegative.push(parseFloat(this.scoresMean[this.scoresMean.length - 1]) - parseFloat(this.scoresSTD[this.scoresSTD.length - 1]))

      
      var xaxisReversed = []
      xaxisReversed = this.xaxis.slice().reverse()
      xaxisReversed = this.xaxis.concat(xaxisReversed)

      // fill in 'text' array for hover
      var text = this.scoresSTD.map (function(value, i) {
          return `STD: +/-${value}`
        })

      var trace1 = {
        x: this.xaxis, 
        y: this.scoresMean, 
        text: text,
        line: {color: "rgb(0,100,80)"}, 
        mode: "lines+markers", 
        name: "Current Accuracy", 
        type: "scatter"
      }

      var trace2 = {
        x: xaxisReversed, 
        y: this.scoresPositive.concat(this.scoresNegative), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(0,100,80,0.2)", 
        line: {color: "transparent"}, 
        name: "Current Accuracy", 
        showlegend: false, 
        type: "scatter"
      }

      const DataforLinePlot = [trace1, trace2]
      const layout = {
        title: 'Stack Ensemble Learning Score',
        paper_bgcolor: "rgb(255,255,255)", 
        plot_bgcolor: "rgb(229,229,229)", 
        xaxis: {
            gridcolor: "rgb(255,255,255)",
            title: 'Step of Execution',
            tickformat: '.0f',
            range: [0, this.scoresMean.length + 2], 
            showgrid: true, 
            showline: false, 
            showticklabels: true, 
            tickcolor: "rgb(127,127,127)", 
            ticks: "outside", 
            zeroline: false
        }, 
        yaxis: {
            gridcolor: "rgb(255,255,255)", 
            title: 'Performance (%)',
            showgrid: true, 
            showline: false, 
            showticklabels: true, 
            tickcolor: "rgb(127,127,127)", 
            ticks: "outside", 
            zeroline: false
        }
      }
      Plotly.newPlot('LinePlot', DataforLinePlot, layout, {showSendToCloud: true, responsive: true})
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingLinePlot', data => {
      this.FinalResultsforLinePlot = data})
    EventBus.$on('emittedEventCallingLinePlot', this.LinePlotView)
  }
}
</script>