<template>
  <div id="OverviewPredPlotly" class="OverviewPredPlotly"></div>
</template>

<script>
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'PredictionsSpace',
  data () {
    return {
      PredictionsData: '',
      WH: []
    }
  },
  methods: {
    ScatterPlotDataView () {
        const XandYCoordinates = JSON.parse(this.PredictionsData[8])

        var result = XandYCoordinates.reduce(function(r, a) {
            a.forEach(function(s, i) {
                var key = i === 0 ? 'Xax' : 'Yax';

                r[key] || (r[key] = []); // if key not found on result object, add the key with empty array as the value

                r[key].push(s);
            })
            return r;
        }, {})

        var dataPointInfo = []
        for (let i = 0; i < XandYCoordinates.length; i++) {
          dataPointInfo[i] = 'Data Point ID: ' + i
        }

        var width = this.WH[0]*3 // interactive visualization
        var height = this.WH[1]*1.48 // interactive visualization
        const Data = [{
        x: result.Xax,
        y: result.Yax,
        mode: 'markers',
        hovertemplate: 
                "<b>%{text}</b><br><br>" +
                "<extra></extra>",
        text: dataPointInfo,
        }]
        const layout = {
        title: 'Predictions Space Projection (tSNE)',
        xaxis: {
            visible: false
        },
        yaxis: {
            visible: false
        },
        dragmode: 'lasso',
        hovermode: "closest",
        autosize: true,
        width: width,
        height: height,
        }

        var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian','zoomIn2d','zoomOut2d','zoom2d'], responsive: true}

        Plotly.newPlot('OverviewPredPlotly', Data, layout, config)
        this.selectedPointsOverview()
    },
    selectedPointsOverview () {
      const OverviewPlotly = document.getElementById('OverviewPredPlotly')
      OverviewPlotly.on('plotly_selected', function (evt) {
        if (typeof evt !== 'undefined') {
          const DataPoints = []
          for (let i = 0; evt.points.length; i++) {
            if (evt.points[i] === undefined) {
              break
            } else {
              const OnlyId = evt.points[i].text.split(' ')
              DataPoints.push(OnlyId[3])
            }
          }
          if (DataPoints != '') {
            EventBus.$emit('SendSelectedDataPointsToServerEvent', DataPoints)
          } else {
            EventBus.$emit('SendSelectedDataPointsToServerEvent', '')
          }
        }
      })
    },
  },
  mounted() {
    EventBus.$on('emittedEventCallingPredictionsSpacePlotView', data => {
      this.PredictionsData = data})
    EventBus.$on('emittedEventCallingPredictionsSpacePlotView', this.ScatterPlotDataView)
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})
  }
}
</script>