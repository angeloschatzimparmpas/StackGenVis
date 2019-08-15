<!-- Main Visualization View -->

<template>
  <div>
    <b-container fluid class="bv-example-row">
      <b-row class="md-3">
        <b-col cols="3">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Data Set Selection and Execution</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-center" >
                <DataSetExecController
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
        <b-col cols="3">
          <mdb-card-header color="primary-color" tag="h5" class="text-center">Data Space Visualization</mdb-card-header>
          <mdb-card-body>
            <mdb-card-text class="text-center">
              <DataSpace/>
            </mdb-card-text>
          </mdb-card-body>
        </b-col>
      </b-row>
      <b-row class="mb-3 mt-3">
        <b-col cols="3">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Algorithms Selection and HyperParameters Search</mdb-card-header>
              <mdb-card-body>
                  <Algorithms/>
                  <AlgorithmHyperParam/>
              </mdb-card-body>
          </mdb-card>
        </b-col>
        <b-col cols="6">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Subset Feature Selection Per Model</mdb-card-header>
            <b-row>
              <b-col cols="4">
                <mdb-card-body>        
                  <StretchedChord/>
                </mdb-card-body>
              </b-col>
            <b-col cols="4">  
              <mdb-card-body>        
                <Heatmap/>
              </mdb-card-body>
            </b-col>
            <b-col cols="4"> 
              <mdb-card-body>
                <FeatureSelection/>
              </mdb-card-body>
            </b-col>
          </b-row>
          </mdb-card>
        </b-col>
        <b-col cols="3">
          <mdb-card >
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Predictions Space Visualization</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-center">
                <PredictionsSpace/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </b-col>
      </b-row>
      <b-row>
          <b-col cols="3">
            <mdb-card>
              <mdb-card-header color="primary-color" tag="h5" class="text-center">Base Models Overview</mdb-card-header>
              <mdb-card-body>
                <ScatterPlot/>
              </mdb-card-body>
            </mdb-card>
          </b-col>
          <b-col cols="3" offset-md="6">
            <mdb-card>
              <mdb-card-header color="primary-color" tag="h5" class="text-center">Meta-Model Performance</mdb-card-header>
              <mdb-card-body>
                <FinalResultsLinePlot/>
              </mdb-card-body>
            </mdb-card>
          </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>

import Vue from 'vue'
import DataSetExecController from './DataSetExecController.vue'
import Algorithms from './Algorithms.vue'
import AlgorithmHyperParam from './AlgorithmHyperParam.vue'
import ScatterPlot from './ScatterPlot.vue'
import DataSpace from './DataSpace.vue'
import PredictionsSpace from './PredictionsSpace.vue'
import BarChart from './BarChart.vue'
import StretchedChord from './StretchedChord.vue'
import Heatmap from './Heatmap.vue'
import FeatureSelection from './FeatureSelection.vue'
import FinalResultsLinePlot from './FinalResultsLinePlot.vue'
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'
import { mdbCard, mdbCardBody, mdbCardText, mdbCardHeader } from 'mdbvue'
import { EventBus } from '../main.js'
import * as jQuery from 'jquery' 
import $ from 'jquery'

