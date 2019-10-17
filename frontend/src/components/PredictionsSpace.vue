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
      WH: []
    }
  },
  methods: {
    ScatterPlotDataView () {
        var target_names = JSON.parse(this.PredictionsData[4])
        const XandYCoordinates = JSON.parse(this.PredictionsData[8])
        const DataSet = JSON.parse(this.PredictionsData[14])
        const DataSetY = JSON.parse(this.PredictionsData[15])
        var DataSetParse = JSON.parse(DataSet)

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
          dataPointInfo[i] = 'Data Point ID: ' + i + '; Details: ' + JSON.stringify(DataSetParse[i])
        }
        
        var colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']

         var traces = []
         var countPrev = 0
         var count = 0
         for (let i = 0; i < target_names.length; i++) {
          count = 0
          for (let j = 0; j < DataSetY.length; j++) {
            if (i == DataSetY[j]) {
              count = count + 1
            }
          }

          traces.push({
            x: result.Xax.slice(countPrev,count+countPrev),
            y: result.Yax.slice(countPrev,count+countPrev),
            mode: 'markers',
            name: target_names[i],
            marker: {
              color: colors[i]
            },
            hovertemplate: 
                    "<b>%{text}</b><br><br>" +
                    "<extra></extra>",
            text: dataPointInfo.slice(countPrev,count+countPrev),
          })
          countPrev = count + countPrev
        }
     
        var width = this.WH[0]*3 // interactive visualization
        var height = this.WH[1]*1.48 // interactive visualization

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
  }
}
</script>