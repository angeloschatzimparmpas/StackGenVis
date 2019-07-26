<!-- Main Visualization View -->

<template>
<b-container fluid class="bv-example-row">
  <b-row class="md-3">
    <b-col cols="3">
      <mdb-card>
        <mdb-card-header color="primary-color" tag="h5" class="text-center">Data Set Selection</mdb-card-header>
        <mdb-card-body>
          <mdb-card-text class="text-center" > 
            <LoadFile
            v-on:RetrieveValueCSVEvent="updateCSVName($event)"
            />
          </mdb-card-text>
        </mdb-card-body>
      </mdb-card>
    </b-col>
    <b-col cols="4">
      <mdb-card>
        <mdb-card-header color="primary-color" tag="h5" class="text-center">Base Classifiers Overview</mdb-card-header>
        <mdb-card-body>
          <ScatterPlot/>
        </mdb-card-body>
      </mdb-card>
    </b-col>
    <b-col cols="5">
      <mdb-card>
        <mdb-card-header color="primary-color" tag="h5" class="text-center">Classifiers, Features, and Classes Chord Visualization</mdb-card-header>
        <mdb-card-body>        
          <StretchedChord/>
        </mdb-card-body>
      </mdb-card>
    </b-col>
  </b-row>
  <b-row class="mb-3 mt-3">
    <b-col cols="3">
      <mdb-card >
        <mdb-card-header color="primary-color" tag="h5" class="text-center">Hyper-Parameters Setting</mdb-card-header>
        <mdb-card-body>
          <mdb-card-text class="text-center">
            <ParametersSetting
            v-on:InitializeEnsembleLearningEvent="DataBaseRequestDataSetName()"
            />
          </mdb-card-text>
        </mdb-card-body>
      </mdb-card>
    </b-col>
  <b-col cols="6">
        <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Per Class Metrics Exploration</mdb-card-header>
                <mdb-card-body>
                  <BarChart/>
                </mdb-card-body>
        </mdb-card>
    </b-col>
  </b-row>
  <b-row>
      <b-col cols="3">
          <mdb-card>
              <mdb-card-header color="primary-color" tag="h5" class="text-center">Visual Mapping</mdb-card-header>
                  <mdb-card-body>
                      <mdb-card-text class="text-center">
                        <Tuning/>
                      </mdb-card-text>
              </mdb-card-body>
          </mdb-card>
      </b-col>
  </b-row>
</b-container>
</template>

<script>
import Vue from 'vue'
import LoadFile from './LoadFile.vue'
import ParametersSetting from './ParametersSetting.vue'
import ScatterPlot from './ScatterPlot.vue'
import BarChart from './BarChart.vue'
import StretchedChord from './StretchedChord.vue'
import Tuning from './Tuning.vue'
import axios from 'axios'
import { mdbCard, mdbCardBody, mdbCardText, mdbCardHeader } from 'mdbvue'
import { EventBus } from '../main.js'

export default Vue.extend({
  name: 'Main',
  components: {
    LoadFile,
    ParametersSetting,
    ScatterPlot,
    BarChart,
    StretchedChord,
    Tuning,
    mdbCard,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText
  },
  data () {
    return {
      Collection: 0,
      OverviewResults: 0,
      RetrieveValueFile: 'IrisC',
      ClassifierIDsList: ''
    }
  },
  methods: {
    updateCSVName (retrieving) {
      this.RetrieveValueFile = retrieving
    },
    DataBaseRequestDataSetName () {
      const path = `http://127.0.0.1:5000/data/ServerRequest`
      const postData = {
        fileName: this.RetrieveValueFile
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
        .then(response => {
          console.log('Send request to server! FileName was sent successfully!')
        })
        .catch(error => {
          console.log(error)
        })
        this.getCollection()
        this.getOverviewResults()
    },
    getCollection () {
      this.Collection = this.getCollectionFromBackend()
    },
    getCollectionFromBackend () {
      const path = `http://localhost:5000/data/ClientRequest`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.Collection = response.data.Collection
          console.log('Collection was overwritten with new data sent by the server!')
        })
        .catch(error => {
          console.log(error)
        })
    },
    getOverviewResults () {
      this.OverviewResults = this.getScatterplotDataFromBackend()
    },
    getScatterplotDataFromBackend () {
      const path = `http://localhost:5000/data/PlotClassifiers`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.OverviewResults = response.data.OverviewResults
          console.log('Server successfully sent all the data related to visualizations!')
          EventBus.$emit('emittedEventCallingScatterPlot', this.OverviewResults)
          EventBus.$emit('emittedEventCallingBarChart', this.OverviewResults)
          EventBus.$emit('emittedEventCallingChordView', this.OverviewResults)
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendSelectedPointsToServer () {
      const path = `http://127.0.0.1:5000/data/ServerRequestSelPoin`
      const postData = {
        ClassifiersList: this.ClassifierIDsList
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
        .then(response => {
          console.log('Sent the selected points to the server (scatterplot)!')
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  mounted() {
    EventBus.$on('SendSelectedPointsToServerEvent', data => { this.ClassifierIDsList = data })
    EventBus.$on('SendSelectedPointsToServerEvent', this.SendSelectedPointsToServer)
  }
})
</script>