export default Vue.extend({
  name: 'Main',
  components: {
    DataSetExecController,
    Algorithms,
    AlgorithmHyperParam,
    ScatterPlot,
    DataSpace,
    PredictionsSpace,
    BarChart,
    StretchedChord,
    Heatmap,
    FeatureSelection,
    FinalResultsLinePlot,
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
      ClassifierIDsList: '',
      SelectedFeaturesPerClassifier: '',
      FinalResults: 0,
      Algorithms: ['KNN','RF'],
      selectedAlgorithm: '',
      PerformancePerModel: '',
      brushed: 0,
      brushedAll: [],
      ExecutionStart: false,
      reset: false,
      limitModels: 64
    }
  },
  methods: {
    DataBaseRequestDataSetName () {
      this.ExecutionStart = true
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
          EventBus.$emit('emittedEventCallingDataPlot', this.Collection)
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
          var length = JSON.parse(this.OverviewResults[0]).length
          console.log(this.ClassifierIDsList)
          if (length < this.limitModels) {
            this.OverviewResults.push(JSON.stringify(this.ClassifierIDsList))
            EventBus.$emit('emittedEventCallingBarChart', this.OverviewResults)
            EventBus.$emit('emittedEventCallingChordView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingHeatmapView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingTableView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingDataSpacePlotView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingPredictionsSpacePlotView', this.OverviewResults)
            this.OverviewResults.pop()
          }
          this.getFinalResults()
        })
        .catch(error => {
          console.log(error)
        })
    },
    getModelsPerformance () {
      this.ModelsPerformance = this.getModelsPerformanceFromBackend()
    },
    getModelsPerformanceFromBackend () {
      const path = `http://localhost:5000/data/PerformanceForEachModel`

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
          this.PerformancePerModel = response.data.PerformancePerModel
          console.log('Server successfully sent all the performance data related to models!')
          EventBus.$emit('emittedEventCallingAllAlgorithms', this.PerformancePerModel)
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
          if (this.ClassifierIDsList.length < this.limitModels) {
            this.OverviewResults.push(JSON.stringify(this.ClassifierIDsList))
            EventBus.$emit('emittedEventCallingBarChart', this.OverviewResults)
            EventBus.$emit('emittedEventCallingChordView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingHeatmapView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingTableView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingDataSpacePlotView', this.OverviewResults)
            EventBus.$emit('emittedEventCallingPredictionsSpacePlotView', this.OverviewResults)
            this.OverviewResults.pop()
          }
          this.getFinalResults()
        })
        .catch(error => {
          console.log(error)
        })
    },
    getFinalResults () {
      this.FinalResults = this.getFinalResultsFromBackend()
    },
    getFinalResultsFromBackend () {
      const path = `http://localhost:5000/data/SendFinalResultsBacktoVisualize`

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
          this.FinalResults = response.data.FinalResults
          EventBus.$emit('emittedEventCallingLinePlot', this.FinalResults)
        })
        .catch(error => {
          console.log(error)
        })
    },
    fileNameSend () {
        const path = `http://127.0.0.1:5000/data/ServerRequest`
          const postData = {
            fileName: this.RetrieveValueFile,
            featureSelection: this.SelectedFeaturesPerClassifier
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
                this.SendAlgorithmsToServer()
            })
            .catch(error => {
              console.log(error)
            })
    },
    SendAlgorithmsToServer () {
      const path = `http://127.0.0.1:5000/data/ServerRequestSelParameters`
      const postData = {
        Algorithms: this.Algorithms,
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
          console.log('Send request to server! Algorithm name was sent successfully!')
          this.getModelsPerformance()
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendBrushedParameters () {
      EventBus.$emit('emittedEventCallingModelBrushed')
      const path = `http://127.0.0.1:5000/data/SendBrushedParam`
      this.brushedAll.push(this.brushed)
      const postData = {
        brushed: this.brushed,
        algorithm: this.selectedAlgorithm
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
          console.log('Send request to server! Brushed parameters sent successfully!')
           if (!this.ExecutionStart) {
          } else {
            this.getCollection()
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    UpdateBasedonFeatures () {
      const path = `http://127.0.0.1:5000/data/FeaturesSelection`
        const postData = {
          featureSelection: this.SelectedFeaturesPerClassifier,
          brushedAll: this.brushedAll
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
            console.log('Sent specific features per model!')
             this.getFinalResults()
          })
          .catch(error => {
            console.log(error)
          })
    },
    CallPCP () {
      EventBus.$emit('emittedEventCallingModelClear')
      EventBus.$emit('emittedEventCallingModelSelect', this.selectedAlgorithm)
      EventBus.$emit('emittedEventCallingModel', this.PerformancePerModel)
    },
    Reset () {
      const path = `http://127.0.0.1:5000/data/Reset`
      this.reset = true
      const postData = {
        ClassifiersList: this.reset
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
          console.log('The server side was reset! Done.')
          this.reset = false
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created() {
    // does the browser support the Navigation Timing API?
    if (window.performance) {
        console.info("window.performance is supported");
    }
    // do something based on the navigation type...
    if(performance.navigation.type === 1) {
        console.info("TYPE_RELOAD");
        this.Reset();
    }
  },
  mounted() {
    loadProgressBar()
    this.fileNameSend()
    window.onbeforeunload = function(e) {
      return 'Dialog text here.'
    }
    $(window).on("unload", function(e) {
      alert('Handler for .unload() called.');
    })
    EventBus.$on('ReturningBrushedPoints', data => { this.brushed = data })
    EventBus.$on('SendSelectedPointsToServerEvent', data => { this.ClassifierIDsList = data })
    EventBus.$on('SendSelectedPointsToServerEvent', this.SendSelectedPointsToServer)
    EventBus.$on('SendSelectedFeaturesEvent', data => { this.SelectedFeaturesPerClassifier = data })
    EventBus.$on('SendSelectedFeaturesEvent', this.UpdateBasedonFeatures )
    EventBus.$on('SendToServerDataSetConfirmation', data => { this.RetrieveValueFile = data })
    EventBus.$on('SendToServerDataSetConfirmation', this.fileNameSend)
    EventBus.$on('PCPCall', data => { this.selectedAlgorithm = data })
    EventBus.$on('PCPCall', this.CallPCP)
    EventBus.$on('PCPCallDB', this.SendBrushedParameters)
    
    //Prevent double click to search for a word. 
    document.addEventListener('mousedown', function (event) {
      if (event.detail > 1) {
      event.preventDefault();
      // of course, you still do not know what you prevent here...
      // You could also check event.ctrlKey/event.shiftKey/event.altKey
      // to not prevent something useful.
      }
    }, false);
  },
})
</script>

<style>
#nprogress .bar {
background: red !important;
}

#nprogress .peg {
box-shadow: 0 0 10px red, 0 0 5px red !important;
}

#nprogress .spinner-icon {
border-top-color: red !important;
border-left-color: red !important;
}
</style>