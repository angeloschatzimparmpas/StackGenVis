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
      barchartmetricsprediction: [],
      SelBarChartMetrics: [],
      boldXAxis: '',
      factors: [1,0,0
      ,1,0,0,1,0
      ,0,1,0,0,0
      ,0,0,1,0,0
      ,0,1,1,1
      ],
      smallScreenMode: '0px',
    }
  },
  methods: {
    LineBar () {
      Plotly.purge('PerMetricBar')
      
      var x = []
      var metricsPerModel = JSON.parse(this.barchartmetrics[9])
      var metricsPerModelSel = []
      if (this.SelBarChartMetrics.length == 0) {
        metricsPerModelSel = metricsPerModel
      } else {
        metricsPerModelSel = this.SelBarChartMetrics
      }

      var factorsLocal = this.factors

      var perModelAllClear = []
      var perModelSelectedClear = []
      var resultsColors = []
      if (this.boldXAxis == 'Accuracy') {
        var chooseFrom = ['<b>Accuracy</b>','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','MCC','ROC AUC','Log Loss']
      }
      else if (this.boldXAxis == 'G-Mean') {
        var chooseFrom = ['Accuracy','<b>G-Mean</b>','<b>G-Mean</b>','<b>G-Mean</b>','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','MCC','ROC AUC','Log Loss']
      }
      else if (this.boldXAxis == 'Precision') {
        var chooseFrom = ['Accuracy','G-Mean','G-Mean','G-Mean','<b>Precision</b>','<b>Precision</b>','<b>Precision</b>','Recall','Recall','Recall','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','MCC','ROC AUC','Log Loss']
      }
      else if (this.boldXAxis == 'Recall') {
        var chooseFrom = ['Accuracy','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','<b>Recall</b>','<b>Recall</b>','<b>Recall</b>','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','MCC','ROC AUC','Log Loss']
      }
      else if (this.boldXAxis == 'F-Beta Score') {
        var chooseFrom = ['Accuracy','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','<b>F-Beta Score</b>','<b>F-Beta Score</b>','<b>F-Beta Score</b>','<b>F-Beta Score</b>','<b>F-Beta Score</b>','<b>F-Beta Score</b>','<b>F-Beta Score</b>','<b>F-Beta Score</b>','<b>F-Beta Score</b>','MCC','ROC AUC','Log Loss']
      }
      else if (this.boldXAxis == 'MCC') {
        var chooseFrom = ['Accuracy','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','<b>MCC</b>','ROC AUC','Log Loss']
      }
      else if (this.boldXAxis == 'ROC AUC') {
        var chooseFrom = ['Accuracy','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','MCC','<b>ROC AUC</b>','Log Loss']
      }
      else if (this.boldXAxis == 'Log Loss') {
        var chooseFrom = ['Accuracy','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','MCC','ROC AUC','<b>Log Loss</b>']
      } 
      else {
        var chooseFrom = ['Accuracy','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','F-Beta Score','MCC','ROC AUC','Log Loss']
      }
      for (let i = 0; i < metricsPerModel.length; i++) {
        if (factorsLocal[i] != 0) {
          resultsColors.push(metricsPerModel[i])
        }
        var temp = metricsPerModel[i]
        var resultsClear = JSON.parse(temp)
        var tempSel = metricsPerModelSel[i]
        var resultsClearSelected = JSON.parse(tempSel)
        for (let j = 0; j < Object.values(resultsClear).length; j++) {
          if (factorsLocal[i] != 0) {
            perModelAllClear.push(Object.values(resultsClear)[j])
            perModelSelectedClear.push(Object.values(resultsClearSelected)[j])
            x.push(chooseFrom[i])
          }
        }
      }


      if (this.smallScreenMode != "370px") {
        var width = this.WH[0]*6.5 // interactive visualization
        var height = this.WH[1]*0.482 // interactive visualization
      } else {
        var width = this.WH[0]*6.8
        var height = this.WH[1]*0.38
      }

        var trace1 = {
        x: x,
        y: perModelAllClear, 
        name: 'All Points', 
        type: 'box',
        boxmean: true,
        marker: {
            color: 'rgb(0,0,0)'
        }
        };
        var trace2 = {
        x: x,
        y: perModelSelectedClear, 
        name: 'Selected Points', 
        type: 'box',
        boxmean: true,
        marker: {
            color: 'rgb(211,211,211)'
        }
        };
        var data = [trace1, trace2];
        var layout = {
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        boxmode: 'group',
        autosize: true,
        width:  width,
        height: height,
        hovermode: 'x',
        margin: {
          l: 50,
          r: 0,
          b: 35,
          t: 40,
          pad: 0
        },
        xaxis: {
            title: 'Performance Metrics',
            titlefont: {
            size: 16,
            color: 'black'
            }},
        yaxis: {
            title: '# Performance (%) #',
            titlefont: {
            size: 16,
            color: 'black'
            }}};
        var boxPlot = document.getElementById('PerMetricBar');
        var config = {displayModeBar: false, scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
        Plotly.newPlot(boxPlot, data, layout, config);

        boxPlot.on('plotly_click', (eventData) => {
          var xAxisHovered
          xAxisHovered = eventData.points[0].x
          var index
          if (xAxisHovered == 'Accuracy') {
            index = 0
          }
          else if (xAxisHovered == 'G-Mean') {
            index = 1
          }
          else if (xAxisHovered == 'Precision') {
            index = 2
          }
          else if (xAxisHovered == 'Recall') {
            index = 3
          }
          else if (xAxisHovered == 'F-Beta Score') {
            index = 4
          }
          else if (xAxisHovered == 'MCC') {
            index = 5
          }
          else if (xAxisHovered == 'ROC AUC') {
            index = 6
          }
          else {
            index = 7
          }
          EventBus.$emit('updateBold', xAxisHovered)
          EventBus.$emit('updateMetricsScatter', resultsColors[index])
        });
      },
      reset () {
        Plotly.purge('PerMetricBar')
      }
    },
    mounted () {
      EventBus.$on('updateBold', data => {this.boldXAxis = data;})
      EventBus.$on('updateBold', this.LineBar)

      EventBus.$on('InitializeMetricsBarChart', data => {this.barchartmetrics = data;})
      EventBus.$on('InitializeMetricsBarChart', this.LineBar)
      
      EventBus.$on('InitializeMetricsBarChartPrediction', data => {this.SelBarChartMetrics.length = []})
      EventBus.$on('InitializeMetricsBarChartPrediction', data => {this.barchartmetrics[9] = data;})
      EventBus.$on('InitializeMetricsBarChartPrediction', this.LineBar)

      EventBus.$on('Responsive', data => {
      this.WH = data})

      EventBus.$on('ResponsiveandAdapt', data => { this.smallScreenMode = data })

      EventBus.$on('UpdateBarChartperMetric', data => {
      this.SelBarChartMetrics = data})
      EventBus.$on('UpdateBarChartperMetric', this.LineBar)

      EventBus.$on('CallFactorsView', data => {
      this.factors = data})
      EventBus.$on('CallFactorsView', this.LineBar)

      EventBus.$on('updateBoxPlots', this.LineBar)

      // reset view
      EventBus.$on('resetViews', this.reset)
    }
}
</script>