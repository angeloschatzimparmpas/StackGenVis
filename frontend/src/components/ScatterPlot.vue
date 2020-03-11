<template>
<div>
  <div align="center">
            Projection Method: <select id="selectBarChart" @change="selectVisualRepresentation()">
              <option value="mds" selected>MDS</option>
              <option value="tsne">t-SNE</option>
              <option value="umap">UMAP</option>
            </select>
            &nbsp;&nbsp;
            Action: <button
            id="RemoveStack"
            v-on:click="RemoveStack">
            <font-awesome-icon icon="minus" />
            {{ valueStackRemove }}
            </button>
            &nbsp;&nbsp;
            Filter: <button
            id="ResetSelection"
            v-on:click="resetSelection">
            <font-awesome-icon icon="sync-alt" />
            {{ valueResetSel }}
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
      newColorsUpdate: [],
      parametersAll: [],
      length: 0,
      valueStackRemove: 'Remove Unselected from Stack',
      DataPointsSelUpdate: [],
      ModelsIDGray: [],
      valueResetSel: 'Reset Metric Selection',
      newStackPoints: '',
      colorsStore: [],
      MDSStore: [],
      parametersStore: [],
      TSNEStore: [],
      modelIDStore: [],
      UMAPStore: [],
      keyLocal: 0,
      activeModels: 0,
      pushModelsRemaining: [],
      onlyOnce: true
    }
  },
  methods: {
    resetSelection () {
      this.newColorsUpdate = []
      EventBus.$emit('updateBold', '')
      EventBus.$emit('updateBoxPlots')
      this.colorsStore = []
      this.MDSStore = []
      this.parametersStore = []
      this.TSNEStore = []
      this.modelIDStore = []
      this.UMAPStore = []
      this.ScatterPlotView()
    },
    reset () {
      Plotly.purge('OverviewPlotly')
    },
    selectVisualRepresentation () {
      const representationSelectionDocum = document.getElementById('selectBarChart')
      this.representationSelection = representationSelectionDocum.options[representationSelectionDocum.selectedIndex].value
      EventBus.$emit('RepresentationSelection', this.representationSelection)
    },
    RemoveStack () {
      EventBus.$emit('RemoveFromStack', this.pushModelsRemaining)
    },
    clean(obj) {
      var propNames = Object.getOwnPropertyNames(obj);
      for (var i = 0; i < propNames.length; i++) {
        var propName = propNames[i];
        if (obj[propName] === null || obj[propName] === undefined) {
          delete obj[propName];
        }
      }
    },
    ScatterPlotView () {
      Plotly.purge('OverviewPlotly')
      var colorsforScatterPlot
      var MDSData

      colorsforScatterPlot = JSON.parse(this.ScatterPlotResults[0])
      if (this.newColorsUpdate.length != 0) {
        colorsforScatterPlot = []
        let resultsClear = JSON.parse(this.newColorsUpdate)
        for (let j = 0; j < Object.values(resultsClear).length; j++) {
          colorsforScatterPlot.push(Object.values(resultsClear)[j])
        }
      }

      MDSData= JSON.parse(this.ScatterPlotResults[1])

      var parametersLoc = JSON.parse(this.ScatterPlotResults[2])
      var parameters = JSON.parse(parametersLoc)
      var TSNEData = JSON.parse(this.ScatterPlotResults[12])
      var modelId = JSON.parse(this.ScatterPlotResults[13])
      var UMAPData = JSON.parse(this.ScatterPlotResults[17])
      if (this.keyLocal == 0) {
        this.colorsStore.push(colorsforScatterPlot)
        this.MDSStore.push(MDSData)
        this.parametersStore.push(parameters)
        this.TSNEStore.push(TSNEData)
        this.modelIDStore.push(modelId)
        this.UMAPStore.push(UMAPData)
        colorsforScatterPlot = this.colorsStore.slice(this.activeModels,this.activeModels+1)[0]
        MDSData = this.MDSStore.slice(this.activeModels,this.activeModels+1)[0]
        parameters = this.parametersStore.slice(this.activeModels,this.activeModels+1)[0]
        TSNEData = this.TSNEStore.slice(this.activeModels,this.activeModels+1)[0]
        modelId = this.modelIDStore.slice(this.activeModels,this.activeModels+1)[0]
        UMAPData = this.UMAPStore.slice(this.activeModels,this.activeModels+1)[0]
      }

      EventBus.$emit('sendPointsNumber', modelId.length)

      var stringParameters = []
      for (let i = 0; i < parameters.length; i++) {
        this.clean(parameters[i])
        stringParameters.push(JSON.stringify(parameters[i]).replace(/,/gi, '<br>'))
      }

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
        classifiersInfoProcessing[i] = 'Model ID: ' + modelId[i] + '<br> Details: ' + stringParameters[i]
      }

      var listofNumbersModelsIDs = []
      var StackModelsIDs = []
      console.log(this.ModelsIDGray.length)
      if (this.ModelsIDGray.length != 0) {
        for (let j = 0; j < this.ModelsIDGray.length; j++){
          listofNumbersModelsIDs.push(parseInt(this.ModelsIDGray[j]))
        }

        var parametersNew = []
        var MDSDataNewX = []
        var MDSDataNewY = []
        var colorsforScatterPlotNew = []

        if (this.DataPointsSelUpdate.length != 0) {
          this.colorsStore.pop()
          this.MDSStore.pop()
          this.parametersStore.pop()
          this.modelIDStore.pop()
          this.UMAPStore.pop()
        }

        for (let i = 0; i < modelId.length; i++) {
          if (listofNumbersModelsIDs.includes(modelId[i])) {
            StackModelsIDs.push(modelId[i])
            parametersNew.push(parameters[i])
            if (this.DataPointsSelUpdate.length != 0) {
              colorsforScatterPlot = JSON.parse(this.DataPointsSelUpdate[0])
              colorsforScatterPlotNew.push(colorsforScatterPlot[i])
            } else {
              colorsforScatterPlotNew.push(colorsforScatterPlot[i])
            }
            if (this.DataPointsSelUpdate.length != 0) {
              MDSData = JSON.parse(this.DataPointsSelUpdate[1])
              MDSDataNewX.push(MDSData[0][i])
              MDSDataNewY.push(MDSData[1][i])
            } else {
              MDSDataNewX.push(MDSData[0][i])
              MDSDataNewY.push(MDSData[1][i])
            }
          }
        }
        this.DataPointsSelUpdate = []
        MDSData[0] = MDSDataNewX
        MDSData[1] = MDSDataNewY
        console.log(StackModelsIDs)
        modelId = StackModelsIDs
        parameters = parametersNew
        colorsforScatterPlot = colorsforScatterPlotNew
        if (this.keyLocal == 1) {
          this.colorsStore.push(colorsforScatterPlot)
          this.MDSStore.push(MDSData)
          this.parametersStore.push(parameters)
          //this.TSNEStore.push(TSNEData)
          this.modelIDStore.push(modelId)
          this.UMAPStore.push(UMAPData)
          console.log(this.activeModels)
          colorsforScatterPlot = this.colorsStore.slice(this.activeModels,this.activeModels+1)[0]
          MDSData = this.MDSStore.slice(this.activeModels,this.activeModels+1)[0]
          parameters = this.parametersStore.slice(this.activeModels,this.activeModels+1)[0]
          //TSNEData = this.TSNEStore.slice(this.activeModels,this.activeModels+1)[0]
          modelId = this.modelIDStore.slice(this.activeModels,this.activeModels+1)[0]
          console.log(modelId)
          //UMAPData = this.UMAPStore.slice(this.activeModels,this.activeModels+1)[0]
        }


        console.log(this.colorsStore)
        console.log(colorsforScatterPlot)
        EventBus.$emit('sendPointsNumber', modelId.length)
        var classifiersInfoProcessing = []
        for (let i = 0; i < modelId.length; i++) {
          classifiersInfoProcessing[i] = 'Model ID: ' + modelId[i] + '; Details: ' + stringParameters[i]
        }
        EventBus.$emit('NewHeatmapAccordingtoNewStack', modelId)

      }
      var DataGeneral

      var maxX
      var minX
      var maxY
      var minY

      var width = this.WH[0]*6.5 // interactive visualization
      var height = this.WH[1]*1.22 // interactive visualization

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
           line: { color: 'rgb(0, 0, 0)', width: 3 },
            color: colorsforScatterPlot,
            size: 12,
            colorscale: 'Viridis',
            colorbar: {
              title: '# Performance (%) #',
              titleside:'right',
            },
          }
        
        }]
        layout = {

          xaxis: {
              visible: false,
              range: [minX, maxX]
          },
          yaxis: {
              visible: false,
              range: [minY, maxY]
          },
          font: { family: 'Helvetica', size: 16, color: '#000000' },
          autosize: true,
          width: width,
          height: height,
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', y: -0.3},
          margin: {
            l: 50,
            r: 0,
            b: 30,
            t: 40,
            pad: 0
          },
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
              line: { color: 'rgb(0, 0, 0)', width: 3 },
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
          margin: {
            l: 50,
            r: 0,
            b: 30,
            t: 40,
            pad: 0
          },
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
           line: { color: 'rgb(0, 0, 0)', width: 3 },
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
          margin: {
            l: 50,
            r: 0,
            b: 30,
            t: 40,
            pad: 0
          },
        }
      }
     
      var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian','zoomIn2d','zoomOut2d','zoom2d'], responsive: true}
      
      var scat = document.getElementById('OverviewPlotly')
      
      Plotly.newPlot(scat, DataGeneral, layout, config)
      if (this.onlyOnce) {
        this.selectedPointsOverview()
      }
    },
    selectedPointsOverview () {
      const OverviewPlotly = document.getElementById('OverviewPlotly')
      var allModels = JSON.parse(this.ScatterPlotResults[13])
      OverviewPlotly.on('plotly_selected', function (evt) {
        if (typeof evt !== 'undefined') {
          var pushModelsRemainingTemp = []
          const ClassifierIDsList = []
          const ClassifierIDsListCleared = []
          for (let i = 0; evt.points.length; i++) {
            if (evt.points[i] === undefined) {
              break
            } else {
              const OnlyId = evt.points[i].text.split(' ')[2]
              const OnlyIdCleared = OnlyId.split('<br>')
              ClassifierIDsList.push(OnlyIdCleared[0])
              let numberNumb = parseInt(OnlyIdCleared[0])
              ClassifierIDsListCleared.push(numberNumb)
            }
          }
          console.log(ClassifierIDsListCleared)
          for (let i = 0; i < allModels.length; i++) {
            if (!ClassifierIDsListCleared.includes(allModels[i])) {
              pushModelsRemainingTemp.push(allModels[i])
            }
          }
          console.log(pushModelsRemainingTemp)
            EventBus.$emit('updateRemaining', pushModelsRemainingTemp)
          if (allModels != '') {
            EventBus.$emit('ChangeKey', 1)
            EventBus.$emit('SendSelectedPointsToServerEvent', ClassifierIDsListCleared)
            EventBus.$emit('SendSelectedPointsToBrushHeatmap', ClassifierIDsListCleared)
          } else {
            EventBus.$emit('ChangeKey', 1)
          }
        }
      })
    },
    UpdateScatter () {
      this.ScatterPlotView()
    },
  //   animate() {
  //     var maxX
  //     var minX
  //     var maxY
  //     var minY

  //     var colorsforScatterPlot = JSON.parse(this.DataPointsSelUpdate[0])
  //     var MDSData = JSON.parse(this.DataPointsSelUpdate[1])

  //     maxX = Math.max(MDSData[0])
  //     minX = Math.min(MDSData[0])
  //     maxY = Math.max(MDSData[1])
  //     minY = Math.max(MDSData[1])

  //     Plotly.animate('OverviewPlotly', {
  //       data: [
  //         {x: MDSData[0], y: MDSData[1],marker: {
  //             color: colorsforScatterPlot,
  //             }}
  //       ],
  //       traces: [0],
  //       layout: {
  //         xaxis: {
  //             visible: false,
  //             range: [minX, maxX]
  //         },
  //         yaxis: {
  //             visible: false,
  //             range: [minY, maxY]
  //         },
  //       }
  //     }, {
  //       transition: {
  //         duration: 3000,
  //         easing: 'cubic-in-out'
  //       },
  //       frame: {
  //         duration: 3000
  //       }
  //     })
  //   }
  },
  mounted() {
    EventBus.$on('onlyOnce', data => { this.onlyOnce = data })

    EventBus.$on('updateMetricsScatter', data => { this.newColorsUpdate = data })
    EventBus.$on('updateMetricsScatter', this.ScatterPlotView)

    EventBus.$on('updateRemaining', data => { this.pushModelsRemaining = data })

    EventBus.$on('requestProven', data => { this.activeModels = data })

    EventBus.$on('sendKeyScatt', data => { this.keyLocal = data })

    EventBus.$on('newPointsStack', data => { this.newStackPoints = data })
    EventBus.$on('newPointsStack', this.ScatterPlotView)

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
    EventBus.$on('UpdateModelsScatterplot', this.ScatterPlotView)

    // reset view
    EventBus.$on('resetViews', this.reset)
  }
}
</script>