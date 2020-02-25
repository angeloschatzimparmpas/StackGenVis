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
      SelBarChartMetrics: [],
      factors: [1,1,1,0,0
      ,1,0,0,1,0
      ,0,1,0,0,0
      ,0,0,1,0,0
      ,0,1,1,1
      ],
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
      var chooseFrom = ['Accuracy','MAE','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','Log Loss']
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
      var width = this.WH[0]*6.5 // interactive visualization
      var height = this.WH[1]*0.5 // interactive visualization
          var trace1 = {
          x: x,
          y: perModelAllClear, 
          name: 'Performance Metrics', 
          type: 'box',
          boxmean: true,
          marker: {
              color: 'rgb(0,0,0)'
          }
          };
          var trace2 = {
          x: x,
          y: perModelSelectedClear, 
          name: 'Selected points', 
          type: 'box',
          boxmean: true,
          marker: {
              color: 'rgb(211,211,211)'
          }
          };
          var data = [trace1, trace2];
          var layout = {
          boxmode: 'group',
          autosize: true,
          width:  width,
          height: height,
          hovermode: 'x',
          margin: {
            l: 50,
            r: 0,
            b: 30,
            t: 40,
            pad: 0
          },
          xaxis: {
              title: 'Performance Metrics',
              titlefont: {
              size: 12,
              color: 'black'
              }},
          yaxis: {
              title: '# Performance (%) #',
              titlefont: {
              size: 12,
              color: 'black'
              }}};
          var boxPlot = document.getElementById('PerMetricBar');
          var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
          Plotly.newPlot(boxPlot, data, layout, config);

          boxPlot.on('plotly_click', (eventData) => {
            var xAxisHovered
            xAxisHovered = eventData.points[0].x
            var index
            if (xAxisHovered == 'Accuracy') {
              Plotly.restyle(boxPlot, 'x', [['<b>Accuracy</b>','MAE','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','Log Loss']]);
              index = 0
            }
            else if (xAxisHovered == 'MAE') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','<b>MAE</b>','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','Log Loss']]);
              index = 1
            }
            else if (xAxisHovered == 'RMSE') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','<b>RMSE</b>','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','Log Loss']]);
              index = 2
            }
            else if (xAxisHovered == 'G-Mean') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','RMSE','<b>G-Mean</b>','<b>G-Mean</b>','<b>G-Mean</b>','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','Log Loss']]);
              index = 3
            }
            else if (xAxisHovered == 'Precision') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','RMSE','G-Mean','G-Mean','G-Mean','<b>Precision</b>','<b>Precision</b>','<b>Precision</b>','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','Log Loss']]);
              index = 4
            }
            else if (xAxisHovered == 'Recall') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','<b>Recall</b>','<b>Recall</b>','<b>Recall</b>','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','Log Loss']]);
              index = 5
            }
            else if (xAxisHovered == 'F-Beta Sc') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','<b>F-Beta Sc</b>','MCC','ROC AUC','Log Loss']]);
              index = 6
            }
            else if (xAxisHovered == 'MCC') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','<b>MCC</b>','ROC AUC','Log Loss']]);
              index = 7
            }
            else if (xAxisHovered == 'ROC AUC') {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','<b>ROC AUC</b>','Log Loss']]);
              index = 8
            }
            else {
              Plotly.restyle(boxPlot, 'x', [['Accuracy','MAE','RMSE','G-Mean','G-Mean','G-Mean','Precision','Precision','Precision','Recall','Recall','Recall','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','F-Beta Sc','MCC','ROC AUC','<b>Log Loss</b>']]);
              index = 9
            }
            EventBus.$emit('updateMetricsScatter', resultsColors[index])
          });
      },
      reset () {
        Plotly.purge('PerMetricBar')
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

      EventBus.$on('CallFactorsView', data => {
      this.factors = data})
      EventBus.$on('CallFactorsView', this.LineBar)

      EventBus.$on('updateBoxPlots', this.LineBar)

      // reset view
      EventBus.$on('resetViews', this.reset)
    }
}
</script>