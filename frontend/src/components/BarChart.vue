<template>
<b-row>
    <b-col cols="12">
        <div id="barChart" class="barChart"></div>
    </b-col>
</b-row>
</template>

<script>
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'BarChart',
  data () {
    return {
      PerformanceResults: '',
      ClassNamesOverview: '',
      PerformanceResultsSel: []
    }
  },
  methods: {
    BarChartView () {

        const PerClassMetrics = JSON.parse(this.PerformanceResults[1])
        const PerClassMetrics2 = JSON.parse(this.PerformanceResults[3])
        var UpdateFeatures = 0
        UpdateFeatures = JSON.parse(this.PerformanceResultsSel[0])
        var UpdateFeatures2 = 0
        UpdateFeatures2 = JSON.parse(this.PerformanceResultsSel[1])
        var target_names
        target_names = Object.keys(PerClassMetrics)
        var sum = []
        var temp = 0
        for (var i=0;i<target_names.length;i++) {
            temp = 0
            temp = (Object.values(PerClassMetrics)[i][0]['f1-score']+Object.values(PerClassMetrics)[i][0]['precision']+Object.values(PerClassMetrics)[i][0]['recall'])/3
            sum.push(temp)
            temp = 0
            temp = (Object.values(PerClassMetrics2)[i][0]['f1-score']+Object.values(PerClassMetrics2)[i][0]['precision']+Object.values(PerClassMetrics2)[i][0]['recall'])/3
            sum.push(temp)
        }
        var sumLine = []
        var temp = 0
        for (var i=0;i<target_names.length;i++) {
            if (UpdateFeatures != 0) {
                temp = 0
                temp = (Object.values(UpdateFeatures)[i][0]['f1-score']+Object.values(UpdateFeatures)[i][0]['precision']+Object.values(UpdateFeatures)[i][0]['recall'])/3
                sumLine.push(temp)
            } else {
                temp = 0
                temp = (Object.values(PerClassMetrics)[i][0]['f1-score']+Object.values(PerClassMetrics)[i][0]['precision']+Object.values(PerClassMetrics)[i][0]['recall'])/3
                sumLine.push(temp)
            }
            if (UpdateFeatures2 != 0) {
                temp = 0
                temp = (Object.values(UpdateFeatures2)[i][0]['f1-score']+Object.values(UpdateFeatures2)[i][0]['precision']+Object.values(UpdateFeatures2)[i][0]['recall'])/3
                sumLine.push(temp)
            } else {
                temp = 0
                temp = (Object.values(PerClassMetrics2)[i][0]['f1-score']+Object.values(PerClassMetrics2)[i][0]['precision']+Object.values(PerClassMetrics2)[i][0]['recall'])/3
                sumLine.push(temp)
            }
        }
       /* console.log(PerClassMetrics)
        if (this.ModelsChosen != []) {
            console.log('mpike')
            for (var i=0;i<target_names.length;i++) {
            temp = 0
            temp = (Object.values(PerClassMetrics)[i][0]['f1-score']+Object.values(PerClassMetrics)[i][0]['f1-score']+Object.values(PerClassMetrics)[i][0]['f1-score'])/3
            sum.push(temp)
            temp = 0
            temp = (Object.values(PerClassMetrics2)[i][0]['f1-score']+Object.values(PerClassMetrics2)[i][0]['f1-score']+Object.values(PerClassMetrics2)[i][0]['f1-score'])/3
            sum.push(temp)
        }
        }*/
        Plotly.purge('barChart')
        
        const f1ScorePerClass = []

       /* for (let j = 0; j < ClassNames.length; j++) {
            f1ScorePerClass[j] = []
                for (let i = 0; i < limitList.length; i++) { // Fix this tomorrow! 0 to 16 and we want the ids.. 
                    f1ScorePerClass[j].push(PerClassMetrics[limitList[i]][ClassNames[j]]['f1-score'])
                }
        }*/
        var layout = {
        autosize: false,
        barmode: 'group',
        width: 550,
        height: 400,
            xaxis: {
                title: 'Algorithm',
                type:"category",
                titlefont: {
                family: 'Arial, sans-serif',
                size: 18,
                color: 'grey'
                },
                showticklabels: true,
                tickangle: 'auto',
                tickfont: {
                family: 'Old Standard TT, serif',
                size: 14,
                color: 'black'
                },
                exponentformat: 'e',
                showexponent: 'all'
            },
            yaxis: {
                title: 'Per Class Performance',
                titlefont: {
                family: 'Arial, sans-serif',
                size: 18,
                color: 'grey'
                }
            },
            xaxis2: {
                overlaying: 'x',
                type:"category",
                titlefont: {
                family: 'Arial, sans-serif',
                size: 18,
                color: 'grey'
                },
                showticklabels: true,
                tickangle: 'auto',
                tickfont: {
                family: 'Old Standard TT, serif',
                size: 14,
                color: 'black'
                },
                exponentformat: 'e',
                showexponent: 'all'
            }
        }
        /*for (let j = 0; j < ClassNames.length; j++) {
            let len = f1ScorePerClass[j].length
            let indices = new Array(len)
            for (let i = 0; i < len; ++i) indices[i] = i
            indices.sort(function (a, b) { return f1ScorePerClass[j][b] < f1ScorePerClass[j][a] ? -1 : f1ScorePerClass[j][b] > f1ScorePerClass[j][a] ? 1 : 0 })
            f1ScorePerClass[j].sort((function(a, b){return b-a}))
            f1ScoreData = [
                {
                x: indices.map(String),
                y: f1ScorePerClass[j],
                type: 'bar',
                marker: {
                    color: 'rgb(158,202,225)',
                    opacity: 0.6,
                    line: {
                    color: 'rgb(8,48,107)',
                    width: 1.5
                    }
                }
                }
            ]*/

            var colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']

            var trace1 = {
            x: ['KNN', 'RF'],
            y: [sum[0],sum[1]],
            name: target_names[0],
            opacity: 0.5,
            marker: {
                opacity: 0.5,
                color: colors[0]
            },
            type: 'bar'
            };

            var trace2 = {
            x: ['KNN', 'RF'],
            y: [sum[2],sum[3]],
            name: target_names[1],
            opacity: 0.5,
            marker: {
                opacity: 0.5,
                color: colors[1]
            },
            type: 'bar'
            };

            var trace3 = {
            x: ['KNN', 'RF'],
            y: [sum[4],sum[5]],
            name: target_names[2],
            opacity: 0.5,
            marker: {
                opacity: 0.5,
                color: colors[2]
            },
            type: 'bar'
            };

            var trace4 = {
            type: 'bar',
            x: ['KNN', 'RF'],
            y: [sumLine[0],sumLine[1]],
            name: target_names[0]+' (Sel)',
            xaxis: 'x2',
            mode: 'markers',
            marker: {
                opacity: 1.0,
                color: colors[0],
            },
            width: [0.1, 0.1]
            };

            var trace5 = {
            type: 'bar',
            x: ['KNN', 'RF'],
            y: [sumLine[2],sumLine[3]],
            name: target_names[1]+' (Sel)',
            xaxis: 'x2',
            mode: 'markers',
            marker: {
                opacity: 1.0,
                color: colors[1],
            },
            width: [0.1, 0.1]
            };

            var trace6 = {
            type: 'bar',
            x: ['KNN', 'RF'],
            y: [sumLine[4],sumLine[5]],
            name: target_names[2]+' (Sel)',
            xaxis: 'x2',
            mode: 'markers',
            marker: {
                opacity: 1.0,
                color: colors[2],
            },
            width: [0.1, 0.1]
            };

            var data = [trace1, trace4, trace2, trace5, trace3, trace6];

            Plotly.newPlot('barChart', data, layout)
        },
        reset () 
        {
            Plotly.purge('barChart')
        }
    },
    mounted() {
        this.PerformanceResultsSel[0] = 0
        this.PerformanceResultsSel[1] = 0
        EventBus.$on('emittedEventCallingBarChartUpdatedFeatures', data => { this.PerformanceResultsSel = data })
        EventBus.$on('emittedEventCallingBarChartUpdatedFeatures', this.BarChartView)
        EventBus.$on('emittedEventCallingBarChart', data => { this.PerformanceResults = data })
        EventBus.$on('emittedEventCallingBarChart', this.BarChartView)
        EventBus.$on('emittedEventCallingUpdateBarChart', data => { this.ModelsChosen = data })
        EventBus.$on('emittedEventCallingUpdateBarChart', this.BarChartView)
        EventBus.$on('resetViews', this.reset)
    }
}
</script>