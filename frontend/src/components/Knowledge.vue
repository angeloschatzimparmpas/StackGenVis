<template>
  <button style="float: right;"
  id="know"
  v-on:click="knowClass">
  <font-awesome-icon icon="file-export" />
  {{ valueKnowE }}
  </button>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'Knowledge',
  data () {
    return {
      valueKnowE: 'Knowledge Extraction'
    }
  },
  methods: {
      knowClass () {
        EventBus.$emit('OpenModal')
      }
  }
}
</script>