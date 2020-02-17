<template>
<div>
  <b-row class="md-3">
    <b-col cols="12">
      <div>Projection Selection: <select id="selectBarChartPred" @change="selectVisualRepresentationPred()">
        <option value="mds" selected>MDS Projection</option>
        <option value="tsne">t-SNE Projection</option>
        <option value="umap">UMAP Projection</option>
      </select>
      <div id="OverviewPredPlotly" class="OverviewPredPlotly"></div>
      </div>
    </b-col>
  </b-row>
</div>
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
      representationDef: 'mds',
      representationSelection: 'mds',
      colorsValues: ['#b3e2cd','#fdcdac','#cbd5e8','#f4cae4','#e6f5c9','#fff2ae','#f1e2cc'],
      WH: []
    }
  },
  methods: {
    selectVisualRepresentationPred () {
      const representationSelectionDocum = document.getElementById('selectBarChartPred')
      this.representationSelection = representationSelectionDocum.options[representationSelectionDocum.selectedIndex].value
      EventBus.$emit('RepresentationSelectionPred', this.representationSelection)
    },
    reset () {
      Plotly.purge('OverviewPredPlotly')
    },
    ScatterPlotPredView () {
       Plotly.purge('OverviewPredPlotly')

      // responsive visualization
      var width = this.WH[0]*6.5 // interactive visualization
      var height = this.WH[1]*1.22 // interactive visualization

      var target_names = JSON.parse(this.PredictionsData[4])
      const XandYCoordinatesMDS = JSON.parse(this.PredictionsData[8])
      const DataSet = JSON.parse(this.PredictionsData[14])
      const DataSetY = JSON.parse(this.PredictionsData[15])
      const originalDataLabels = JSON.parse(this.PredictionsData[16])
      var DataSetParse = JSON.parse(DataSet)
      const XandYCoordinatesTSNE = JSON.parse(this.PredictionsData[18])
      const XandYCoordinatesUMAP= JSON.parse(this.PredictionsData[19])

      var result = [];
      var IDs = [];
      var Xaxs = [];
      var Yaxs = [];

      if (this.representationDef == 'mds') {
        for (let i = 0; i < XandYCoordinatesMDS[0].length; i++) {
          Xaxs.push(XandYCoordinatesMDS[0][i])
          Yaxs.push(XandYCoordinatesMDS[1][i])
          IDs.push(i)
        }
        result.Xax = Xaxs
        result.Yax = Yaxs
        result.ID = IDs

        var traces = []
        var layout = []

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

        layout = {
        title: 'Predictions Space Projection (MDS)',
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
      } else if (this.representationDef == 'tsne') {
        result = XandYCoordinatesTSNE.reduce(function(r, a) {
          var id = 0
          a.forEach(function(s, i) {
              var key = i === 0 ? 'Xax' : 'Yax'

              r[key] || (r[key] = []) // if key not found on result object, add the key with empty array as the value

              r[key].push(s)

          })

            return r
        }, {})

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

        layout = {
        title: 'Prediction Space Projection (t-SNE)',
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
      } else {
        for (let i = 0; i < XandYCoordinatesUMAP[0].length; i++) {
          Xaxs.push(XandYCoordinatesUMAP[0][i])
          Yaxs.push(XandYCoordinatesUMAP[1][i])
          IDs.push(i)
        }
        result.Xax = Xaxs
        result.Yax = Yaxs
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

        layout = {
        title: 'Predictions Space Projection (UMAP)',
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
    EventBus.$on('emittedEventCallingPredictionsSpacePlotView', this.ScatterPlotPredView)
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})

    EventBus.$on('RepresentationSelectionPred', data => {this.representationDef = data})
    EventBus.$on('RepresentationSelectionPred', this.ScatterPlotPredView)

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }
}
</script>