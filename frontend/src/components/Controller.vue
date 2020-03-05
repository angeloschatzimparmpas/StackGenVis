<template>
  <button class="btn-outline-success" style="float: right;"
  id="Execute"
  v-on:click="execute">
  <font-awesome-icon icon="play" />
  {{ valueExecute }}
  </button>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'Controller',
  data () {
    return {
      valueExecute: 'Execute Stacking Ensemble'
    }
  },
  methods: {
      execute () {
        EventBus.$emit('PCPCallDB')
      }
  }
}
</script>