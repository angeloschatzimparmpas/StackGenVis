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
      DataSpace: ''
    }
  },
  methods: {
    ScatterPlotDataView () {
        const XandYCoordinates = this.DataSpace[0]

        var result = XandYCoordinates.reduce(function(r, a) {
            a.forEach(function(s, i) {
                var key = i === 0 ? 'Xax' : 'Yax';

                r[key] || (r[key] = []); // if key not found on result object, add the key with empty array as the value

                r[key].push(s);
            })
            return r;
        }, {})

        const Data = [{
        x: result.Xax,
        y: result.Yax,
        mode: 'markers',
        }]
        const layout = {
        title: 'Data Space Projection (tSNE)',
        xaxis: {
            visible: false
        },
        yaxis: {
            visible: false
        }
        }
        Plotly.newPlot('OverviewDataPlotly', Data, layout)
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingDataPlot', data => {
      this.CollectionData = data})
    EventBus.$on('emittedEventCallingDataSpacePlotView', data => {
      this.DataSpace = data})
    EventBus.$on('emittedEventCallingDataSpacePlotView', this.ScatterPlotDataView)
  }
}
</script>