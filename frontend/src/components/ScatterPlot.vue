<template>
<div>
  <div align="center">
            Projection Selection: <select id="selectBarChart" @change="selectVisualRepresentation()">
              <option value="mds" selected>MDS Projection</option>
              <option value="tsne">t-SNE Projection</option>
              <option value="umap">UMAP Projection</option>
            </select>
            Action: <button
            id="RemoveStack"
            v-on:click="RemoveStack">
            <font-awesome-icon icon="minus" />
            {{ valueStackRemove }}
            </button>
  </div>
  <div id="OverviewPlotly" class="OverviewPlotly"></div>
</div>
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
      representationDef: 'mds',
      representationSelection: 'mds',
      colorsforOver: [],
      brushedBox : [],
      max: 0,
      min: 0,
      WH: [],
      parametersAll: [],
      length: 0,
      valueStackRemove: 'Remove from Stack',
      DataPointsSelUpdate: [],
      ModelsIDGray: []
    }
  },
  methods: {
    reset () {
      Plotly.purge('OverviewPlotly')
    },
    selectVisualRepresentation () {
      const representationSelectionDocum = document.getElementById('selectBarChart')
      this.representationSelection = representationSelectionDocum.options[representationSelectionDocum.selectedIndex].value
      EventBus.$emit('RepresentationSelection', this.representationSelection)
    },
    RemoveStack () {
      EventBus.$emit('RemoveFromStack')
    },
    ScatterPlotView () {
      Plotly.purge('OverviewPlotly')
      var colorsforScatterPlot = JSON.parse(this.ScatterPlotResults[0])

      var MDSData = JSON.parse(this.ScatterPlotResults[1])
      var parameters = JSON.parse(this.ScatterPlotResults[2])
      var TSNEData = JSON.parse(this.ScatterPlotResults[12])
      var modelId = JSON.parse(this.ScatterPlotResults[13])
      var UMAPData = JSON.parse(this.ScatterPlotResults[17])

      EventBus.$emit('sendPointsNumber', modelId.length)

      parameters = JSON.parse(parameters)

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
      for (let i = 0; i < modelId.length; i++) {
        classifiersInfoProcessing[i] = 'Model ID: ' + modelId[i] + '; Details: ' + JSON.stringify(parameters[i])
      }

      var listofNumbersModelsIDs = []
      var StackModelsIDs = []
      if (this.ModelsIDGray.length != 0) {
        for (let j = 0; j < this.ModelsIDGray.length; j++){
          listofNumbersModelsIDs.push(parseInt(this.ModelsIDGray[j].replace(/\D/g, "")))
        }

        var parametersNew = []
        var MDSDataNewX = []
        var MDSDataNewY = []
        var colorsforScatterPlotNew = []
        for (let i = 0; i < modelId.length; i++) {
          if (listofNumbersModelsIDs.includes(modelId[i])) {
          } else {
            StackModelsIDs.push(modelId[i])
            parametersNew.push(parameters[i])
            colorsforScatterPlotNew.push(colorsforScatterPlot[i])
            MDSDataNewX.push(MDSData[0][i])
            MDSDataNewY.push(MDSData[1][i])
          }
        }
        EventBus.$emit('sendPointsNumber', StackModelsIDs.length)
        var classifiersInfoProcessing = []
        for (let i = 0; i < StackModelsIDs.length; i++) {
          classifiersInfoProcessing[i] = 'Model ID: ' + StackModelsIDs[i] + '; Details: ' + JSON.stringify(parametersNew[i])
        }
        MDSData[0] = MDSDataNewX
        MDSData[1] = MDSDataNewY
        colorsforScatterPlot = colorsforScatterPlotNew
        EventBus.$emit('NewHeatmapAccordingtoNewStack', StackModelsIDs)
      }
      var DataGeneral

      var maxX
      var minX
      var maxY
      var minY

      var layout
      if (this.representationDef == 'mds') {
        maxX = Math.max(MDSData[0])
        minX = Math.min(MDSData[0])
        maxY = Math.max(MDSData[1])
        minY = Math.max(MDSData[1])

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
           line: { color: 'rgb(0, 0, 0)', width: 2 },
            color: colorsforScatterPlot,
            size: 12,
            colorscale: 'Viridis',
            colorbar: {
              title: 'Metrics Average',
              titleside: 'Top'
            },
          }
        
        }]
        var width = this.WH[0]*6.5 // interactive visualization
        var height = this.WH[1]*1.22 // interactive visualization
        layout = {
          title: 'Models Performance (MDS)',
          xaxis: {
              visible: false,
              range: [minX, maxX]
          },
          yaxis: {
              visible: false,
              range: [minY, maxY]
          },
          autosize: true,
          width: width,
          height: height,
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', y: -0.3},
        }
      } else if (this.representationDef == 'tsne') {
        var result = TSNEData.reduce(function(r, a) {
            a.forEach(function(s, i) {
                var key = i === 0 ? 'Xax' : 'Yax';

                r[key] || (r[key] = []); // if key not found on result object, add the key with empty array as the value

                r[key].push(s);
            })
            return r;
        }, {})

        maxX = Math.max(result.Xax)
        minX = Math.min(result.Xax)
        maxY = Math.max(result.Yax)
        minY = Math.max(result.Yax)

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
                title: 'Metrics Average',
                titleside: 'Top'
              },
          }
        }]
        layout = {
          title: 'Models Performance (t-SNE)',
          xaxis: {
              visible: false,
              range: [minX, maxX]
          },
          yaxis: {
              visible: false,
              range: [minY, maxY]
          },
          autosize: true,
          width: width,
          height: height,
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', y: -0.3},
        }

      } else {
        maxX = Math.max(UMAPData[0])
        minX = Math.min(UMAPData[0])
        maxY = Math.max(UMAPData[1])
        minY = Math.max(UMAPData[1])

        DataGeneral = [{
          type: 'scatter',
          mode: 'markers',
          x: UMAPData[0],
          y: UMAPData[1],
          hovertemplate: 
                "<b>%{text}</b><br><br>" +
                "<extra></extra>",
          text: classifiersInfoProcessing,
          marker: {
           line: { color: 'rgb(0, 0, 0)', width: 2 },
            color: colorsforScatterPlot,
            size: 12,
            colorscale: 'Viridis',
            colorbar: {
              title: 'Metrics Average',
              titleside: 'Top'
            },
          }
        
        }]
        var width = this.WH[0]*6.5 // interactive visualization
        var height = this.WH[1]*1 // interactive visualization
        layout = {
          title: 'Models Performance (UMAP)',
          xaxis: {
              visible: false,
              range: [minX, maxX]
          },
          yaxis: {
              visible: false,
              range: [minY, maxY]
          },
          autosize: true,
          width: width,
          height: height,
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', y: -0.3},
        }
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
          const ClassifierIDsListCleared = []
          for (let i = 0; evt.points.length; i++) {
            if (evt.points[i] === undefined) {
              break
            } else {
              const OnlyId = evt.points[i].text.split(';')
              ClassifierIDsList.push(OnlyId[0])
              let numb = OnlyId[0].match(/\d/g);
              numb = numb.join("");
              let numberNumb = Number(numb)
              ClassifierIDsListCleared.push(numberNumb)
            }
          }
          if (ClassifierIDsList != '') {
            EventBus.$emit('SendSelectedPointsToServerEvent', ClassifierIDsList)
            EventBus.$emit('SendSelectedPointsToBrushHeatmap', ClassifierIDsListCleared)
          } else {
            EventBus.$emit('SendSelectedPointsToServerEvent', '')
          }
        }
      })
    },
    UpdateScatter () {
      this.ScatterPlotView()
    },
    animate() {
      var maxX
      var minX
      var maxY
      var minY

      var colorsforScatterPlot = JSON.parse(this.DataPointsSelUpdate[0])
      var MDSData = JSON.parse(this.DataPointsSelUpdate[1])

      maxX = Math.max(MDSData[0])
      minX = Math.min(MDSData[0])
      maxY = Math.max(MDSData[1])
      minY = Math.max(MDSData[1])

      Plotly.animate('OverviewPlotly', {
        data: [
          {x: MDSData[0], y: MDSData[1],marker: {
              color: colorsforScatterPlot,
              }}
        ],
        traces: [0],
        layout: {
          xaxis: {
              visible: false,
              range: [minX, maxX]
          },
          yaxis: {
              visible: false,
              range: [minY, maxY]
          },
        }
      }, {
        transition: {
          duration: 3000,
          easing: 'cubic-in-out'
        },
        frame: {
          duration: 3000
        }
      })
    }
  },
  mounted() {
    EventBus.$on('GrayOutPoints', data => { this.ModelsIDGray = data })
    EventBus.$on('GrayOutPoints', this.ScatterPlotView)
    EventBus.$on('emittedEventCallingBrushedBoxPlot', data => {
      this.brushedBox = data})
    EventBus.$on('emittedEventCallingScatterPlot', data => {
      this.ScatterPlotResults = data})
    EventBus.$on('emittedEventCallingScatterPlot', this.ScatterPlotView)
    EventBus.$on('getColors', data => {
      this.colorsforOver = data})
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})
    EventBus.$on('ParametersAll',  data => { this.parametersAll = data })
    EventBus.$on('getColors', this.UpdateScatter)
    EventBus.$on('RepresentationSelection', data => {this.representationDef = data})
    EventBus.$on('RepresentationSelection', this.ScatterPlotView)
    EventBus.$on('UpdateModelsScatterplot', data => {this.DataPointsSelUpdate = data})
    EventBus.$on('UpdateModelsScatterplot', this.animate)

    // reset view
    EventBus.$on('resetViews', this.reset)
  }
}
</script>