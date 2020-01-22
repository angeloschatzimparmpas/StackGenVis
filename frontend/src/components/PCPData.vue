<template>
  <div id="PCPDataView" class="parcoords" style="width: 300px; height:200px"></div>
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
      colorsValues: ['#6a3d9a','#b15928','#e31a1c']
    }
  },
  methods: {
    PCPView () {
      d3.selectAll("#PCPDataView > *").remove();
      const target_names = JSON.parse(this.PCPDataReceived[3])
      const DataSet = JSON.parse(this.PCPDataReceived[5])
      const target = JSON.parse(this.PCPDataReceived[6])
      var colors = this.colorsValues

      this.pc = ParCoords()("#PCPDataView")
          .data(DataSet)
          .color(function(d, i) { return colors[target_names[i]] })
          .hideAxis([target,'_id','InstanceID'])
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
  }
}
</script>