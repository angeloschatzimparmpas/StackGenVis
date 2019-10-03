<template>
  <div id="OverviewPlotly" class="OverviewPlotly"></div>
</template>

<script>
import * as Plotly from 'plotly.js'
import * as d3Base from 'd3'

import { EventBus } from '../main.js'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default {
  name: 'ScatterPlot',
  data () {
    return {
      ScatterPlotResults: '',
      representationDefault: 'MDS',
      colorsforOver: [],
      brushedBox : [],
      max: 0,
      min: 0,
      parametersAll: [],
      length: 0,
    }
  },
  methods: {
    ScatterPlotView () {

      function isEquivalent(a, b) {
        // Create arrays of property names
        var aProps = Object.getOwnPropertyNames(a);
        var bProps = Object.getOwnPropertyNames(b);

        // If number of properties is different,
        // objects are not equivalent
        if (aProps.length != bProps.length) {
            return false;
        }

        for (var i = 0; i < aProps.length; i++) {
            var propName = aProps[i];

            // If values of same property are not equal,
            // objects are not equivalent
            if (a[propName] !== b[propName]) {
                return false;
            }
        }

        // If we made it this far, objects
        // are considered equivalent
        return true;
    }

      Plotly.purge('OverviewPlotly')
      var colorsforScatterPlot = JSON.parse(this.ScatterPlotResults[0])
      console.log(colorsforScatterPlot)
      var MDSData = JSON.parse(this.ScatterPlotResults[1])
      console.log(MDSData)
      var parameters = JSON.parse(this.ScatterPlotResults[2])
      parameters = JSON.parse(parameters)
      var classifiersInfo = this.brushedBox
      var keepingArrayIndices = []
      var modelsDetails = []
      var modelsIDs = []
      for (var j in parameters) {
        for (var i in classifiersInfo) {
          if (isEquivalent(JSON.parse(this.parametersAll[classifiersInfo[i].model]),parameters[j])) {
            keepingArrayIndices.push(j)
            modelsDetails.push(this.parametersAll[classifiersInfo[i].model])
            modelsIDs.push(classifiersInfo[i].model)
          } else {
          }
        }
      }

      var flag
      this.length = keepingArrayIndices.length
      EventBus.$emit('sendPointsNumber', this.length)
      EventBus.$emit('sendModelsIDs', modelsIDs)
      EventBus.$emit('sendIndicestoRemove', keepingArrayIndices)
      var lengthInitial = colorsforScatterPlot.length
      var counter = 0
      for (var i = 0; i < lengthInitial; i++) {
        flag = 0
        for (var j = 0; j < keepingArrayIndices.length; j++) {
          if (i == parseInt(keepingArrayIndices[j])) {
            flag = 1
          }
        }
        if (flag == 0) {
          colorsforScatterPlot.splice(i-counter, 1)
          MDSData[0].splice(i-counter,1)
          MDSData[1].splice(i-counter,1)
          counter++
        }
      }
      console.log(MDSData)
      console.log(colorsforScatterPlot)
      if (this.colorsforOver.length != 0) {
        if (this.colorsforOver[1].length != 0) {
          MDSData = this.colorsforOver[1]
        }
        if (this.colorsforOver[0].length != 0) {
          colorsforScatterPlot = this.colorsforOver[0]
        }
      }
      console.log(this.colorsforOver)
      var classifiersInfoProcessing = []
      for (let i = 0; i < modelsDetails.length; i++) {
        classifiersInfoProcessing[i] = 'Model ID: ' + modelsIDs[i] + '; Details: ' + modelsDetails[i]
      }
      var DataGeneral
      var layout
        DataGeneral = [{
          type: 'scatter',
          mode: 'markers',
          x: MDSData[0],
          y: MDSData[1],
          hovertemplate: 
                "<b>%{text}</b><br><br>" +
                "<extra></extra>",
          text: classifiersInfoProcessing,
          marker: {
              color: colorsforScatterPlot,
              size: 12,
              colorscale: 'Viridis',
              colorbar: {
                title: 'Metrics Average',
                titleside: 'Top'
              },
          }
        }]
        layout = {
          title: 'Models Performance (MDS)',
          xaxis: {
              visible: false
          },
          yaxis: {
              visible: false
          },
          autosize: true,
          width: 400,
          height: 400,
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', y: -0.3},
        }
     
      var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian','zoomIn2d','zoomOut2d','zoom2d'], responsive: true}
      
      var scat = document.getElementById('OverviewPlotly')
      
      Plotly.newPlot(scat, DataGeneral, layout, config)

      this.selectedPointsOverview()
    },
    selectedPointsOverview () {
      const OverviewPlotly = document.getElementById('OverviewPlotly')
      OverviewPlotly.on('plotly_selected', function (evt) {
        if (typeof evt !== 'undefined') {
          const ClassifierIDsList = []
          for (let i = 0; evt.points.length; i++) {
            if (evt.points[i] === undefined) {
              break
            } else {
              const OnlyId = evt.points[i].text.split(';')
              ClassifierIDsList.push(OnlyId[0])
            }
          }
          if (ClassifierIDsList != '') {
            EventBus.$emit('SendSelectedPointsToServerEvent', ClassifierIDsList)
          } else {
            EventBus.$emit('SendSelectedPointsToServerEvent', '')
          }
        }
      })
    },
    UpdateScatter () {
      this.ScatterPlotView()
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingBrushedBoxPlot', data => {
      this.brushedBox = data})
    EventBus.$on('emittedEventCallingScatterPlot', data => {
      this.ScatterPlotResults = data})
    EventBus.$on('emittedEventCallingScatterPlot', this.ScatterPlotView)
    EventBus.$on('getColors', data => {
      this.colorsforOver = data})
    EventBus.$on('ParametersAll',  data => { this.parametersAll = data })
    EventBus.$on('getColors', this.UpdateScatter)
  }
}
</script>