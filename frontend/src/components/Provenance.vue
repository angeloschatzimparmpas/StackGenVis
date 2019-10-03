<template>
    <div>
        <div class="squares-container">
            <canvas id="main-canvas"></canvas>
            <svg id="main-svg"></svg>
        </div>
    </div>
</template>

<script>
import { EventBus } from '../main.js'

export default {
  name: 'Provenance',
  data () {
    return {
    }
  },
  methods: {
    provenance () {
        var container = d3.select(".squares-container");
        var vis = new SquaresVisualization(container.node());
        loadData("mnist.csv", DATA => {
            vis.layout();
            vis.setInstances(DATA.slice(0, 4000));
            vis.setLayoutParameter({
            y0: 10,
            numberBins: 10,
            squaresPerBin: 11,
            squareSize: 3,
            squareSpacing: 4,
            xSpacing: 88
            });
        });
    }
  },
  mount () {
  }
}
</script>