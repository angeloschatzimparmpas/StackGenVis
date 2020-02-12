<template>
<b-row>
    <b-col cols="12">
        <div id="barChart" class="barChart" style="min-height: 307px;"></div>
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
      algorithmsinBar: [],
      modelsSelectedinBar: [],
      factors: [1,1,1,1,1],
      KNNModels: 576, //KNN models,
      colorsValues: ['#6a3d9a','#b15928','#e31a1c'],
      WH: []
    }
  },
  methods: {
    BarChartView () {
      const PerClassMetrics = JSON.parse(this.PerformanceResults[2])
      const PerClassMetrics2 = JSON.parse(this.PerformanceResults[10])

      var KNNModels = []
      var RFModels = []
      
            
      var factorsLocal = this.factors
      var divide = factorsLocal[1] + factorsLocal[2] + factorsLocal[3]

      if (this.modelsSelectedinBar.length != 0){
          for (let i=0; i<this.algorithmsinBar.length;i++) {
              if (this.algorithmsinBar[i] === "KNN") {
                  KNNModels.push(JSON.parse(this.modelsSelectedinBar[i]))
              } else {
                  RFModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.KNNModels)
              }
          }
      }
      
      var target_names
      target_names = Object.keys(PerClassMetrics)

      var sum = []
      var temp = 0
      var temp2 = 0
      for (var i=0;i<target_names.length;i++) {
          temp = 0
          temp2 = 0
          for (var j=0;j<Object.keys(PerClassMetrics[target_names[i]]).length;j++){
              temp = temp + ((Object.values(PerClassMetrics)[i][j]['f1-score']*factorsLocal[1])+(Object.values(PerClassMetrics)[i][j]['precision']*factorsLocal[2])+(Object.values(PerClassMetrics)[i][j]['recall']*factorsLocal[3]))/divide
          }
          temp = temp/Object.keys(PerClassMetrics[target_names[i]]).length
          sum.push(temp)
          for (var k=0;k<Object.keys(PerClassMetrics2[target_names[i]]).length;k++){
            temp2 = temp2 + ((Object.values(PerClassMetrics2)[i][k]['f1-score']*factorsLocal[1])+(Object.values(PerClassMetrics2)[i][k]['precision']*factorsLocal[2])+(Object.values(PerClassMetrics2)[i][k]['recall']*factorsLocal[3]))/divide
          }
          temp2 = temp2/Object.keys(PerClassMetrics2[target_names[i]]).length
          sum.push(temp2)
      }

      var sumLine = []
      var temp = 0
      var temp2 = 0
      for (var i=0;i<target_names.length;i++) {
          temp = 0
          temp2 = 0

          if (KNNModels.length == 0) {
              for (var j=0;j<Object.keys(PerClassMetrics[target_names[i]]).length;j++){
                temp = temp + ((Object.values(PerClassMetrics)[i][j]['f1-score']*factorsLocal[1])+(Object.values(PerClassMetrics)[i][j]['precision']*factorsLocal[2])+(Object.values(PerClassMetrics)[i][j]['recall']*factorsLocal[3]))/divide
              }
              temp = temp/Object.keys(PerClassMetrics[target_names[i]]).length
          } else {
              for (var j=0;j<KNNModels.length;j++){
                  temp = temp + ((Object.values(PerClassMetrics)[i][j]['f1-score']*factorsLocal[1])+(Object.values(PerClassMetrics)[i][j]['precision']*factorsLocal[2])+(Object.values(PerClassMetrics)[i][j]['recall']*factorsLocal[3]))/divide
              }
              temp = temp/KNNModels.length
          }
          sumLine.push(temp)

          if (RFModels.length == 0) {
              for (var k=0;k<Object.keys(PerClassMetrics2[target_names[i]]).length;k++){
                  temp2 = temp2 + ((Object.values(PerClassMetrics2)[i][k]['f1-score']*factorsLocal[1])+(Object.values(PerClassMetrics2)[i][k]['precision']*factorsLocal[2])+(Object.values(PerClassMetrics2)[i][k]['recall']*factorsLocal[3]))/divide
              }
              temp2 = temp2/Object.keys(PerClassMetrics2[target_names[i]]).length
          } else {
              for (var k=0;k<RFModels.length;k++){
                  temp2 = temp2 + ((Object.values(PerClassMetrics2)[i][k]['f1-score']*factorsLocal[1])+(Object.values(PerClassMetrics2)[i][k]['precision']*factorsLocal[2])+(Object.values(PerClassMetrics2)[i][k]['recall']*factorsLocal[3]))/divide
              }
              temp2 = temp2/RFModels.length
          }
          sumLine.push(temp2)
      }
      Plotly.purge('barChart')
      
      var layout = {
      autosize: true,
      barmode: 'group',
      width: this.WH[0]*3,
      height: this.WH[1]*0.635,
          xaxis: {
              title: 'Algorithm',
              type:"category",
              showticklabels: true,
              tickangle: 'auto',
              exponentformat: 'e',
              showexponent: 'all'
          },
          yaxis: {
              title: 'Performance Metrics',
          },
          xaxis2: {
              overlaying: 'x',
              type:"category",
              showticklabels: true,
              tickangle: 'auto',
              exponentformat: 'e',
              showexponent: 'all'
          },
      margin: {
          l: 50,
          r: 0,
          b: 30,
          t: 30,
          pad: 0
          }
      }
          var traces = []
          var tracesSel = []
          var data = []
          
          for (var i = 0; i < target_names.length; i++) {
              traces[i] = {
                  x: ['KNN', 'RF'],
                  y: [sum[i+i],sum[i+i+1]],
                  name: target_names[i],
                  opacity: 0.5,
                  marker: {
                      opacity: 0.5,
                      color: this.colorsValues[i]
                  },
                  type: 'bar'
                  };
              tracesSel[i] = {
                  type: 'bar',
                  x: ['KNN', 'RF'],
                  y: [sumLine[i+i],sumLine[i+i+1]],
                  name: target_names[i]+' (Sel)',
                  xaxis: 'x2',
                  mode: 'markers',
                  marker: {
                      opacity: 1.0,
                      color: this.colorsValues[i],
                  },
                  width: [0.1, 0.1]
                  };
                  data.push(traces[i])
                  data.push(tracesSel[i])
          }
          Plotly.newPlot('barChart', data, layout)
      },
      reset () 
      {
        setTimeout(() => {
          Plotly.purge('barChart')
        }, 50);
      }
    },
    mounted() {
      EventBus.$on('updateBarChartAlgorithm', data => { this.algorithmsinBar = data })
      EventBus.$on('updateBarChart', data => { this.modelsSelectedinBar = data })
      EventBus.$on('updateBarChart', this.BarChartView)
      EventBus.$on('emittedEventCallingBarChart', data => { this.PerformanceResults = data })
      EventBus.$on('emittedEventCallingBarChart', this.BarChartView)
      EventBus.$on('emittedEventCallingUpdateBarChart', data => { this.ModelsChosen = data })
      EventBus.$on('emittedEventCallingUpdateBarChart', this.BarChartView)

      EventBus.$on('Responsive', data => {
          this.WH = data})
      EventBus.$on('ResponsiveandChange', data => {
          this.WH = data})

      EventBus.$on('CallFactorsView', data => { this.factors = data })
      EventBus.$on('CallFactorsView', this.BarChartView)

      // reset view
      EventBus.$on('resetViews', this.reset)
    }
}
</script>