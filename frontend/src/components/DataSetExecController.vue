<template>
<div>
  <label id="data" for="param-dataset" data-toggle="tooltip" data-placement="right" title="Tip: use one of the data sets already provided or upload a new file.">{{ dataset }}</label>
  <select id="selectFile" @change="selectDataSet()">
      <option value="HeartC.csv" selected>Heart Disease</option>
      <option value="StanceC.csv">Stance in Texts</option>
      <option value="DiabetesC.csv">Pima Indian Diabetes</option>
      <option value="IrisC.csv">Iris</option>
      <option value="local">Upload New File</option>
  </select>

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
import {$,jQuery} from 'jquery';
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default {
  name: 'DataSetExecController',
  data () {
    return {
      RetrieveValueCSV: 'DiabetesC', // default value for the first data set
      value: 'Confirm',
      valueReset: 'Reset',
      dataset: 'Data set'
    }
  },
  methods: {
    selectDataSet () {   
      const fileName = document.getElementById('selectFile')
      this.RetrieveValueCSV = fileName.options[fileName.selectedIndex].value
      this.RetrieveValueCSV = this.RetrieveValueCSV.split('.')[0]

      if (this.RetrieveValueCSV == "DiabetesC" || this.RetrieveValueCSV == "HeartC" || this.RetrieveValueCSV == "IrisC" || this.RetrieveValueCSV == "StanceC") { // This is a function that handles a new file, which users can upload.
        this.dataset = "Data set"
        d3.select("#data").select("input").remove(); // Remove the selection field.
        EventBus.$emit('SendToServerDataSetConfirmation', this.RetrieveValueCSV)
      } else {
        EventBus.$emit('SendToServerDataSetConfirmation', this.RetrieveValueCSV)
        d3.select("#data").select("input").remove();
        this.dataset = ""
        var data
        d3.select("#data")
          .append("input")
          .attr("type", "file")
          .style("font-size", "18.5px")
          .style("width", "200px")
          .on("change", function() {
            var file = d3.event.target.files[0];
            Papa.parse(file, {
                header: true,
                dynamicTyping: true,
                skipEmptyLines: true,
                complete: function(results) {
                  data = results.data;
                  EventBus.$emit('SendToServerLocalFile', data)
                }
              });
          })
      }
    },
    reset () {
      EventBus.$emit('reset')
      EventBus.$emit('alternateFlagLock')
    },
    confirm () {
      EventBus.$emit('ConfirmDataSet')
    }
  }
}
</script>
