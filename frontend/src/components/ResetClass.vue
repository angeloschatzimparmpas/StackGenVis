<template>
  <button style="float: right;"
  id="ResetClass"
  v-on:click="resetClass">
  <font-awesome-icon icon="sync-alt" />
  {{ valueResetC }}
  </button>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'ResetClass',
  data () {
    return {
      valueResetC: 'Reset Class Optimization'
    }
  },
  methods: {
      resetClass () {
        EventBus.$emit('clearPCP')
        EventBus.$emit('alternateFlagLock')
        EventBus.$emit('boxplotCall', true)
      }
  }
}
</script>