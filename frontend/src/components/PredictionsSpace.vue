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
      PredictionsData: ''
    }
  },
  methods: {
    ScatterPlotDataView () {
        const XandYCoordinates = JSON.parse(this.PredictionsData[8])

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
        title: 'Predictions Space Projection (tSNE)',
        xaxis: {
            visible: false
        },
        yaxis: {
            visible: false
        },
        autosize: true,
        width: 400,
        height: 400,
        }
        Plotly.newPlot('OverviewPredPlotly', Data, layout, {responsive: true})
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingPredictionsSpacePlotView', data => {
      this.PredictionsData = data})
    EventBus.$on('emittedEventCallingPredictionsSpacePlotView', this.ScatterPlotDataView)
  }
}
</script>