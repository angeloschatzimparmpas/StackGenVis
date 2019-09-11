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
      pc: 0
    }
  },
  methods: {
    PCPView () {
      d3.selectAll("#PCP > *").remove(); 
      if (this.selAlgorithm != '') {
        var colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']
        var colorGiv = 0
        
        var Combined = 0
        if (this.selAlgorithm == 'KNN') {    
          Combined = JSON.parse(this.ModelsPerformance[0])
          colorGiv = colors[0]
        } else {
          Combined = JSON.parse(this.ModelsPerformance[1])
          colorGiv = colors[1]
        }
        var valuesPerf = Object.values(Combined['mean_test_score'])
        var ObjectsParams = Combined['params']
        var ArrayCombined = new Array(valuesPerf.length)
        for (let i = 0; i < valuesPerf.length; i++) {
            Object.assign(ObjectsParams[i], {performance: valuesPerf[i]}, {model: i})
            ArrayCombined[i] = ObjectsParams[i]
        }
        EventBus.$emit('AllAlModels', ArrayCombined.length)
        this.pc = ParCoords()("#PCP")
            .data(ArrayCombined)
            .color(colorGiv)
            .hideAxis(['model'])
            .bundlingStrength(0) // set bundling strength
            .smoothness(0)
            .bundleDimension('performance')
            .showControlPoints(false)
            .render()
            .brushMode('1D-axes')
            .interactive();

        this.pc.on("brush", function(d) {
          EventBus.$emit('AllSelModels', d.length)
          EventBus.$emit('UpdateBoxPlot', d)
        });
      }
    },
    sliders () {

    },
    brushed () {
        if (this.pc.brushed()) {
          EventBus.$emit('ReturningBrushedPoints', this.pc.brushed())
        } else {
          EventBus.$emit('ReturningBrushedPoints', this.pc.data())
        }
    },
    clear () {
        d3.selectAll("#PCP > *").remove(); 
    },
    None () {
      document.getElementById('PCP').style.cssText='display:none';
    },
    Reveal () {
      document.getElementById('PCP').style.cssText='height:200px;display:""';
    }
  },
  mounted() {
    EventBus.$on('emittedEventCallingModelBrushed', this.brushed)
    EventBus.$on('emittedEventCallingModelSelect', data => { this.selAlgorithm = data })
    EventBus.$on('emittedEventCallingModel', data => { this.ModelsPerformance = data })
    EventBus.$on('emittedEventCallingModel', this.PCPView)
    EventBus.$on('ResponsiveandChange', this.PCPView)
    EventBus.$on('emittedEventCallingModelClear', this.clear)
    EventBus.$on('slidersOn', this.None)
    EventBus.$on('PCPCall', this.Reveal)
  }
}
</script>