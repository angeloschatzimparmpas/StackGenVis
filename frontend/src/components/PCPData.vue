<template>
  <div id="PCPDataView" class="parcoords"></div>
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
      colorsValues: ['#808000','#008080','#bebada','#fccde5','#d9d9d9','#bc80bd','#ccebc5'],
      ClassifierIDsListClearedData: []
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
      this.ClassifierIDsListClearedData = DataSetParse.slice();
      const target_names = JSON.parse(this.PCPDataReceived[3])
      const target_names_original = JSON.parse(this.PCPDataReceived[4])

      var extraction = []
      for (let i = 0; i < DataSetParse.length; i++) {
        extraction.push(Object.assign(DataSetParse[i], {Outcome: target_names_original[i]}))
      }
      var colors = this.colorsValues
      EventBus.$emit('sendDatatoPickle', extraction)

      var highlighted = []
      for (let i = 0; i < this.ClassifierIDsListClearedData.length; i++) {
        highlighted.push(DataSetParse[i])
      }

      if (DataSetParse.length == this.ClassifierIDsListClearedData.length || this.ClassifierIDsListClearedData.length == 0)
        var pc = ParCoords()("#PCPDataView")
            .data(DataSetParse)
            .width(1200)
            .height(280)
            .hideAxis(["Outcome"])
            .color(function(d, i) { return colors[target_names[i]] })
            .bundlingStrength(0) // set bundling strength
            .smoothness(0)
            .showControlPoints(false)
            .render()
            .brushMode('1D-axes')
            .reorderable()
            .interactive();
      else {
        var pc = ParCoords()("#PCPDataView")
          .data(DataSetParse)
          .width(1200)
          .height(280)
          .hideAxis(["Outcome"])
          .color(function(d, i) { return colors[target_names[i]] })
          .bundlingStrength(0) // set bundling strength
          .smoothness(0)
          .showControlPoints(false)
          .render()
          .highlight(highlighted)
          .brushMode('1D-axes')
          .reorderable()
          .interactive();
      }

    },
  },
  // fix when selecting points the pcp should update!
  mounted() {
    EventBus.$on('SendSelectedPointsToServerEventfromData', data => { this.ClassifierIDsListClearedData = data })
    EventBus.$on('SendSelectedPointsToServerEventfromData', this.PCPView)

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