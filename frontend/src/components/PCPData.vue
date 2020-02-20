<template>
  <div id="PCPDataView" class="parcoords" style="width: 1200px; height:280px"></div>
</template>

<script>
import 'parcoord-es/dist/parcoords.css';
import ParCoords from 'parcoord-es';
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

import { EventBus } from '../main.js'

export default {
  name: 'PCPData',
  data () {
    return {
      PCPDataReceived: '',
      colorsValues: ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99']
    }
  },
  methods: {
    reset () {
      d3.selectAll("#PCPDataView > *").remove();
    },
    PCPView () {
      d3.selectAll("#PCPDataView > *").remove();
      const DataSetNew = JSON.parse(this.PCPDataReceived[2])
      var DataSetParse = JSON.parse(DataSetNew)
      const target_names = JSON.parse(this.PCPDataReceived[3])
      var colors = this.colorsValues

      this.pc = ParCoords()("#PCPDataView")
          .data(DataSetParse)
          .color(function(d, i) { return colors[target_names[i]] })
          .bundlingStrength(0) // set bundling strength
          .smoothness(0)
          .showControlPoints(false)
          .render()
          .brushMode('1D-axes')
          .reorderable()
          .interactive();
    },
  },
  // fix when selecting points the pcp should update!
  mounted() {
    EventBus.$on('emittedEventCallingDataPCP', data => { this.PCPDataReceived = data })
    EventBus.$on('emittedEventCallingDataPCP', this.PCPView)
    EventBus.$on('ResponsiveandChange', this.PCPView)

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }
}
</script>

<style>
  .parcoords svg {
    position: relative !important;
  }
</style>