<template>
  <div id="PerMetricBar" class="PerMetricBar"></div>
</template>

<script>
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'PerMetricsBarChart',
  data () {
    return {
      barchartmetrics: '',
      WH: [],
      SelBarChartMetrics: []
    }
  },
  methods: {
        LineBar () {

        Plotly.purge('PerMetricBar')

        var metricsPerModel = JSON.parse(this.barchartmetrics[9])
        var metricsPerModelSel = []
        if (this.SelBarChartMetrics.length == 0) {
          metricsPerModelSel = metricsPerModel
        } else {
          metricsPerModelSel = this.SelBarChartMetrics
        }
        var width = this.WH[0]*3 // interactive visualization
        var height = this.WH[1]/2 // interactive visualization
            var trace1 = {
            x: ['Acc','F1s','Pre','Rec','Jac'], 
            y: metricsPerModel, 
            name: 'Projection average', 
            type: 'bar',
            marker: {
                color: 'rgb(0,0,0)'
            }
            };
            var trace2 = {
            x: ['Acc','F1s','Pre','Rec','Jac'], 
            y: metricsPerModelSel, 
            name: 'Selected points', 
            type: 'bar',
            marker: {
                color: 'rgb(211,211,211)'
            }
            };
            var data = [trace1, trace2];
            var layout = {
            barmode: 'group',autosize: false,
            width:  width,
            height: height,
            margin: {
                l: 50,
                r: 30,
                b: 30,
                t: 5,
                pad: 4
            },
            xaxis: {
                title: 'Performance Metrics',
                titlefont: {
                size: 12,
                color: 'black'
                }},
            yaxis: {
                title: 'Performance',
                titlefont: {
                size: 12,
                color: 'black'
                }}};

        Plotly.newPlot('PerMetricBar', data, layout, {displayModeBar:false}, {staticPlot: true});
        //}
        }
    },
    mounted () {
        EventBus.$on('InitializeMetricsBarChart', data => {this.barchartmetrics = data;})
        EventBus.$on('InitializeMetricsBarChart', this.LineBar)
        EventBus.$on('Responsive', data => {
        this.WH = data})
        EventBus.$on('ResponsiveandChange', data => {
        this.WH = data})
        EventBus.$on('UpdateBarChartperMetric', data => {
        this.SelBarChartMetrics = data})
        EventBus.$on('UpdateBarChartperMetric', this.LineBar)
    }
}
</script>