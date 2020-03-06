<template>
  <button style="float: right;"
  id="updateActive"
  v-on:click="sendUpdateActive">
  <font-awesome-icon icon="calculator" />
  {{ valueActive }}
  </button>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'Active',
  data () {
    return {
      valueActive: 'Compute Metamodel\'s Performance'
    }
  },
  methods: {
      sendUpdateActive () {
        EventBus.$emit('sendToServerFeatures')
      }
  }
}
</script>