<template>
    <div>
        <div class="squares-container" style="min-height: 307px;">
            <canvas id="main-canvas" ></canvas>
        </div>
    </div>
</template>

<script>
import * as d3Base from 'd3'

import { EventBus } from '../main.js'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

import * as Stardust from 'stardust-core'
import * as StardustGL from 'stardust-webgl'

export default {
  name: 'Provenance',
  data () {
    return {
        stackInformation: '',
        WH: [],
        data: [],
        counter: 0,
        typeCounter: [],
        typeColumnCounter: [],
        KNNModels: 576, //KNN models
        platform: ''
    }
  },
  methods: {
    reset () {
      if (this.platform == '') {

      } else {
        this.platform.clear();
      }
    },
    provenance () {
      var canvas = document.getElementById("main-canvas");
      var width = this.WH[0]*9 // interactive visualization
      var height = this.WH[1]*0.5 // interactive visualization

      var flagKNN = 0
      var flagRF = 0
      var StackInfo = JSON.parse(this.stackInformation[1])
      // Create a WebGL 2D platform on the canvas:
      this.platform = Stardust.platform("webgl-2d", canvas, width, height);
    
      for (let i = 0; i < StackInfo.length; i++) {
        if (StackInfo[i] < this.KNNModels){
          this.data.push({
            type:0, column:this.counter, height:height
          })
          flagKNN = 1
        } else {
          this.data.push({
            type:1, column:this.counter, height:height
          })
          flagRF = 1
        }
      }
      if (flagKNN == 1) {
        this.typeCounter.push(0)
      }
      if (flagRF == 1) {
        this.typeCounter.push(0)
      }
      this.typeColumnCounter.push(0)
      
      this.data.forEach(d => {
        if (d.column == this.counter) {
          d.typeIndex = this.typeCounter[d.type]++;
          d.typeColumnIndex = this.typeColumnCounter[d.column]++;
        }
      });

      // Convert the SVG file to Stardust mark spec.
      let isotype = new Stardust.mark.circle();

      // Create the mark object.
      let isotypes = Stardust.mark.create(isotype, this.platform);

      let isotypeHeight = 18;
      let colors = [[166,206,227], [31,120,180], [178,223,138], [51,160,44], [251,154,153], [227,26,28], [253,191,111], [255,127,0], [202,178,214], [106,61,154], [255,255,153], [177,89,40]];
      colors = colors.map(x => [x[0] / 255, x[1] / 255, x[2] / 255, 1]);

      let pScale = Stardust.scale.custom(`
              Vector2(
                  20 + column * 100 + typeColumnIndex % 5 * 8,
                  height - 10 - floor(typeColumnIndex / 5) * 10
              )
          `);
      pScale.attr("typeColumnIndex", d => d.typeColumnIndex);
      pScale.attr("column", d => d.column);
      pScale.attr("typeIndex", d => d.typeIndex);
      pScale.attr("type", d => d.type);
      pScale.attr("height", d => d.height);

      let qScale = Stardust.scale.custom(`
              Vector2(
                  65 + typeIndex % 30 * 8,
                  height - 10 - floor(typeIndex / 15) * 18
              )
          `);
      qScale.attr("typeIndex", d => d.typeIndex);
      qScale.attr("type", d => d.type);
      qScale.attr("height", d => d.height);

      let interpolateScale = Stardust.scale.interpolate("Vector2");
      interpolateScale.t(0);

      isotypes.attr("center", interpolateScale(pScale(), qScale()));
      isotypes.attr("radius", 4.0);
      isotypes.attr("color", d => colors[d.type]);

      isotypes.data(this.data);

      isotypes.render();
      this.counter = this.counter + 1
  }
  },
  mounted () {
    EventBus.$on('InitializeProvenance', data => {this.stackInformation = data})
    EventBus.$on('InitializeProvenance', this.provenance)
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }

}
</script>