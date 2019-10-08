<template>
  <div id="PCP" class="parcoords" style="height:200px"></div>
</template>

<script>
import 'parcoord-es/dist/parcoords.css';
import ParCoords from 'parcoord-es';
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

import { EventBus } from '../main.js'

export default {
  name: 'AlgorithmHyperParam',
  data () {
    return {
      ModelsPerformance: 0,
      selAlgorithm: 0,
      pc: 0,
      KNNModels: 576 //KNN models
    }
  },
  methods: {
    PCPView () {
      d3.selectAll("#PCP > *").remove(); 
      if (this.selAlgorithm != '') {
        var colors = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']
        var colorGiv = 0
        
        var Combined = 0
        if (this.selAlgorithm == 'KNN') {    
          Combined = JSON.parse(this.ModelsPerformance[1])
          colorGiv = colors[0]
        } else {
          Combined = JSON.parse(this.ModelsPerformance[7])
          colorGiv = colors[1]
        }
        var valuesPerf = Object.values(Combined['0'])
        var ObjectsParams = Combined['params']
        var newObjectsParams = []
        var ArrayCombined = []
        var temp
        for (var i = 0; i < valuesPerf.length; i++) {
          if (this.selAlgorithm === 'KNN') {
            // There is a problem here!
            newObjectsParams.push({'weights':ObjectsParams[i].weights, 'algorithm':ObjectsParams[i].algorithm,'metric':ObjectsParams[i].metric,'n_neighbors':ObjectsParams[i].n_neighbors})
            Object.assign(newObjectsParams[i], {performance: valuesPerf[i]}, {model: i})
            ArrayCombined[i] = newObjectsParams[i]
          } else {
            Object.assign(ObjectsParams[i], {performance: valuesPerf[i]}, {model: this.KNNModels + i})
            ArrayCombined[i] = ObjectsParams[i]
          }
        }
        EventBus.$emit('AllAlModels', ArrayCombined.length)
        this.pc = ParCoords()("#PCP")
            .data(ArrayCombined)
            .color(colorGiv)
            .hideAxis(['model'])
            .bundlingStrength(0) // set bundling strength
            .smoothness(0)
            .showControlPoints(false)
            .render()
            .brushMode('1D-axes')
            .reorderable()
            .interactive();

        this.pc.on("brushend", function(d) {
          EventBus.$emit('AllSelModels', d.length)
          EventBus.$emit('UpdateBoxPlot', d)
        });
      }
    },
    sliders () {

    },

    clear () {
        d3.selectAll("#PCP > *").remove(); 
    },
  },
  mounted() {
    EventBus.$on('ReturningBrushedPointsModels', this.brushed)
    EventBus.$on('emittedEventCallingModelSelect', data => { this.selAlgorithm = data })
    EventBus.$on('emittedEventCallingModel', data => { this.ModelsPerformance = data })
    EventBus.$on('emittedEventCallingModel', this.PCPView)
    EventBus.$on('ResponsiveandChange', this.PCPView)
    EventBus.$on('emittedEventCallingModelClear', this.clear)
  }
}
</script>