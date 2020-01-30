<template>
  <div>
    <div id="exploding_boxplot" class="exploding_boxplot"></div>
  </div>
</template>

<script>
import { EventBus } from '../main.js'
import * as d3Base from 'd3'
import * as exploding_boxplot from 'd3_exploding_boxplot'
import 'd3_exploding_boxplot/src/d3_exploding_boxplot.css'
import $ from 'jquery'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default {
  name: 'Algorithms',
  data () {
    return {
      PerformanceAllModels: '',
      brushedAll: [],
      brushedBoxPl: [],
      previousColor: 0,
      selectedAlgorithm: 0,
      AllAlgorithms: ['KNN','RF'],
      KNNModels: 576, //KNN models
      WH: [],
      parameters: [],
      algorithm1: [],
      algorithm2: [],
      chart: '',
      flagEmpty: 0,
      ActiveModels: [],
    }
  },
  methods: {
    reset () {
      d3.selectAll("#exploding_boxplot > *").remove()
    },
    boxplot () {
      // reset the boxplot
      d3.selectAll("#exploding_boxplot > *").remove()

      // retrieve models ID
      const Algor1IDs = this.PerformanceAllModels[0]
      const Algor2IDs = this.PerformanceAllModels[8]
      
      // retrieve the results like performance
      const PerformAlgor1 = JSON.parse(this.PerformanceAllModels[1])
      const PerformAlgor2 = JSON.parse(this.PerformanceAllModels[9])

      // initialize/instansiate algorithms and parameters
      this.algorithm1 = []
      this.algorithm2 = []
      this.parameters = []

      for (var i = 0; i < Object.keys(PerformAlgor1['0']).length; i++) {
        this.algorithm1.push({'Performance Metrics': Object.values(PerformAlgor1['0'])[i]*100,Algorithm:'KNN',Model:'Model ' + Algor1IDs[i] + '; Parameters '+JSON.stringify(Object.values(PerformAlgor1['params'])[i])+'; Performance Metrics ',ModelID:Algor1IDs[i]})
        this.parameters.push(JSON.stringify(Object.values(PerformAlgor1['params'])[i]))
      }
      for (let j = 0; j < Object.keys(PerformAlgor2['0']).length; j++) {
        this.algorithm2.push({'Performance Metrics': Object.values(PerformAlgor2['0'])[j]*100,Algorithm:'RF',Model:'Model ' + Algor2IDs[j] + '; Parameters '+JSON.stringify(Object.values(PerformAlgor2['params'])[j])+'; Performance Metrics ',ModelID:Algor2IDs[j]})
        this.parameters.push(JSON.stringify(Object.values(PerformAlgor2['params'])[j]))
      }

      EventBus.$emit('ParametersAll', this.parameters)

      // concat the data
      var data = this.algorithm1.concat(this.algorithm2)
      
      // aesthetic :
      // y : point's value on y axis
      // group : how to group data on x axis
      // color : color of the point / boxplot
      // label : displayed text in toolbox
      this.chart = exploding_boxplot(data, {y:'Performance Metrics',group:'Algorithm',color:'Algorithm',label:'Model'})
      this.chart.width(this.WH[0]*3) // interactive visualization
      this.chart.height(this.WH[1]) // interactive visualization
      //call chart on a div
      this.chart('#exploding_boxplot')

      // colorscale
      const previousColor = ['#8dd3c7','#8da0cb']
      // check for brushing
      var el = document.getElementsByClassName('d3-exploding-boxplot boxcontent')
      var overall = document.getElementsByClassName('overall')
      this.brushStatus = document.getElementsByClassName('extent')
      // on clicks
      
      var flagEmptyKNN = 0
      var flagEmptyRF = 0

      el[0].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point KNN')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[0]
          allPoints[i].style.opacity = '1.0'
        } 

        if (flagEmptyKNN == 0) {
          flagEmptyKNN = 1
        } else {
          flagEmptyKNN = 0
        }

        EventBus.$emit('updateFlagKNN', flagEmptyKNN)
        EventBus.$emit('PCPCall', 'KNN')
        EventBus.$emit('updateBarChart', [])
      }
      el[1].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point RF')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[1]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyRF == 0) {
          flagEmptyRF = 1
        } else {
          flagEmptyRF = 0
        }
      
        EventBus.$emit('updateFlagRF', flagEmptyRF)
        EventBus.$emit('PCPCall', 'RF')
        EventBus.$emit('updateBarChart', [])
      }

      overall[0].ondblclick = function () {
        flagEmptyKNN = 0
        flagEmptyRF = 0
        EventBus.$emit('alternateFlagLock', flagEmptyKNN)
      }

      // check if brushed through all boxplots and not only one at a time
      const myObserver = new ResizeObserver(entries => {
        EventBus.$emit('brusheAllOn')
      })
      var brushRect = document.querySelector('.extent')
      myObserver.observe(brushRect);
    },
    brushActivationAll () {
      // continue here and select the correct points.
      var limiter = this.chart.returnBrush()

      var algorithm = []
      const previousColor = ['#8dd3c7','#8da0cb']
      var modelsActive = []
      for (var j = 0; j < this.AllAlgorithms.length; j++) {
        algorithm = []
        if (this.AllAlgorithms[j] === 'KNN') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point KNN')
          algorithm = this.algorithm1
        } else {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point RF')
          algorithm = this.algorithm2
        }
        for (let k = 0; k < allPoints.length; k++) {
          if (algorithm[k]['Performance Metrics'] < limiter[0] && algorithm[k]['Performance Metrics'] > limiter[1]) {
            modelsActive.push(algorithm[k].ModelID)
          }
        }
        for (let i = 0; i < allPoints.length; i++) {
          if (this.AllAlgorithms[j] === 'KNN') {
            allPoints[i].style.fill = previousColor[0]
          } else {
            allPoints[i].style.fill = previousColor[1]
          }
        }

        if (modelsActive.length == 0) {
          for (let i = 0; i < allPoints.length; i++) {
            //if (modelsActive.indexOf(i) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '1.0'
            //}
          }
        } else if (modelsActive.length == allPoints.length) {
          for (let i = 0; i < allPoints.length; i++) {
            if (this.AllAlgorithms[j] === 'KNN') {
              allPoints[i].style.fill = previousColor[0]
              allPoints[i].style.opacity = '1.0'
            } else {
              allPoints[i].style.fill = previousColor[1]
              allPoints[i].style.opacity = '1.0'
            }
          }
        } else {
          for (let i = 0; i < allPoints.length; i++) {
            allPoints[i].style.opacity = '1.0'
            if (this.AllAlgorithms[j] === 'KNN') {
              if (modelsActive.indexOf(i) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else {
              if (modelsActive.indexOf(i+this.KNNModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            }
          }
        }
      }
      EventBus.$emit('sendParameters', this.parameters)
      EventBus.$emit('updateActiveModels', modelsActive)
      this.UpdateBarChart()
    },
    brushed () {
      if (this.selectedAlgorithm == 'KNN') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point KNN')
      } else {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point RF')
      }
      const previousColor = ['#8dd3c7','#8da0cb']
      var modelsActive = []
      for (let j = 0; j < this.brushedBoxPl.length; j++) {
        modelsActive.push(this.brushedBoxPl[j].model)
      }
      for (let i = 0; i < allPoints.length; i++) {
        if (this.selectedAlgorithm == 'KNN') {
          allPoints[i].style.fill = previousColor[0]
        } else {
          allPoints[i].style.fill = previousColor[1]
        }
      }
      if (modelsActive.length == 0) {
        for (let i = 0; i < allPoints.length; i++) {
          //if (modelsActive.indexOf(i) == -1) {
            allPoints[i].style.fill = "#d3d3d3"
            allPoints[i].style.opacity = '1.0'
          //}
        }
      } else if (modelsActive.length == allPoints.length) {
        for (let i = 0; i < allPoints.length; i++) {
          if (this.selectedAlgorithm == 'KNN') {
            allPoints[i].style.fill = previousColor[0]
            allPoints[i].style.opacity = '1.0'
          } else {
            allPoints[i].style.fill = previousColor[1]
            allPoints[i].style.opacity = '1.0'
          }
        }
      } else {
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.opacity = '1.0'
          if (this.selectedAlgorithm == 'KNN') {
            if (modelsActive.indexOf(i) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else {
            if (modelsActive.indexOf(i+this.KNNModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          }
        }
      }
      EventBus.$emit('sendParameters', this.parameters)
      EventBus.$emit('updateActiveModels', modelsActive)
      this.UpdateBarChart()
    },
    UpdateBarChart () {
      var allPoints = document.getElementsByClassName('d3-exploding-boxplot point')
      var activeModels = []
      var algorithmsSelected = []
      var modelsSelected =[]
      for (let i = 0; i < allPoints.length; i++) {
        if (allPoints[i].style.fill != "rgb(211, 211, 211)") {
          activeModels.push(allPoints[i].__data__.Model)
          if (allPoints[i].__data__.Algorithm === 'KNN') {
            algorithmsSelected.push('KNN')
          }
          else {
            algorithmsSelected.push('RF')
          }
        }
      }
      if (activeModels.length == 0){
      } else {
        for (let i = 0; i<activeModels.length; i++) {
          var array = activeModels[i].split(';')
          var temp = array[0].split(' ')
          modelsSelected.push(temp[1])
        }
      }
      EventBus.$emit('updateBarChartAlgorithm', algorithmsSelected)
      EventBus.$emit('updateBarChart', modelsSelected)
    },
    selectedPointsPerAlgorithm () {
      var allPoints = document.getElementsByClassName('d3-exploding-boxplot point')
      var activeModels = []
      var algorithmsSelected = []
      var models = []
      for (let i = 0; i < allPoints.length; i++) {
        if (allPoints[i].style.fill != "rgb(211, 211, 211)") {
          activeModels.push(allPoints[i].__data__.Model)
          if (allPoints[i].__data__.Algorithm === 'KNN') {
            algorithmsSelected.push('KNN')
          }
          else {
            algorithmsSelected.push('RF')
          }
        }
      }
      if (activeModels.length == 0){
        alert('No models selected, please, retry!')
      } else {
        for (let i = 0; i<activeModels.length; i++) {
          var array = activeModels[i].split(';')
          var temp = array[0].split(' ')
          models.push(temp[1])
        }
        EventBus.$emit('ReturningAlgorithms', algorithmsSelected)
        EventBus.$emit('ReturningBrushedPointsIDs', models)
      }
    },
    previousBoxPlotState () {
      var el = document.getElementsByClassName('d3-exploding-boxplot box')
      if (document.getElementById('PCP').style.display == 'none') {
        
      } else {
        if (this.selectedAlgorithm == 'KNN') {
          $(el)[0].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'RF') {
          $(el)[2].dispatchEvent(new Event('click'))
        } else {

        }
      }
    }
  },
  mounted () {
    EventBus.$on('emittedEventCallingModelBrushed', this.selectedPointsPerAlgorithm)
    EventBus.$on('emittedEventCallingAllAlgorithms', data => {
      this.PerformanceAllModels = data})
    EventBus.$on('emittedEventCallingAllAlgorithms', this.boxplot)
    EventBus.$on('emittedEventCallingBrushedBoxPlot', data => {
      this.brushedBoxPl = data})
    EventBus.$on('emittedEventCallingBrushedBoxPlot', this.brushed),
    EventBus.$on('Responsive', data => {
      this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
      this.WH = data})
    EventBus.$on('ResponsiveandChange', this.boxplot)
    EventBus.$on('ResponsiveandChange', this.previousBoxPlotState)
    EventBus.$on('emittedEventCallingSelectedALgorithm', data => {
      this.selectedAlgorithm = data})
    EventBus.$on('brusheAllOn', this.brushActivationAll)

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }
}
</script>