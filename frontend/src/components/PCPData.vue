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
      ClassifierIDsListClearedData: [],
      RetrieveDataSet: 'HeartC',
      smallScreenMode: '0px'
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
      const target_names_original = JSON.parse(this.PCPDataReceived[4])

      if (this.smallScreenMode != "370px") {
        var width = 1200
        var height = 248
      } else {
        var width = 800
        var height = 251
      }

      var extraction = []
      for (let i = 0; i < DataSetParse.length; i++) {
        if (this.RetrieveDataSet == 'IrisC') {
          extraction.push(Object.assign(DataSetParse[i], {Outcome: target_names[i]}, {ID: i}))
        } else {
          extraction.push(Object.assign(DataSetParse[i], {Outcome: target_names_original[i]}, {ID: i}))
        }

      }
      var colors = this.colorsValues
      EventBus.$emit('sendDatatoPickle', extraction)

      var highlighted = []
      for (let i = 0; i < DataSetParse.length; i++) {
        if (this.ClassifierIDsListClearedData.includes(i)) {
          highlighted[i] = DataSetParse[i]
        }
      }

      if (DataSetParse.length == this.ClassifierIDsListClearedData.length || this.ClassifierIDsListClearedData.length == 0) {
        var pc = ParCoords()("#PCPDataView")
            .data(DataSetParse)
            .width(width)
            .height(height)
            .hideAxis(["Outcome","ID"])
            .color(function(d, i) { return colors[d.Outcome] })
            .bundlingStrength(0) // set bundling strength
            .smoothness(0)
            .showControlPoints(false)
            .render()
            .brushMode('1D-axes')
            .reorderable()
            .interactive();
      }
      else {
        var pc = ParCoords()("#PCPDataView")
          .data(DataSetParse)
          .width(width)
          .height(height)
          .hideAxis(["Outcome","ID"])
          .color(function(d, i) { return colors[d.Outcome] })
          .bundlingStrength(0) // set bundling strength
          .smoothness(0)
          .showControlPoints(false)
          .render()
          .highlight(highlighted)
          .brushMode('1D-axes')
          .reorderable()
          .interactive();
      }
      pc.alphaOnBrushed(0.2);
      pc.on('brushend', function(brushed, args){
        var brushedCleared = []
        for (let i = 0; i < brushed.length; i++) {
          brushedCleared.push(brushed[i].ID)
        }
        EventBus.$emit('brushedDataSpace', brushedCleared)
    })

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

    EventBus.$on('SendToServerDataSetConfirmation', data => { this.RetrieveDataSet = data })

    EventBus.$on('ResponsiveandAdapt', data => { this.smallScreenMode = data })
  }
}
</script>

<style>
  .parcoords svg {
    position: relative !important;
  }
</style>