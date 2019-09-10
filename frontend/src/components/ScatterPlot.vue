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
      max: 0,
      min: 0,
    }
  },
  methods: {
    ScatterPlotView () {
      Plotly.purge('OverviewPlotly')
      var colorsforScatterPlot = JSON.parse(this.ScatterPlotResults[0])
      var MDSData = JSON.parse(this.ScatterPlotResults[1])
      var TSNEData = JSON.parse(this.ScatterPlotResults[12])
      const classifiersInfo = JSON.parse(this.ScatterPlotResults[2])
      if (this.colorsforOver.length != 0) {
        if (this.colorsforOver[1].length != 0) {
          MDSData = this.colorsforOver[1]
          TSNEData = this.colorsforOver[2]
        }
        if (this.colorsforOver[0].length != 0) {
          colorsforScatterPlot = this.colorsforOver[0]
        }
      }
      var classifiersInfoProcessing = []
      for (let i = 0; i < classifiersInfo.length; i++) {
        classifiersInfoProcessing[i] = 'Model ID: ' + i + '; Details: '
      }
      var DataGeneral
      var layout
      if ( this.representationDefault == 'MDS') {
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
                title: 'Metrics Sum',
                titleside: 'Top'
              },
              reversescale: true
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
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', y: -0.3},
        }
      } else {
        var result = TSNEData.reduce(function(r, a) {
            a.forEach(function(s, i) {
                var key = i === 0 ? 'Xax' : 'Yax';

                r[key] || (r[key] = []); // if key not found on result object, add the key with empty array as the value

                r[key].push(s);
            })
            return r;
        }, {})
        DataGeneral = [{
          type: 'scatter',
          mode: 'markers',
          x: result.Xax,
          y: result.Yax,
          hovertemplate: 
                "<b>%{text}</b><br><br>" +
                "<extra></extra>",
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
        layout = {
          title: 'Models Performance (t-SNE)',
          xaxis: {
              visible: false
          },
          yaxis: {
              visible: false
          },
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', y: -0.3},
        }
      }

      var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian','zoomIn2d','zoomOut2d','zoom2d'], responsive: true}
      
      Plotly.newPlot('OverviewPlotly', DataGeneral, layout, config)
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
    },
    UpdateScatter () {
      this.ScatterPlotView()
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingScatterPlot', data => {
      this.ScatterPlotResults = data})
    EventBus.$on('emittedEventCallingScatterPlot', this.ScatterPlotView)
    EventBus.$on('getColors', data => {
      this.colorsforOver = data})
    EventBus.$on('getColors', this.UpdateScatter),
    EventBus.$on('RepresentationSelection', data => {this.representationDefault = data})
    EventBus.$on('RepresentationSelection', this.ScatterPlotView)
  }
}
</script>