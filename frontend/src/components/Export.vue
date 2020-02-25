<template>
  <div id="ExportResults">
  Data Instances: {{ DataPickled }}
  <br>
  =======================================================
  <br>
  Data Features Per Model: {{ FeaturesPickled }}
  <br>
  =======================================================
  <br>
  Models IDs and Parameters: {{ ModelsPickled }}
  </div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Cryo from 'cryo'
export default {
  name: 'Export',
  data () {
    return {
      DataPickled: '',
      FeaturesPickled: '',
      ModelsPickled: '',
      stackData: [],
      stackFeatures: [],
      stackModels: [],
    }
  },
  methods: {
    Pickle () {
      this.DataPickled = Cryo.stringify(this.stackData)
      this.FeaturesPickled = Cryo.stringify(this.stackFeatures)
      this.ModelsPickled = Cryo.stringify(this.stackModels)
    }
  },
  mounted () {
    EventBus.$on('sendDatatoPickle', data => {
    this.stackData = data})
    EventBus.$on('sendDatatoPickle', this.Pickle)

    EventBus.$on('sendSelectedFeaturestoPickle', data => {
    this.stackFeatures = data})
    EventBus.$on('sendSelectedFeaturestoPickle', this.Pickle)

    EventBus.$on('ExtractResults', data => {
    this.stackModels = data})
    EventBus.$on('ExtractResults', this.Pickle)
  }
}
</script>

<style scoped>
#ExportResults {
  word-break: break-all !important;
}
</style>