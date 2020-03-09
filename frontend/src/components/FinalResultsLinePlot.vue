<template>
  <div id="LinePlot" style="min-height: 363px;"></div>
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
      scoresPositive: [], 
      scoresNegative: [],
      scoresMean2: [],
      scoresSTD2: [],
      scoresPositive2: [], 
      scoresNegative2: [],
      scoresMean3: [],
      scoresSTD3: [],
      scoresPositive3: [], 
      scoresNegative3: [],
      scoresMean4: [],
      scoresSTD4: [],
      scoresPositive4: [], 
      scoresNegative4: [],
      Stack_scoresMean: [],
      Stack_scoresSTD: [],
      Stack_scoresPositive: [], 
      Stack_scoresNegative: [],
      Stack_scoresMean2: [],
      Stack_scoresSTD2: [],
      Stack_scoresPositive2: [], 
      Stack_scoresNegative2: [],
      Stack_scoresMean3: [],
      Stack_scoresSTD3: [],
      Stack_scoresPositive3: [], 
      Stack_scoresNegative3: [],
      Stack_scoresMean4: [],
      Stack_scoresSTD4: [],
      Stack_scoresPositive4: [], 
      Stack_scoresNegative4: [],
      xaxis: [],
      WH: [],
      firstTime: 0
    }
  },
  methods: {
    reset () {
      Plotly.purge('LinePlot')
    },
    LinePlotView () {
      this.NumberofExecutions ++ 
      this.xaxis.push(this.NumberofExecutions)

      // Under Exploration = Current
      this.scoresMean.push((JSON.parse(this.FinalResultsforLinePlot[0])*100).toFixed(2))
      this.scoresSTD.push((JSON.parse(this.FinalResultsforLinePlot[1])*100).toFixed(2))

      this.scoresPositive.push(parseFloat(this.scoresMean[this.scoresMean.length - 1]) + parseFloat(this.scoresSTD[this.scoresSTD.length - 1]))
      this.scoresNegative.push(parseFloat(this.scoresMean[this.scoresMean.length - 1]) - parseFloat(this.scoresSTD[this.scoresSTD.length - 1]))

      this.scoresMean2.push((JSON.parse(this.FinalResultsforLinePlot[4])*100).toFixed(2))
      this.scoresSTD2.push((JSON.parse(this.FinalResultsforLinePlot[5])*100).toFixed(2))

      this.scoresPositive2.push(parseFloat(this.scoresMean2[this.scoresMean2.length - 1]) + parseFloat(this.scoresSTD2[this.scoresSTD2.length - 1]))
      this.scoresNegative2.push(parseFloat(this.scoresMean2[this.scoresMean2.length - 1]) - parseFloat(this.scoresSTD2[this.scoresSTD2.length - 1]))

      this.scoresMean3.push((JSON.parse(this.FinalResultsforLinePlot[8])*100).toFixed(2))
      this.scoresSTD3.push((JSON.parse(this.FinalResultsforLinePlot[9])*100).toFixed(2))

      this.scoresPositive3.push(parseFloat(this.scoresMean3[this.scoresMean3.length - 1]) + parseFloat(this.scoresSTD3[this.scoresSTD3.length - 1]))
      this.scoresNegative3.push(parseFloat(this.scoresMean3[this.scoresMean3.length - 1]) - parseFloat(this.scoresSTD3[this.scoresSTD3.length - 1]))

      this.scoresMean4.push((JSON.parse(this.FinalResultsforLinePlot[12])*100).toFixed(2))
      this.scoresSTD4.push((JSON.parse(this.FinalResultsforLinePlot[13])*100).toFixed(2))

      this.scoresPositive4.push(parseFloat(this.scoresMean4[this.scoresMean4.length - 1]) + parseFloat(this.scoresSTD4[this.scoresSTD4.length - 1]))
      this.scoresNegative4.push(parseFloat(this.scoresMean4[this.scoresMean4.length - 1]) - parseFloat(this.scoresSTD4[this.scoresSTD4.length - 1]))

      // Stack

      this.Stack_scoresMean.push((JSON.parse(this.FinalResultsforLinePlot[2])*100).toFixed(2))
      this.Stack_scoresSTD.push((JSON.parse(this.FinalResultsforLinePlot[3])*100).toFixed(2))

      this.Stack_scoresPositive.push(parseFloat(this.Stack_scoresMean[this.Stack_scoresMean.length - 1]) + parseFloat(this.Stack_scoresSTD[this.Stack_scoresSTD.length - 1]))
      this.Stack_scoresNegative.push(parseFloat(this.Stack_scoresMean[this.Stack_scoresMean.length - 1]) - parseFloat(this.Stack_scoresSTD[this.Stack_scoresSTD.length - 1]))

      this.Stack_scoresMean2.push((JSON.parse(this.FinalResultsforLinePlot[6])*100).toFixed(2))
      this.Stack_scoresSTD2.push((JSON.parse(this.FinalResultsforLinePlot[7])*100).toFixed(2))

      this.Stack_scoresPositive2.push(parseFloat(this.Stack_scoresMean2[this.Stack_scoresMean2.length - 1]) + parseFloat(this.Stack_scoresSTD2[this.Stack_scoresSTD2.length - 1]))
      this.Stack_scoresNegative2.push(parseFloat(this.Stack_scoresMean2[this.Stack_scoresMean2.length - 1]) - parseFloat(this.Stack_scoresSTD2[this.Stack_scoresSTD2.length - 1]))


      this.Stack_scoresMean3.push((JSON.parse(this.FinalResultsforLinePlot[10])*100).toFixed(2))
      this.Stack_scoresSTD3.push((JSON.parse(this.FinalResultsforLinePlot[11])*100).toFixed(2))

      this.Stack_scoresPositive3.push(parseFloat(this.Stack_scoresMean3[this.Stack_scoresMean3.length - 1]) + parseFloat(this.Stack_scoresSTD3[this.Stack_scoresSTD3.length - 1]))
      this.Stack_scoresNegative3.push(parseFloat(this.Stack_scoresMean3[this.Stack_scoresMean3.length - 1]) - parseFloat(this.Stack_scoresSTD3[this.Stack_scoresSTD3.length - 1]))

      this.Stack_scoresMean4.push((JSON.parse(this.FinalResultsforLinePlot[14])*100).toFixed(2))
      this.Stack_scoresSTD4.push((JSON.parse(this.FinalResultsforLinePlot[15])*100).toFixed(2))

      this.Stack_scoresPositive4.push(parseFloat(this.Stack_scoresMean4[this.Stack_scoresMean4.length - 1]) + parseFloat(this.Stack_scoresSTD4[this.Stack_scoresSTD4.length - 1]))
      this.Stack_scoresNegative4.push(parseFloat(this.Stack_scoresMean4[this.Stack_scoresMean4.length - 1]) - parseFloat(this.Stack_scoresSTD4[this.Stack_scoresSTD4.length - 1]))
      
      var xaxisReversed = []
      xaxisReversed = this.xaxis.slice().reverse()
      xaxisReversed = this.xaxis.concat(xaxisReversed)

      // fill in 'text' array for hover
      var text = this.scoresSTD.map (function(value, i) {
          return `STD: +/-${value}`
        })

      // Current

      var trace1 = {
        x: this.xaxis, 
        y: this.scoresMean, 
        text: text,
        line: {color: "rgb(55,126,184)"}, 
        mode: "lines+markers", 
        marker : {
          symbol: 'circle' },
        name: "Active Accuracy",
        type: "scatter"
      }

      var trace2 = {
        x: xaxisReversed, 
        y: this.scoresPositive.concat(this.scoresNegative), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(55,126,184,0)", 
        line: {color: "transparent"}, 
        name: "Active Accuracy", 
        showlegend: false, 
        type: "scatter"
      }

      var text = this.scoresSTD2.map (function(value, i) {
          return `STD: +/-${value}`
      })

      var trace3 = {
        x: this.xaxis, 
        y: this.scoresMean2, 
        text: text,
        line: {color: "rgb(55,126,184)"}, 
        mode: "lines+markers", 
        marker : {
            symbol: 'square' },
        name: "Active Precision", 
        type: "scatter"
      }

      var trace4 = {
        x: xaxisReversed, 
        y: this.scoresPositive2.concat(this.scoresNegative2), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(55,126,184,0)", 
        line: {color: "transparent"}, 
        name: "Active Precision", 
        showlegend: false, 
        type: "scatter"
      }
      var text = this.scoresSTD3.map (function(value, i) {
          return `STD: +/-${value}`
      })
      var trace5 = {
        x: this.xaxis, 
        y: this.scoresMean3, 
        text: text,
        line: {color: "rgb(55,126,184)"}, 
        mode: "lines+markers", 
        marker : {
            symbol: 'triangle-up' },
        name: "Active Recall", 
        type: "scatter"
      }

      var trace6 = {
        x: xaxisReversed, 
        y: this.scoresPositive3.concat(this.scoresNegative3), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(55,126,184,0)", 
        line: {color: "transparent"}, 
        name: "Active Recall", 
        showlegend: false, 
        type: "scatter"
      }
      var text = this.scoresSTD4.map (function(value, i) {
          return `STD: +/-${value}`
      })
      var trace7 = {
        x: this.xaxis, 
        y: this.scoresMean4, 
        text: text,
        line: {color: "rgb(55,126,184)"}, 
        mode: "lines+markers", 
        marker : {
            symbol: 'diamond' },
        name: "Active F1 Score", 
        type: "scatter"
      }

      var trace8 = {
        x: xaxisReversed, 
        y: this.scoresPositive4.concat(this.scoresNegative4), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(55,126,184,0)", 
        line: {color: "transparent"}, 
        name: "Active F1 Score", 
        showlegend: false, 
        type: "scatter"
      }

      // Stack
      var text = this.Stack_scoresSTD.map (function(value, i) {
          return `STD: +/-${value}`
      })
        var trace9 = {
        x: this.xaxis, 
        y: this.Stack_scoresMean, 
        text: text,
        line: {color: "rgb(228,26,28)"}, 
        mode: "lines+markers", 
        marker : {
          symbol: 'x' },
        name: "Stack Accuracy", 
        type: "scatter"
      }

      var trace10 = {
        x: xaxisReversed, 
        y: this.Stack_scoresPositive.concat(this.Stack_scoresNegative), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(228,26,28,0)", 
        line: {color: "transparent"}, 
        name: "Stack Accuracy", 
        showlegend: false, 
        type: "scatter"
      }
      var text = this.Stack_scoresSTD2.map (function(value, i) {
          return `STD: +/-${value}`
      })
      var trace11 = {
        x: this.xaxis, 
        y: this.Stack_scoresMean2, 
        text: text,
        line: {color: "rgb(228,26,28)"}, 
        mode: "lines+markers", 
        marker : {
          symbol: 'cross' },
        name: "Stack Precision", 
        type: "scatter"
      }

      var trace12 = {
        x: xaxisReversed, 
        y: this.Stack_scoresPositive2.concat(this.Stack_scoresNegative2), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(228,26,28,0)", 
        line: {color: "transparent"}, 
        name: "Stack Precision", 
        showlegend: false, 
        type: "scatter"
      }
      var text = this.Stack_scoresSTD3.map (function(value, i) {
          return `STD: +/-${value}`
      })
      var trace13 = {
        x: this.xaxis, 
        y: this.Stack_scoresMean3, 
        text: text,
        line: {color: "rgb(228,26,28)"}, 
        mode: "lines+markers",
        marker : {
          symbol: 'triangle-down' },
        name: "Stack Recall", 
        type: "scatter"
      }

      var trace14 = {
        x: xaxisReversed, 
        y: this.Stack_scoresPositive3.concat(this.Stack_scoresNegative3), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(228,26,28,0)", 
        line: {color: "transparent"}, 
        name: "Stack Recall", 
        showlegend: false, 
        type: "scatter"
      }
      var text = this.Stack_scoresSTD4.map (function(value, i) {
          return `STD: +/-${value}`
      })
      var trace15 = {
        x: this.xaxis, 
        y: this.Stack_scoresMean4, 
        text: text,
        line: {color: "rgb(228,26,28)"}, 
        mode: "lines+markers",
        marker : {
          symbol: 'hexagram' },
        name: "Stack F1 Score", 
        type: "scatter"
      }

      var trace16 = {
        x: xaxisReversed, 
        y: this.Stack_scoresPositive4.concat(this.Stack_scoresNegative4), 
        text: '',
        hoverinfo: 'text',
        fill: "tozerox", 
        fillcolor: "rgba(228,26,28,0)", 
        line: {color: "transparent"}, 
        name: "Stack F1 Score", 
        showlegend: false, 
        type: "scatter"
      }

      const DataforLinePlot = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12, trace13, trace14, trace15, trace16]

      var width = this.WH[0]*3.18 // interactive visualization
      var height = this.WH[1]*0.765 // interactive visualization

      var layout = {
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        paper_bgcolor: "rgb(255,255,255)", 
        plot_bgcolor: "rgb(229,229,229)", 
        xaxis: {
            gridcolor: "rgb(255,255,255)",
            title: 'Step of the Execution',
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
            title: '# Performance (%) #',
            showgrid: true, 
            showline: false, 
            showticklabels: true, 
            tickcolor: "rgb(127,127,127)", 
            ticks: "outside", 
            zeroline: false
        },
        autosize: false,
        width: width,
        height: height,
        margin: {
          l: 50,
          r: 0,
          b: 50,
          t: 5,
          pad: 0
        },
      }
      var config = {displayModeBar: false, scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
      Plotly.newPlot('LinePlot', DataforLinePlot, layout, config)

      if (this.firstTime == 0) {
        EventBus.$emit('emittedEventCallingReally')
        this.firstTime = 1
      }
    }
  },
  mounted() {
    EventBus.$on('updateFlagForFinalResults', data => { this.firstTime = data})

    EventBus.$on('emittedEventCallingLinePlot', data => {
      this.FinalResultsforLinePlot = data})
    EventBus.$on('emittedEventCallingLinePlot', this.LinePlotView)

    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }
}
</script>