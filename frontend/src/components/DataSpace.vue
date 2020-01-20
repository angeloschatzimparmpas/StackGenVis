<template>
  <div id="OverviewDataPlotly" class="OverviewDataPlotly"></div>
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
      responsiveWidthHeight: [],
      colorsValues: ['#00bbbb','#b15928','#ff7f00']
    }
  },
  methods: {
    scatterPlotDataView () {
        // responsive visualization
        let width = this.responsiveWidthHeight[0]*3 
        let height = this.responsiveWidthHeight[1]*2.1

        var target_names = JSON.parse(this.dataPoints[4])
        const XandYCoordinates = JSON.parse(this.dataPoints[7])
        const DataSet = JSON.parse(this.dataPoints[14])
        const DataSetY = JSON.parse(this.dataPoints[15])
        const originalDataLabels = JSON.parse(this.dataPoints[16])
        var DataSetParse = JSON.parse(DataSet)

        let intData = []
        if (this.highlightedPoints.length > 0){
          let removedPuncData = this.highlightedPoints.map(function(x){return x.replace(';', '');})
          intData = removedPuncData.map(Number)
        } else {
          intData = []
        }

        var result = XandYCoordinates.reduce(function(r, a) {
            var id = 0
            a.forEach(function(s, i) {
                var key = i === 0 ? 'Xax' : 'Yax'

                r[key] || (r[key] = []) // if key not found on result object, add the key with empty array as the value

                r[key].push(s)

            })

            return r
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

          var Opacity = aux_ID.map((item, index) => {
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
            marker: { color: this.colorsValues[i], line: { color: 'rgb(0, 0, 0)', width: 2 }, opacity: Opacity },
            hovertemplate: 
                    "<b>%{text}</b><br><br>" +
                    "<extra></extra>",
            text: Text,
          })
        }

        const layout = {
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

        var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian','zoomIn2d','zoomOut2d','zoom2d'], responsive: true}

        Plotly.newPlot('OverviewDataPlotly', traces, layout, config)
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
  }
}
</script>