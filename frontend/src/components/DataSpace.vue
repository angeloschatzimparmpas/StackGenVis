<template>
  <div>
    <div align="center">
      Projection Method: <select id="selectBarChartData" @change="selectVisualRepresentationData()">
        <option value="mds">MDS</option>
        <option value="tsne" selected>t-SNE</option>
        <option value="umap">UMAP</option>
      </select>
      &nbsp;&nbsp;
      Filter: <select id="selectFilterID" @change="selectAppliedFilter()">
        <option value="mean" selected>Mean</option>
        <option value="median">Median</option>
      </select>
      &nbsp;&nbsp;
      Action: <button
      id="mergeID"
      v-on:click="merge">
      <font-awesome-icon icon="object-group" />
      {{ mergeData }}
      </button>
      <button
      id="composeID"
      v-on:click="compose">
      <font-awesome-icon icon="clone" />
      {{ composeData }}
      </button>
      <button
      id="removeID"
      v-on:click="remove">
      <font-awesome-icon icon="eraser" />
      {{ removeData }}
      </button>
      &nbsp;&nbsp;<br>
      History Manager: <button
      id="saveID"
      v-on:click="save">
      <font-awesome-icon icon="save" />
      {{ saveData }}
      </button>
      <button
      id="restoreID"
      v-on:click="restore">
      <font-awesome-icon icon="undo" />
      {{ restoreData }}
      </button>
    </div>
    <div id="OverviewDataPlotly" class="OverviewDataPlotly"></div>
  </div>
</template>

