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
      barchartmetrics: ''
    }
  },
  methods: {
        LineBar () {
        var  metricsPerModel = JSON.parse(this.barchartmetrics[9])
        var vh = 80

        /*if (this.representationDefault === 'bar'){
        var type = 'bar';
        } else if (this.representationDefault === 'line'){
            var type = 'line';
        } else {
            var type = 'difference';
        }
        var difference = [];
        for (var i=0; i<metricsPerModel.length; i++){
            difference.push(metricsPerModel[i] - metricsPerModel[i]);
        }*/

        /*if (type == 'difference'){
            var trace = {
            x: kValuesLegend, 
            y: difference, 
            name: 'Delta(preservation)', 
            showlegend:  true,
            type: 'line',
            marker: {
                color: 'rgb(128,128,0)'
            }
            };
            var LimitXaxis = Number(maxKNN) + 1;
            var data = [trace];
            var layout = {
            barmode: 'group',autosize: false,
            width: 400,
            height: vh * 1.3,
            margin: {
                l: 50,
                r: 30,
                b: 30,
                t: 5,
                pad: 4
            },
            xaxis: {range: [0, LimitXaxis],
                title: 'Number of neighbors',
                titlefont: {
                size: 12,
                color: 'black'
                }},
            yaxis: {
                title: '+/- Pres.',
                titlefont: {
                size: 12,
                color: 'black'
                }}};

        Plotly.newPlot('PerMetricBar', data, layout, {displayModeBar:false}, {staticPlot: true});
        } else{*/
            var trace1 = {
            x: ['Acc','F1s','Pre','Rec','Jac'], 
            y: metricsPerModel, 
            name: 'Projection average', 
            type: type,
            marker: {
                color: 'rgb(0,0,0)'
            }
            };
            var trace2 = {
            x: ['Acc','F1s','Pre','Rec','Jac'], 
            y: metricsPerModel, 
            name: 'Selected points', 
            type: type,
            marker: {
                color: 'rgb(0, 187, 187)'
            }
            };
            var data = [trace1, trace2];
            var layout = {
            barmode: 'group',autosize: false,
            width:  400,
            height: vh * 1.3,
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
    }
}
</script>