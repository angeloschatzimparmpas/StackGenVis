<template>
<div>
  <label id="modeSel" for="param-dataset" data-toggle="tooltip" data-placement="right">{{ valueMode }}</label>
  <select id="selectMode" @click="clickMode()" @change="changeMode()">
    <option value="stack" selected>Stacking</option>
    <option value="blend">Blending</option>
  </select>
</div>
</template>

<script>

import { EventBus } from '../main.js'

export default {
  name: 'Mode',
  data () {
    return {
      valueMode: 'Method: ',
      defaultMode: 'stack'
    }
  },
  methods: {
      clickMode () {
        EventBus.$emit('ChangeOfMode', this.defaultMode) 
      },
      changeMode () {
        var methodRetrieved = document.getElementById('selectMode')
        this.defaultMode = methodRetrieved.options[methodRetrieved.selectedIndex].value
        EventBus.$emit('ChangeOfMode', this.defaultMode) 
      }
  }
}
</script>