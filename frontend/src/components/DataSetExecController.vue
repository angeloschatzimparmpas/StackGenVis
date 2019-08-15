<template>
<div>
  <select id="selectFile" @change="selectDataSet()">
      <option value="DiabetesC.csv">Pima Indian Diabetes</option>
      <option value="BreastC.csv">Breast Cancer Winconsin</option>
      <option value="IrisC.csv" selected>Iris</option>
      <option value="" hidden></option>
  </select>
  <button
  id="fileInput"
  type="file"
  @click="upload"
  class="mt-2 ml-2">
  <font-awesome-icon icon="upload"/>
  Upload</button>
  <button
  id="Execute"
  v-on:click="execute">
  <font-awesome-icon icon="play" />
  {{ value }}
  </button>
</div>
</template>

<script>
// import Papa from 'papaparse'
import { EventBus } from '../main.js'

export default {
  name: 'DataSetExecController',
  data () {
    return {
      RetrieveValueCSV: 'IrisC',
      value: 'Execute',
      InitializeEnsemble: false
    }
  },
  methods: {
    upload () {
      // const that = this
      // const fileToLoad = event.target.files[0]
      // const reader = new FileReader()
      /*
      reader.onload = fileLoadedEvent => {
      Papa.parse(fileLoadedEvent.target.result, {
      header: true,
      complete (results) {
      console.log('complete', results)
      that.doc = JSON.stringify(results.data, null, 2)
      },
      error (errors) {
      console.log('error', errors)
      }
      })
      }
      reader.readAsText(fileToLoad)
      */
    },
    selectDataSet () {   
      const fileName = document.getElementById('selectFile')
      this.RetrieveValueCSV = fileName.options[fileName.selectedIndex].value
      this.RetrieveValueCSV = this.RetrieveValueCSV.split('.')[0]
      EventBus.$emit('SendToServerDataSetConfirmation', this.RetrieveValueCSV)
    },
    execute () {
        this.InitializeEnsemble = true
        this.value = 'ReExecute'
        this.$emit('InitializeEnsembleLearningEvent')
    }
  }
}
</script>
