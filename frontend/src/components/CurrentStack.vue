<template>
    <div>
        <div id="CircleChart"></div>
    </div>
</template>

<script>
import { EventBus } from '../main.js'
import CirclePack from 'circlepack-chart';

export default {
  name: 'CurrentStack',
  data () {
    return {

    }
  },
  methods: {
    stack () {
    console.log('mpike')
    const CHILDREN_PROB_DECAY = 1; // per level
    const MAX_CHILDREN = 1000;
    const MAX_VALUE = 100;
    function genNode(name='root', probOfChildren=1) {
      if (Math.random() < probOfChildren) {
        return {
          name,
          children: [...Array(Math.round(Math.random() * MAX_CHILDREN))]
            .map((_, i) => genNode(i, probOfChildren - CHILDREN_PROB_DECAY))
        }
      } else {
        return {
          name,
          value: Math.round(Math.random() * MAX_VALUE)
        }
      }
    }
    const color = d3.scaleOrdinal(d3.schemePaired);
    CirclePack()
      .data(genNode())
      .sort((a, b) => a.value - b.value) // sort ascending by size
      .color(d => color(d.name))
      .showLabels(false)
      .excludeRoot(true)
      .tooltipContent((d, node) => `Size: <i>${node.value}</i>`)
      (document.getElementById('CircleChart'));
    },
    mount () {
        this.stack()
    }
  }
}
</script>