<template>
    <div>
        <div class="squares-container">
            <canvas id="main-canvas"></canvas>
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
        stackInformation: ''
    }
  },
  methods: {
    provenance () {
      var canvas = document.getElementById("main-canvas");
      var width = 960;
      var height = 500;

      // Create a WebGL 2D platform on the canvas:
      var platform = Stardust.platform("webgl-2d", canvas, width, height);
      var data = [];
  [27, 53, 91, 52, 112, 42, 107, 91, 68, 56, 115, 86, 26, 102, 28, 23, 119, 110].forEach((x, index) => {
    for (let i = 0; i < x; i++) {
      data.push({
        type: index % 3,
        column: Math.floor(index / 3)
      });
    }
  });
  var typeCounter = [0, 0, 0];
  var typeColumnCounter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  data.forEach(d => {
    d.typeIndex = typeCounter[d.type]++;
    d.typeColumnIndex = typeColumnCounter[3 * d.column + d.type]++;
  });
      // Convert the SVG file to Stardust mark spec.
      let isotype = new Stardust.mark.circle();

      // Create the mark object.
      let isotypes = Stardust.mark.create(isotype, platform);

      let isotypeHeight = 18;
     let colors = [[141,211,199], [255,255,179], [190,186,218]];
    colors = colors.map(x => [x[0] / 255, x[1] / 255, x[2] / 255, 1]);

    let pScale = Stardust.scale.custom(`
            Vector2(
                20 + column * 160 + type * 45 + typeColumnIndex % 5 * 8,
                460 - floor(typeColumnIndex / 5) * 10
            )
        `);
    pScale.attr("typeColumnIndex", d => d.typeColumnIndex);
    pScale.attr("column", d => d.column);
    pScale.attr("typeIndex", d => d.typeIndex);
    pScale.attr("type", d => d.type);

    let qScale = Stardust.scale.custom(`
            Vector2(
                65 + type * 300 + typeIndex % 30 * 8,
                460 - floor(typeIndex / 15) * 18
            )
        `);
    qScale.attr("typeIndex", d => d.typeIndex);
    qScale.attr("type", d => d.type);

    let interpolateScale = Stardust.scale.interpolate("Vector2");
    interpolateScale.t(0);

      isotypes.attr("center", interpolateScale(pScale(), qScale()));
      isotypes.attr("radius", 4.0);
      isotypes.attr("color", d => colors[d.type]);

      isotypes.data(data);

      isotypes.render();

  }
  },
  mounted () {
    EventBus.$on('InitializeProvenance', data => {this.stackInformation = data})
    EventBus.$on('InitializeProvenance', this.provenance)
  }

}
</script>