<template>
    <div>
        <div id="exploding_boxplot" class="exploding_boxplot"></div>
    </div>
</template>

<script>
import interact from 'interactjs'
import { EventBus } from '../main.js'
import * as d3Base from 'd3'
import * as exploding_boxplot from 'd3_exploding_boxplot'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default {
  name: 'Algorithms',
  data () {
    return {
      PerformanceAllModels: ''
    }
  },
  methods: {
    boxplot () {
      //generate random data
      const PerformAlgor1 = JSON.parse(this.PerformanceAllModels[0])
      const PerformAlgor2 = JSON.parse(this.PerformanceAllModels[1])
      var algorithm1 = []
      var algorithm2 = []
      var median = []
      var sum = 0
      for (let i = 0; i < Object.keys(PerformAlgor1.mean_test_score).length; i++) {
        algorithm1.push({Performance: Object.values(PerformAlgor1.mean_test_score)[i]*100,Algorithm:'KNN',Model:'Model ' + i + ',  Accuracy '})
        sum = sum + Object.values(PerformAlgor1.mean_test_score)[i]*100
      }
      median.push(sum/Object.keys(PerformAlgor1.mean_test_score).length)
      sum = 0
      for (let i = 0; i < Object.keys(PerformAlgor2.mean_test_score).length; i++) {
        algorithm2.push({Performance: Object.values(PerformAlgor2.mean_test_score)[i]*100,Algorithm:'RF',Model:'Model ' + i + ',  Accuracy '})
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
      var chart = exploding_boxplot(data, {y:'Performance',group:'Algorithm',color:'Algorithm',label:'Model'})

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
    }
  },
  mounted () {
    EventBus.$on('emittedEventCallingAllAlgorithms', data => {
      this.PerformanceAllModels = data})
    EventBus.$on('emittedEventCallingAllAlgorithms', this.boxplot)
    }
}
</script>

<style>
@import 'd3_exploding_boxplot/src/d3_exploding_boxplot.css';
</style>
