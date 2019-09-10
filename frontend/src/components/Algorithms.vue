<template>
    <div>
        <div id="exploding_boxplot" class="exploding_boxplot" ref="myClickable"></div>
    </div>
</template>

<script>
import interact from 'interactjs'
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
      brushedBoxPl: [],
      previousColor: 0,
      selectedAlgorithm: 0,
      WH: []
    }
  },
  methods: {
    boxplot () {
      d3.selectAll("#exploding_boxplot > *").remove(); 
      //generate random data
        const PerformAlgor1 = JSON.parse(this.PerformanceAllModels[0])
        const PerformAlgor2 = JSON.parse(this.PerformanceAllModels[1])
        var algorithm1 = []
        var algorithm2 = []
        var median = []
        var sum = 0
        for (let i = 0; i < Object.keys(PerformAlgor1.mean_test_score).length; i++) {
          algorithm1.push({Accuracy: Object.values(PerformAlgor1.mean_test_score)[i]*100,Algorithm:'KNN',Model:'Model ' + i + ',  Accuracy '})
          sum = sum + Object.values(PerformAlgor1.mean_test_score)[i]*100
        }
        median.push(sum/Object.keys(PerformAlgor1.mean_test_score).length)
        sum = 0
        for (let i = 0; i < Object.keys(PerformAlgor2.mean_test_score).length; i++) {
          algorithm2.push({Accuracy: Object.values(PerformAlgor2.mean_test_score)[i]*100,Algorithm:'RF',Model:'Model ' + i + ',  Accuracy '})
          sum = sum + Object.values(PerformAlgor1.mean_test_score)[i]*100
        }
        var data = algorithm1.concat(algorithm2)
        /*median.push(sum/Object.keys(PerformAlgor2.mean_test_score).length)
        if (median[0] > median[1])
          var data = algorithm1.concat(algorithm2)
        else 
          var data = algorithm2.concat(algorithm1)*/

        // chart(data,aes)
        // aesthetic :
        // y : point's value on y axis
        // group : how to group data on x axis
        // color : color of the point / boxplot
        // label : displayed text in toolbox
        var chart = exploding_boxplot(data, {y:'Accuracy',group:'Algorithm',color:'Algorithm',label:'Model'})
        chart.width(this.WH[0]*3)
        chart.height(this.WH[1])
        //call chart on a div
        chart('#exploding_boxplot')

        var el = document.getElementsByClassName('d3-exploding-boxplot boxcontent')
        var doubleClick = document.getElementsByClassName('exploding_boxplot')
        doubleClick[0].ondblclick = function(d) {
          EventBus.$emit('PCPCallDB')
        }
        el[0].onclick = function() {
          EventBus.$emit('PCPCall', 'KNN')
        }
        el[1].onclick = function() {
          EventBus.$emit('PCPCall', 'RF')
        }
    },
    brushed () {
      var allPoints = document.getElementsByClassName("d3-exploding-boxplot point")
      const previousColor = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']
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
          if (modelsActive.indexOf(i) == -1) {
            allPoints[i].style.fill = "#d3d3d3"
            allPoints[i].style.opacity = '0.4'
          }
        }
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
  }
}
</script>
