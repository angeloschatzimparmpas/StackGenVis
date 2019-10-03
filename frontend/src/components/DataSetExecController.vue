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
  id="Confirm"
  v-on:click="confirm">
  <font-awesome-icon icon="check" />
  {{ value }}
  </button>
  <button
  id="Reset"
  v-on:click="reset">
  <font-awesome-icon icon="trash" />
  {{ valueReset }}
  </button>
</div>
</template>

<script>
import Papa from 'papaparse'
import { EventBus } from '../main.js'

export default {
  name: 'DataSetExecController',
  data () {
    return {
      RetrieveValueCSV: 'IrisC',
      value: 'Confirm',
      valueReset: 'Reset',
    }
  },
  methods: {
    upload () {
      EventBus.$emit('UploadedFile')
    },
    selectDataSet () {   
      const fileName = document.getElementById('selectFile')
      this.RetrieveValueCSV = fileName.options[fileName.selectedIndex].value
      this.RetrieveValueCSV = this.RetrieveValueCSV.split('.')[0]
      EventBus.$emit('SendToServerDataSetConfirmation', this.RetrieveValueCSV)
    },
    reset () {
      EventBus.$emit('reset')
    },
    confirm () {
      EventBus.$emit('ConfirmDataSet')
    }
  }
}
</script>
