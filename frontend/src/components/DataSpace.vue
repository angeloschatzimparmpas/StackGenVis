<template>
  <div>
    <div align="center">
      Projection Selection: <select id="selectBarChartData" @change="selectVisualRepresentationData()">
        <option value="mds" selected>MDS Projection</option>
        <option value="tsne">t-SNE Projection</option>
        <option value="umap">UMAP Projection</option>
      </select>
      Filter: <select id="selectFilterID" @change="selectAppliedFilter()">
        <option value="mean" selected>Mean</option>
        <option value="median">Median</option>
      </select>
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
      History Controller: <button
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
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'DataSpace',
  data () {
    return {
      dataPoints: '',
      highlightedPoints: '',
      representationDef: 'mds',
      representationSelection: 'mds',
      mergeData: 'Merge',
      removeData: 'Remove',
      composeData: 'Compose',
      saveData: 'Save Step',
      restoreData: 'Restore Step',
      userSelectedFilter: 'mean',
      responsiveWidthHeight: [],
      colorsValues: ['#b3e2cd','#fdcdac','#cbd5e8','#f4cae4','#e6f5c9','#fff2ae','#f1e2cc']
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
      EventBus.$emit('SendAction', 'merge')
    },
    remove () {
      EventBus.$emit('SendAction', 'remove')
    },
    compose () {
      EventBus.$emit('SendAction', 'compose')
    },
    save () {
      EventBus.$emit('SendProvenance', 'save')
    },
    restore () {
      EventBus.$emit('SendProvenance', 'restore')
    },
    scatterPlotDataView () {
      Plotly.purge('OverviewDataPlotly')

      // responsive visualization
      let width = this.responsiveWidthHeight[0]*6.5
      let height = this.responsiveWidthHeight[1]*1.1

      var target_names = JSON.parse(this.dataPoints[0])
      const XandYCoordinatesMDS = JSON.parse(this.dataPoints[1])
      const DataSet = JSON.parse(this.dataPoints[2])
      const DataSetY = JSON.parse(this.dataPoints[3])
      const originalDataLabels = JSON.parse(this.dataPoints[4])
      var DataSetParse = JSON.parse(DataSet)
      const XandYCoordinatesTSNE = JSON.parse(this.dataPoints[5])
      const XandYCoordinatesUMAP = JSON.parse(this.dataPoints[6])

      let intData = []
      if (this.highlightedPoints.length > 0){
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
              name: target_names[i],
              marker: { color: this.colorsValues[i], line: { color: 'rgb(0, 0, 0)', width: 2 }, opacity: Opacity, size: 12 },
              hovertemplate: 
                      "<b>%{text}</b><br><br>" +
                      "<extra></extra>",
              text: Text,
            })
        }

        layout = {
        title: 'Data Space Projection (MDS)',
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
            name: target_names[i],
            marker: { color: this.colorsValues[i], line: { color: 'rgb(0, 0, 0)', width: 2 }, opacity: Opacity, size: 12 },
            hovertemplate: 
                    "<b>%{text}</b><br><br>" +
                    "<extra></extra>",
            text: Text,
          })
        }

        layout = {
        title: 'Data Space Projection (t-SNE)',
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
              name: target_names[i],
              marker: { color: this.colorsValues[i], line: { color: 'rgb(0, 0, 0)', width: 2 }, opacity: Opacity, size: 12 },
              hovertemplate: 
                      "<b>%{text}</b><br><br>" +
                      "<extra></extra>",
              text: Text,
            })
        }

        layout = {
        title: 'Data Space Projection (UMAP)',
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

      Plotly.newPlot('OverviewDataPlotly', traces, layout, config)

      this.selectedDataPoints()
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
              const OnlyId = evt.points[i].text.split(';')
              ClassifierIDsList.push(OnlyId[0])
              let numb = OnlyId[0].match(/\d/g);
              numb = numb.join("");
              let numberNumb = Number(numb)
              ClassifierIDsListCleared.push(numberNumb)
            }
          }
          if (ClassifierIDsList != '') {
            EventBus.$emit('SendSelectedPointsToServerEventfromData', ClassifierIDsListCleared)
          } else {
            EventBus.$emit('SendSelectedPointsToServerEventfromData', '')
          }
        }
      })
    }
  },
  mounted() {
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
    EventBus.$on('ResponsiveandChange', data => {
      this.responsiveWidthHeight = data})

    EventBus.$on('RepresentationSelectionData', data => {this.representationDef = data})
    EventBus.$on('RepresentationSelectionData', this.scatterPlotDataView)
    
    // reset view
    EventBus.$on('resetViews', this.reset)
  }
}
</script>