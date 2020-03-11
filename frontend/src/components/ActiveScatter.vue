<template>
  <button style="float: right;"
  id="updateActiveScatter"
  v-on:click="sendUpdateActiveScatter">
  <font-awesome-icon icon="calculator" />
  {{ valueActive }}
  </button>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'ActiveScatter',
  data () {
    return {
      valueActive: 'Compute Metamodel\'s Performance'
    }
  },
  methods: {
      sendUpdateActiveScatter () {
        EventBus.$emit('sendToServerSelectedScatter')
      }
  }
}
</script>