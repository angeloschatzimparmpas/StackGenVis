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
      UpdatedData: '',
      colorsValues: ['#6a3d9a','#b15928','#e31a1c'],
      responsiveWidthHeight: []
    }
  },
  methods: {
    reset () {
      Plotly.purge('OverviewPredPlotly')
    },
    ScatterPlotDataView () {
       Plotly.purge('OverviewPredPlotly')

      // responsive visualization
      var width = this.responsiveWidthHeight[0]*3
      var height = this.responsiveWidthHeight[1]*1.48 

      var target_names = JSON.parse(this.PredictionsData[4])
      const XandYCoordinates = JSON.parse(this.PredictionsData[8])
      const DataSet = JSON.parse(this.PredictionsData[14])
      const DataSetY = JSON.parse(this.PredictionsData[15])
      const originalDataLabels = JSON.parse(this.PredictionsData[16])
      var DataSetParse = JSON.parse(DataSet)

      var result = XandYCoordinates.reduce(function(r, a) {
          a.forEach(function(s, i) {
              var key = i === 0 ? 'Xax' : 'Yax';

              r[key] || (r[key] = []); // if key not found on result object, add the key with empty array as the value

              r[key].push(s);
          })
          return r;
      }, {})

      var IDs = [];

      for (let i = 0; i < result.Xax.length; i++) {
        IDs.push(i)
      }
      result.ID = IDs
      
      var traces = []

      for (let i = 0; i < target_names.length; i++) {

        const aux_X = result.Xax.filter((item, index) => originalDataLabels[index] == target_names[i]);
        const aux_Y = result.Yax.filter((item, index) => originalDataLabels[index] == target_names[i]);
        const aux_ID = result.ID.filter((item, index) => originalDataLabels[index] == target_names[i]);

        var Text = aux_ID.map((item, index) => {
          let popup = 'Data Point ID: ' + item + '; Details: ' + JSON.stringify(DataSetParse[item])
          return popup;
        });

        traces.push({
            x: aux_X,
            y: aux_Y,
            mode: 'markers',
            name: target_names[i],
            marker: { color: this.colorsValues[i], line: { color: 'rgb(0, 0, 0)', width: 2 }, opacity: 1, size: 12 },
            hovertemplate: 
                    "<b>%{text}</b><br><br>" +
                    "<extra></extra>",
            text: Text,
          })
      }

      const layout = {
      title: 'Predictions Space Projection (t-SNE)',
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

      Plotly.newPlot('OverviewPredPlotly', traces, layout, config)
      this.selectedPointsOverview()
    },
    UpdateScatterPlot () {
      const XandYCoordinates = JSON.parse(this.UpdatedData[0])

      Plotly.animate('OverviewPredPlotly', {
        data: [
          {x: XandYCoordinates[0], y: XandYCoordinates[1]}
        ],
        traces: [0],
        layout: {}
      }, {
        transition: {
          duration: 1000,
          easing: 'cubic-in-out'
        },
        frame: {
          duration: 1000
        }
      })
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
    EventBus.$on('updatePredictionsSpace', data => { this.UpdatedData = data })
    EventBus.$on('updatePredictionsSpace', this.UpdateScatterPlot)
    EventBus.$on('emittedEventCallingPredictionsSpacePlotView', data => {
      this.PredictionsData = data})
    EventBus.$on('emittedEventCallingPredictionsSpacePlotView', this.ScatterPlotDataView)
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }
}
</script>