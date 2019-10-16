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
      CollectionData: '',
      DataSpace: '',
      WH: []
    }
  },
  methods: {
    ScatterPlotDataView () {
        const XandYCoordinates = JSON.parse(this.DataSpace[7])

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
        var height = this.WH[1]*1.5 // interactive visualization
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
        title: 'Data Space Projection (tSNE)',
        xaxis: {
            visible: false
        },
        yaxis: {
            visible: false
        },
        autosize: true,
        width: width,
        height: height,
        }
        Plotly.newPlot('OverviewDataPlotly', Data, layout, {responsive: true})
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingDataPlot', data => {
      this.CollectionData = data})
    EventBus.$on('emittedEventCallingDataSpacePlotView', data => {
      this.DataSpace = data})
    EventBus.$on('emittedEventCallingDataSpacePlotView', this.ScatterPlotDataView)
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})
  }
}
</script>