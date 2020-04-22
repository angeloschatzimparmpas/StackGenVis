<template>
  <button style="float: right;"
  id="addStack"
  v-on:click="valueActiveStFun">
  <font-awesome-icon icon="save" />
  {{ valueActiveSt }}
  </button>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'saveStack',
  data () {
    return {
      valueActiveSt: 'Store in a new Stack'
    }
  },
  methods: {
      valueActiveStFun () {
        EventBus.$emit('storeStack')
      }
  }
}
</script>