<script>
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'DataSpace',
  data () {
    return {
      dataPoints: '',
      highlightedPoints: '',
      representationDef: 'tsne',
      representationSelection: 'tsne',
      mergeData: 'Merge',
      removeData: 'Remove',
      composeData: 'Compose',
      saveData: 'Save Step',
      restoreData: 'Restore Step',
      userSelectedFilter: 'mean',
      responsiveWidthHeight: [],
      RetrieveDataSet: 'HeartC',
      colorsValues: ['#808000','#008080','#bebada','#fccde5','#d9d9d9','#bc80bd','#ccebc5'],
      onlyOnce: true,
      restylePoints: [],
      smallScreenMode: '0px'
    }
  },
  methods: {
    selectVisualRepresentationData () {
      const representationSelectionDocum = document.getElementById('selectBarChartData')
      this.representationSelection = representationSelectionDocum.options[representationSelectionDocum.selectedIndex].value
      EventBus.$emit('RepresentationSelectionData', this.representationSelection)
    },
    reset () {
      Plotly.purge('OverviewDataPlotly')
    },
    selectAppliedFilter () {
      var representationSelectionDocum = document.getElementById('selectFilterID')
      this.userSelectedFilter = representationSelectionDocum.options[representationSelectionDocum.selectedIndex].value
      EventBus.$emit('SendFilter', this.userSelectedFilter)
    },
    merge() {
      this.restylePoints = []
      EventBus.$emit('SendAction', 'merge')
      EventBus.$emit('SendSelectedPointsToServerEventfromData', [])
    },
    remove () {
      this.restylePoints = []
      EventBus.$emit('SendAction', 'remove')
      EventBus.$emit('SendSelectedPointsToServerEventfromData', [])
    },
    compose () {
      this.restylePoints = []
      EventBus.$emit('SendAction', 'compose')
      EventBus.$emit('SendSelectedPointsToServerEventfromData', [])
    },
    save () {
      this.restylePoints = []
      EventBus.$emit('SendProvenance', 'save')
      EventBus.$emit('SendSelectedPointsToServerEventfromData', [])
    },
    restore () {
      this.restylePoints = []
      EventBus.$emit('SendProvenance', 'restore')
      EventBus.$emit('SendSelectedPointsToServerEventfromData', [])
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
    scatterPlotDataView () {
      Plotly.purge('OverviewDataPlotly')
        
      if (this.smallScreenMode != "370px") {
        // responsive visualization
        var width = this.responsiveWidthHeight[0]*6.5
        var height = this.responsiveWidthHeight[1]*0.85
      } else {
        var width = this.responsiveWidthHeight[0]*6.5
        var height = this.responsiveWidthHeight[1]*0.83
      }

      var target_names = JSON.parse(this.dataPoints[0])
      const XandYCoordinatesMDS = JSON.parse(this.dataPoints[1])
      const DataSet = JSON.parse(this.dataPoints[2])
      const originalDataLabels = JSON.parse(this.dataPoints[3])

      //console.log(DataSetY)
      //const originalDataLabels = JSON.parse(this.dataPoints[4])
      var DataSetParse = JSON.parse(DataSet)
      var stringParameters = []
      for (let i = 0; i < DataSetParse.length; i++) {
        this.clean(DataSetParse[i])
        stringParameters.push(JSON.stringify(DataSetParse[i]).replace(/,/gi, '<br>'))
      }
      const XandYCoordinatesTSNE = JSON.parse(this.dataPoints[5])
      const XandYCoordinatesUMAP = JSON.parse(this.dataPoints[6])
      const impSizeArray = JSON.parse(this.dataPoints[7])

      var sizeScatterplot = []

      var scale = d3.scaleLinear()
        .domain([0,1])
        .range([10,20]);

      for (let i = 0; i < impSizeArray.length; i++) {
        sizeScatterplot.push(scale(impSizeArray[i]))
      }

      let intData = []
      if (this.highlightedPoints.length > 0){
        this.restylePoints = []
        let removedPuncData = this.highlightedPoints.map(function(x){return x.replace(';', '');})
        intData = removedPuncData.map(Number)
      } else {
        intData = []
      }

      var result = []
      var IDs = []
      var Xaxs = []
      var Yaxs = []
      var Opacity
      var colorUpdate = []

      var beautifyLabels = []
      if (this.RetrieveDataSet == 'StanceC') {
        beautifyLabels.push('Absence of Hypotheticality')
        beautifyLabels.push('Presence of Hypotheticality')
      }
      else if (this.RetrieveDataSet == 'HeartC') {
        beautifyLabels.push('< 50% Diameter Narrowing / Healthy')
        beautifyLabels.push('> 50% Diameter Narrowing / Diseased')
      } else {
        target_names.forEach(element => {
          beautifyLabels.push(element)
        });
        target_names = []
        target_names.push(0)
        target_names.push(1)
        target_names.push(2)
      }

      if (this.representationDef == 'mds') {
        for (let i = 0; i < XandYCoordinatesMDS[0].length; i++) {
          Xaxs.push(XandYCoordinatesMDS[0][i])
          Yaxs.push(XandYCoordinatesMDS[1][i])
          IDs.push(i)
          if (this.restylePoints.length != 0) {
            if (XandYCoordinatesMDS[0].length == this.restylePoints.length) {
              colorUpdate.push('rgb(0, 0, 0)')
            } else {
              if (this.restylePoints.includes(i)) {
                  colorUpdate.push('rgb(175, 68, 39)')
                } else {
                  colorUpdate.push('rgb(0, 0, 0)')
                }
              }
            } else {
                  colorUpdate.push('rgb(0, 0, 0)')
            }
        }
        result.Xax = Xaxs
        result.Yax = Yaxs
        result.ID = IDs
        result.colorUpdates = colorUpdate

        var traces = []
        var layout = []
        for (let i = 0; i < target_names.length; i++) {

          const aux_X = result.Xax.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_Y = result.Yax.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_ID = result.ID.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_colorUpdates = result.colorUpdates.filter((item, index) => originalDataLabels[index] == target_names[i]);

          var Text = aux_ID.map((item, index) => {
            let popup = 'Data Point ID: ' + item + '<br> Details: ' + stringParameters[item]
            return popup;
          });

          Opacity = aux_ID.map((item, index) => {
            let opac
            if (intData.length == 0) {
              opac = 1
            } else if (intData.indexOf(item) > -1) {
              opac = 1
            } else {
              opac = 0.5
            }
            return opac;
          });

          traces.push({
              x: aux_X,
              y: aux_Y,
              mode: 'markers',
              name: beautifyLabels[i],
              marker: { color: this.colorsValues[i], line: { color: aux_colorUpdates[i], width: 3 }, opacity: Opacity, size: sizeScatterplot },
              hovertemplate: 
                      "<b>%{text}</b><br><br>" +
                      "<extra></extra>",
              text: Text,
            })
        }

        layout = {font: { family: 'Helvetica', size: 14, color: '#000000' },
        legend: {orientation: 'h', xanchor: 'center', x: 0.5},
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
        margin: {
            l: 50,
            r: 0,
            b: 30,
            t: 40,
            pad: 0
          },
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
          if (this.restylePoints.length != 0) {
            if (XandYCoordinatesMDS[0].length == this.restylePoints.length) {
              colorUpdate.push('rgb(0, 0, 0)')
            } else {
              if (this.restylePoints.includes(i)) {
                  colorUpdate.push('rgb(175, 68, 39)')
                } else {
                  colorUpdate.push('rgb(0, 0, 0)')
                }
              }
            } else {
              colorUpdate.push('rgb(0, 0, 0)')
          }
        }
        result.ID = IDs
        result.colorUpdates = colorUpdate
        
        var traces = []

        for (let i = 0; i < target_names.length; i++) {

          const aux_X = result.Xax.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_Y = result.Yax.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_ID = result.ID.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_colorUpdates = result.colorUpdates.filter((item, index) => originalDataLabels[index] == target_names[i]);

          var Text = aux_ID.map((item, index) => {
            let popup = 'Data Point ID: ' + item + '<br> Details: ' + stringParameters[item]
            return popup;
          });

          Opacity = aux_ID.map((item, index) => {
            let opac
            if (intData.length == 0) {
              opac = 1
            } else if (intData.indexOf(item) > -1) {
              opac = 1
            } else {
              opac = 0.5
            }
            return opac;
          });

          traces.push({
            x: aux_X,
            y: aux_Y,
            mode: 'markers',
            name: beautifyLabels[i],
            marker: { color: this.colorsValues[i], line: { color: aux_colorUpdates, width: 3 }, opacity: Opacity, size: sizeScatterplot },
            hovertemplate: 
                    "<b>%{text}</b><br><br>" +
                    "<extra></extra>",
            text: Text,
          })
        }

        layout = {font: { family: 'Helvetica', size: 14, color: '#000000' },
        legend: {orientation: 'h', xanchor: 'center', x: 0.5},
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
        margin: {
            l: 50,
            r: 0,
            b: 30,
            t: 40,
            pad: 0
          },
        }
      } else {
        for (let i = 0; i < XandYCoordinatesUMAP[0].length; i++) {
          Xaxs.push(XandYCoordinatesUMAP[0][i])
          Yaxs.push(XandYCoordinatesUMAP[1][i])
          IDs.push(i)
          if (this.restylePoints.length != 0) {
            if (XandYCoordinatesMDS[0].length == this.restylePoints.length) {
              colorUpdate.push('rgb(0, 0, 0)')
            } else {
              if (this.restylePoints.includes(i)) {
                  colorUpdate.push('rgb(175, 68, 39)')
                } else {
                  colorUpdate.push('rgb(0, 0, 0)')
                }
              }
            } else {
              colorUpdate.push('rgb(0, 0, 0)')
            }
        }
        result.Xax = Xaxs
        result.Yax = Yaxs
        result.ID = IDs
        result.colorUpdates = colorUpdate

        var traces = []
        var layout = []

        var traces = []

        for (let i = 0; i < target_names.length; i++) {

          const aux_X = result.Xax.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_Y = result.Yax.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_ID = result.ID.filter((item, index) => originalDataLabels[index] == target_names[i]);
          const aux_colorUpdates = result.colorUpdates.filter((item, index) => originalDataLabels[index] == target_names[i]);

          var Text = aux_ID.map((item, index) => {
            let popup = 'Data Point ID: ' + item + '<br> Details: ' + stringParameters[item]
            return popup;
          });

          Opacity = aux_ID.map((item, index) => {
            let opac
            if (intData.length == 0) {
              opac = 1
            } else if (intData.indexOf(item) > -1) {
              opac = 1
            } else {
              opac = 0.5
            }
            return opac;
          });

          traces.push({
              x: aux_X,
              y: aux_Y,
              mode: 'markers',
              name: beautifyLabels[i],
              marker: { color: this.colorsValues[i], line: { color: aux_colorUpdates, width: 3 }, opacity: Opacity, size: sizeScatterplot },
              hovertemplate: 
                      "<b>%{text}</b><br><br>" +
                      "<extra></extra>",
              text: Text,
            })
        }

        layout = {font: { family: 'Helvetica', size: 14, color: '#000000' },
        legend: {orientation: 'h', xanchor: 'center', x: 0.5},
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

      Plotly.newPlot('OverviewDataPlotly', traces, layout, config)
      if (this.onlyOnce) {
        this.selectedDataPoints()
      }
      this.onlyOnce = false

    },
    selectedDataPoints () {
      const OverviewDataPlotly = document.getElementById('OverviewDataPlotly')
      OverviewDataPlotly.on('plotly_selected', function (evt) {
        if (typeof evt !== 'undefined') {
          const ClassifierIDsList = []
          const ClassifierIDsListCleared = []
          for (let i = 0; evt.points.length; i++) {
            if (evt.points[i] === undefined) {
              break
            } else {
              const OnlyId = evt.points[i].text.split('<br>')
              const ImpID = OnlyId[0].split(' ')
              ClassifierIDsList.push(ImpID[3])
              let numberNumb = parseInt(ImpID[3])
              ClassifierIDsListCleared.push(numberNumb)
            }
          }
          if (ClassifierIDsList != '') {
            EventBus.$emit('ChangeKey', 1)
            EventBus.$emit('SendSelectedPointsToServerEventfromData', ClassifierIDsListCleared)
          } else {
            EventBus.$emit('ChangeKey', 0)
          }
        }
      })
    }
  },
  mounted() {
    EventBus.$on('onlyOnce', data => { this.onlyOnce = data })
    // initialize the first data space projection based on the data set 
    EventBus.$on('emittedEventCallingDataSpacePlotView', data => {
      this.dataPoints = data})
    EventBus.$on('emittedEventCallingDataSpacePlotView', this.scatterPlotDataView)

    // linking based on predictions space brushing
    EventBus.$on('updateDataSpaceHighlighting', data => {
      this.highlightedPoints = data})
    EventBus.$on('updateDataSpaceHighlighting', this.scatterPlotDataView)

    // make the view responsive to window changes
    EventBus.$on('Responsive', data => {
      this.responsiveWidthHeight = data})
    
    EventBus.$on('ResponsiveandAdapt', data => { this.smallScreenMode = data })

    EventBus.$on('RepresentationSelectionData', data => {this.representationDef = data})
    EventBus.$on('RepresentationSelectionData', this.scatterPlotDataView)
    
    // reset view
    EventBus.$on('resetViews', this.reset)

    EventBus.$on('SendToServerDataSetConfirmation', data => { this.RetrieveDataSet = data })

    EventBus.$on('brushedDataSpace', data => {this.onlyOnce = true})
    EventBus.$on('brushedDataSpace', data => {this.restylePoints = data})
    EventBus.$on('brushedDataSpace', this.scatterPlotDataView)
  }
}
</script>