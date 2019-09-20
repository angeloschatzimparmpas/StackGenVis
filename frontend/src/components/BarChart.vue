<template>
<b-row>
    <b-col cols="4">
        <div id="barChartPrecision0" class="barChartPrecision0"></div>
        <div id="barChartPrecision1" class="barChartPrecision1"></div>
        <div id="barChartPrecision2" class="barChartPrecision2"></div>
    </b-col>
    <b-col cols="4">
        <div id="barChartRecall0" class="barChartRecall0"></div>
        <div id="barChartRecall1" class="barChartRecall1"></div>
        <div id="barChartRecall2" class="barChartRecall2"></div>
    </b-col>
    <b-col cols="4">
        <div id="barChartf1Score0" class="barChartf1Score0"></div>
        <div id="barChartf1Score1" class="barChartf1Score1"></div>
        <div id="barChartf1Score2" class="barChartf1Score2"></div>
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
      BarChartResults: '',
      ClassNamesOverview: ''
    }
  },
  methods: {
    BarChartView () {
        const PerClassMetrics = JSON.parse(this.BarChartResults[3])
        var ClassNames = JSON.parse(this.BarChartResults[4])
        this.ClassNamesOverview = ClassNames
        let ClassifierswithoutFI = JSON.parse(this.BarChartResults[7])
        let ClassifierswithFI = JSON.parse(this.BarChartResults[8])
        const limit = JSON.parse(this.BarChartResults[14])

        for (let j = 0; j < this.ClassNamesOverview.length; j++) {
            Plotly.purge('barChartf1Score' + j)
            Plotly.purge('barChartPrecision' + j)
            Plotly.purge('barChartRecall' + j)
        }

        var Classifiers
        Classifiers = ClassifierswithoutFI.concat(ClassifierswithFI)

        var PerClassMetricsRed = []
        var limitList = []
        if (limit == '') {
            for (let i = 0; i < Classifiers.length; i++) {
                limitList.push(Classifiers[i])
            }
        } else {
            limitList = []
            for (let i = 0; i < limit.length; i++) {
                for (let j = 0; j < Classifiers.length; j++) {
                    if (Number(limit[i].match(/\d+/)[0]) == Classifiers[j]) {
                        limitList.push(Number(limit[i].match(/\d+/)[0]))
                    }
                }
            }
        }
        
        const precisionPerClass = []
        const recallPerClass = []
        const f1ScorePerClass = []

        for (let j = 0; j < ClassNames.length; j++) {
            precisionPerClass[j] = []
            recallPerClass[j] = []
            f1ScorePerClass[j] = []
                for (let i = 0; i < limitList.length; i++) { // Fix this tomorrow! 0 to 16 and we want the ids.. 
                    precisionPerClass[j].push(PerClassMetrics[limitList[i]][ClassNames[j]].precision)
                    recallPerClass[j].push(PerClassMetrics[limitList[i]][ClassNames[j]].recall)
                    f1ScorePerClass[j].push(PerClassMetrics[limitList[i]][ClassNames[j]]['f1-score'])
                }
        }

        var precisionData
        var recallData
        var f1ScoreData

        var layoutPrec = {
        autosize: false,
        width: 300,
        height: 300,
        xaxis: {
            title: 'Classifier ID',
            type:"category",
            titlefont: {
            family: 'Arial, sans-serif',
            size: 18,
            color: 'lightgrey'
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
            title: 'Precision',
            titlefont: {
            family: 'Arial, sans-serif',
            size: 18,
            color: 'lightgrey'
            }
        }
        }

        var layoutRec = {
        autosize: false,
        width: 300,
        height: 300,
        xaxis: {
            title: 'Classifier ID',
            type:"category",
            titlefont: {
            family: 'Arial, sans-serif',
            size: 18,
            color: 'lightgrey'
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
            title: 'Recall',
            titlefont: {
            family: 'Arial, sans-serif',
            size: 18,
            color: 'lightgrey'
            }
        }
        }

        var layoutf1Score = {
        autosize: false,
        width: 300,
        height: 300,
        xaxis: {
            title: 'Classifier ID',
            type:"category",
            titlefont: {
            family: 'Arial, sans-serif',
            size: 18,
            color: 'lightgrey'
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
            title: 'F1-Score',
            titlefont: {
            family: 'Arial, sans-serif',
            size: 18,
            color: 'lightgrey'
            }
        }
        }
        for (let j = 0; j < ClassNames.length; j++) {
        let len = precisionPerClass[j].length
        let indices = new Array(len)
        for (let i = 0; i < len; ++i) indices[i] = i
        indices.sort(function (a, b) { return precisionPerClass[j][b] < precisionPerClass[j][a] ? -1 : precisionPerClass[j][b] > precisionPerClass[j][a] ? 1 : 0 })
        precisionPerClass[j].sort((function(a, b){return b-a}))
        precisionData = [
            {
            x: indices.map(String),
            y: precisionPerClass[j],
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
        ]

        Plotly.newPlot('barChartPrecision' + j, precisionData, layoutPrec)
        }
        for (let j = 0; j < ClassNames.length; j++) {
        let len = recallPerClass[j].length
        let indices = new Array(len)
        for (let i = 0; i < len; ++i) indices[i] = i
        indices.sort(function (a, b) { return recallPerClass[j][b] < recallPerClass[j][a] ? -1 : recallPerClass[j][b] > recallPerClass[j][a] ? 1 : 0 })
        recallPerClass[j].sort((function(a, b){return b-a}))
        recallData = [
            {
            x: indices.map(String),
            y: recallPerClass[j],
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
        ]

        Plotly.newPlot('barChartRecall' + j, recallData, layoutRec)
        }
        for (let j = 0; j < ClassNames.length; j++) {
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
            ]

            Plotly.newPlot('barChartf1Score' + j, f1ScoreData, layoutf1Score)
                }
        },
        reset () {
            for (let j = 0; j < this.ClassNamesOverview.length; j++) {
                Plotly.purge('barChartf1Score' + j)
                Plotly.purge('barChartPrecision' + j)
                Plotly.purge('barChartRecall' + j)
            }
        }
    },
    mounted() {
        EventBus.$on('emittedEventCallingBarChart', data => { this.BarChartResults = data })
        EventBus.$on('emittedEventCallingBarChart', this.BarChartView)
        EventBus.$on('resetViews', this.reset)
    }
}
</script>