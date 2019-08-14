<template>
  <div id="OverviewPlotly" class="OverviewPlotly"></div>
</template>

<script>
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'ScatterPlot',
  data () {
    return {
      ScatterPlotResults: ''
    }
  },
  methods: {
    ScatterPlotView () {
      const colorsforScatterPlot = JSON.parse(this.ScatterPlotResults[0])
      const MDSData = JSON.parse(this.ScatterPlotResults[1])
      const classifiersInfo = JSON.parse(this.ScatterPlotResults[2])

      var classifiersInfoProcessing = []
      for (let i = 0; i < classifiersInfo.length; i++) {
        classifiersInfoProcessing[i] = 'ClassifierID: ' + i + '; Details: '
      }
      const DataforMDS = [{
      x: MDSData[0],
      y: MDSData[1],
      mode: 'markers',
      text: classifiersInfoProcessing,
      marker: {
          color: colorsforScatterPlot,
          size: 12,
          colorscale: 'Viridis',
          colorbar: {
          title: 'Metrics Sum',
          titleside: 'Top'
          },
          reversescale: true
      }
      }]
      const layout = {
      title: 'Models Performance (MDS)',
      xaxis: {
          visible: false
      },
      yaxis: {
          visible: false
      }
      }
      Plotly.newPlot('OverviewPlotly', DataforMDS, layout)

      this.selectedPointsOverview()
    },
    selectedPointsOverview () {
      const OverviewPlotly = document.getElementById('OverviewPlotly')
      OverviewPlotly.on('plotly_selected', function (evt) {
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
        }
      })
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingScatterPlot', data => {
      this.ScatterPlotResults = data})
    EventBus.$on('emittedEventCallingScatterPlot', this.ScatterPlotView)
  }
}
</script>