<template>
    <div>
        <button
        id="Execute"
        v-on:click="execute">
        <font-awesome-icon icon="play" />
        {{ valueExecute }}
        </button>
  </div>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'Controller',
  data () {
    return {
      value: 'Add to Stack',
      valueExecute: 'Execute Stacking Ensemble'
    }
  },
  methods: {
      execute () {
        EventBus.$emit('PCPCallDB')
        //EventBus.$emit('InitializeEnsembleLearningEvent')
      }
  }
}
</script>