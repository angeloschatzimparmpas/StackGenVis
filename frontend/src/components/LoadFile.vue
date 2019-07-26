<template>
<div>
  <select id="selectFile" v-on:change="SelectedFileChange">
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
</div>
</template>

<script>
// import Papa from 'papaparse'

export default {
  name: 'LoadFile',
  data () {
    return {
      RetrieveValueCSV: 'IrisC'
    }
  },
  methods: {
    SelectedFileChange () {
      const fileName = document.getElementById('selectFile')
      this.RetrieveValueCSV = fileName.options[fileName.selectedIndex].value
      this.RetrieveValueCSV = this.RetrieveValueCSV.split('.')[0]
      this.$emit('RetrieveValueCSVEvent', this.RetrieveValueCSV)
    },
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
    }
  }
}
</script>
