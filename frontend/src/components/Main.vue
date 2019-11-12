<!-- Main Visualization View -->

<template>
  <div>
    <b-container fluid class="bv-example-row">
      <b-row class="md-3">
        <b-col cols="3">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Data and Performance Metrics Selection</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-center" >
                <DataSetExecController/>
                <SlidersController/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        <mdb-card style="margin-top: 15px">
          <mdb-card-header color="primary-color" tag="h5" class="text-center">Parameters Space Exploration Overview</mdb-card-header>
            <mdb-card-body>
              <Parameters/>
            </mdb-card-body>
          </mdb-card>
        </b-col>
        <b-col cols="3">
          <mdb-card>
             <mdb-card-header color="primary-color" tag="h5" class="text-center">Models Space Visualization
              [Sel.:{{OverSelLength}}/All:{{OverAllLength}}]
              </mdb-card-header>
              <mdb-card-body>
                <ScatterPlot/>
                <PerMetricBarChart/>
              </mdb-card-body>
          </mdb-card>
        </b-col>
        <b-col cols="3">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Predictions Space Visualization</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-center">
                <PredictionsSpace/>
                <BalancePredictions/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </b-col>
        <b-col cols="3">
           <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Data Space Visualization</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-center">
                <DataSpace/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </b-col>
      </b-row>
      <b-row class="mb-3 mt-3">
        <b-col cols="3">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Best Algorithms and HyperParameters Search [Sel.:{{valueSel}}/All:{{valueAll}}]</mdb-card-header>
              <mdb-card-body>
                  <Algorithms :width="width" :height="height"/>
                  <AlgorithmHyperParam/>
                  <mdb-card-text class="text-center" >
                    <Controller/>
                  </mdb-card-text>
              </mdb-card-body>
          </mdb-card>
        </b-col>
        <b-col cols="6">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center">Models Feature Selection</mdb-card-header>
            <b-row>
            <b-col cols="12">  
              <mdb-card-body>        
                <Heatmap/>
              </mdb-card-body>
            </b-col>
          </b-row>
            <mdb-card-text>
              <mdb-card-body>        
                <ToggleSelection/>
              </mdb-card-body>
            </mdb-card-text>
          </mdb-card>
        </b-col>
        <b-col cols="3">
          <mdb-card >
            <mdb-card>
              <mdb-card-header color="primary-color" tag="h5" class="text-center">Meta-Model Performance</mdb-card-header>
              <mdb-card-body>
                <FinalResultsLinePlot/>
              </mdb-card-body>
            </mdb-card>
          </mdb-card>
        </b-col>
      </b-row>
      <b-row>
          <b-col cols="3">
            <mdb-card>
              <mdb-card-header color="primary-color" tag="h5" class="text-center">Diverse Algorithms Exploration</mdb-card-header>
              <mdb-card-body>
                  <BarChart/>
              </mdb-card-body>
            </mdb-card>
          </b-col>
          <b-col cols="9">
            <mdb-card>
              <mdb-card-header color="primary-color" tag="h5" class="text-center">Current Stacking Ensemble and Provenance Visualization</mdb-card-header>
              <mdb-card-body>
                  <Provenance/>
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
import Controller from './Controller.vue'
import SlidersController from './SlidersController.vue'
import ScatterPlot from './ScatterPlot.vue'
import PerMetricBarChart from './PerMetricBarChart.vue'
import DataSpace from './DataSpace.vue'
import PredictionsSpace from './PredictionsSpace.vue'
import BalancePredictions from './BalancePredictions.vue'
import BarChart from './BarChart.vue'
import Heatmap from './Heatmap.vue'
import ToggleSelection from './ToggleSelection.vue'
import FinalResultsLinePlot from './FinalResultsLinePlot.vue'
import Provenance from './Provenance.vue'
import Parameters from './Parameters.vue'
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import { mdbCard, mdbCardBody, mdbCardText, mdbCardHeader } from 'mdbvue'
import { EventBus } from '../main.js'
import * as jQuery from 'jquery' 
import $ from 'jquery'
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default Vue.extend({
  name: 'Main',
  components: {
    DataSetExecController,
    Algorithms,
    AlgorithmHyperParam,
    Controller,
    SlidersController,
    ScatterPlot,
    PerMetricBarChart,
    DataSpace,
    PredictionsSpace,
    BalancePredictions,
    BarChart,
    Heatmap,
    ToggleSelection,
    Provenance,
    Parameters,
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
      PerformanceCheck: '',
      firstTimeFlag: 1,
      selectedModels_Stack: [],
      selectedAlgorithms: [],
      parametersofModels: [],
      reset: false,
      brushedBoxPlotUpdate: 0,
      width: 0,
      height: 0,
      combineWH: [],
      basicValuesFact: [],
      sumPerClassifier: [],
      valueSel: 0,
      valueAll: 0,
      OverSelLength: 0,
      OverAllLength: 0,
      toggle1: 1,
      toggle2: 1,
      toggle3: 1,
      modelsUpdate: [],
      AlgorithmsUpdate: [],
      SelectedMetricsForModels: [],
      DataPointsSel: '',
      DataPointsModels: ''
    }
  },
  methods: {
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
    getDatafromtheBackEnd () {
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
          if (this.firstTimeFlag == 1) {
            this.selectedModels_Stack.push(0)
            this.selectedModels_Stack.push(JSON.stringify(this.modelsUpdate))
            EventBus.$emit('InitializeProvenance', this.selectedModels_Stack)
          }
          this.firstTimeFlag = 0
          EventBus.$emit('InitializeMetricsBarChart', this.OverviewResults)
          this.valueSel = 0
          this.valueAll = 0
          var toggles = []
          toggles.push(this.toggle1)
          toggles.push(this.toggle2)
          toggles.push(this.toggle3)
          EventBus.$emit('emitToggles', this.OverviewResults)
          EventBus.$emit('emittedEventCallingToggles', toggles)
          EventBus.$emit('emittedEventCallingHeatmapView', this.OverviewResults)
          EventBus.$emit('emittedEventCallingDataSpacePlotView', this.OverviewResults)
          EventBus.$emit('emittedEventCallingPredictionsSpacePlotView', this.OverviewResults)
          EventBus.$emit('emittedEventCallingBalanceView', this.OverviewResults)
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
          console.log('Server successfully sent updated per class features!')
          EventBus.$emit('emittedEventCallingAllAlgorithms', this.PerformancePerModel)
          EventBus.$emit('emittedEventCallingBarChart', this.PerformancePerModel)
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendSelectedPointsToServer () {
      if (this.ClassifierIDsList === ''){
        this.OverSelLength = 0
        EventBus.$emit('resetViews')
      } else {
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
            this.OverSelLength = this.ClassifierIDsList.length
            EventBus.$emit('emittedEventCallingHeatmapView', this.OverviewResults)
            this.getSelectedModelsMetrics()
            this.getFinalResults()
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    RemoveFromStackModels () {
      const path = `http://127.0.0.1:5000/data/ServerRemoveFromStack`

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
      EventBus.$emit('GrayOutPoints', this.ClassifierIDsList)
      this.updatePredictionsSpace()
      this.getFinalResults()
      })
      .catch(error => {
      console.log(error)
      })
    },
    updatePredictionsSpace () {
      const path = `http://localhost:5000/data/UpdatePredictionsSpace`

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
          this.UpdatePredictions = response.data.UpdatePredictions
          console.log('Updating Predictions Space!')
          EventBus.$emit('updatePredictionsSpace', this.UpdatePredictions)
          EventBus.$emit('InitializeProvenance', this.UpdatePredictions)
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendSelectedDataPointsToServer () {

      const path = `http://127.0.0.1:5000/data/ServerRequestDataPoint`
    
      const postData = {
        DataPointsSel: this.DataPointsSel
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
          console.log('Sent the selected data points to the server!')
          this.getSelectedDataPointsModels()
        })
        .catch(error => {
          console.log(error)
        })
    },
    getSelectedDataPointsModels () {
      const path = `http://localhost:5000/data/ServerSentDataPointsModel`

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
          this.DataPointsModels = response.data.DataPointsModels
          console.log('Server successfully sent the new models for the scatterplot!')
          EventBus.$emit('UpdateModelsScatterplot', this.DataPointsModels)
        })
        .catch(error => {
          console.log(error)
        })
    },
    getSelectedModelsMetrics () {
      const path = `http://localhost:5000/data/BarChartSelectedModels`

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
          this.SelectedMetricsForModels = response.data.SelectedMetricsForModels
          console.log('Server successfully updated barchart for metrics based on selected models!')
          EventBus.$emit('UpdateBarChartperMetric', this.SelectedMetricsForModels)
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
      const postData = {
        models: this.modelsUpdate,
        algorithms: this.selectedAlgorithms
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
          this.getDatafromtheBackEnd()
        })
        .catch(error => {
          console.log(error)
        })
    },
    UpdateBarChartFeatures () {
      const path = `http://127.0.0.1:5000/data/FeaturesScoresUpdate`
      const postData = {
        models: this.modelsUpdate,
        algorithms: this.AlgorithmsUpdate
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
          console.log('Send request to server! Updating Barchart!')
          this.UpdateModelsFeaturePerformance()
        })
        .catch(error => {
          console.log(error)
        })
    },
    UpdateBasedonFeatures () {
      const path = `http://127.0.0.1:5000/data/FeaturesSelection`
        const postData = {
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
            console.log('Sent specific features per model!')
             this.getFinalResults()
          })
          .catch(error => {
            console.log(error)
          })
    },
    UpdateBrushBoxPlot () {
      EventBus.$emit('emittedEventCallingBrushedBoxPlot', this.brushedBoxPlotUpdate)
    },
    CallPCP () {
      EventBus.$emit('emittedEventCallingSelectedALgorithm', this.selectedAlgorithm)
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
    },
    UploadProcess () {
    },
    render (flag) {
      this.combineWH = []
      this.width = document.body.clientWidth / 12 - 30
      this.height = document.body.clientHeight / 3
      this.combineWH.push(this.width)
      this.combineWH.push(this.height)
      if(flag) {
        EventBus.$emit('Responsive', this.combineWH)
      }
      else {
        EventBus.$emit('ResponsiveandChange', this.combineWH)
      }
    },
    change () {
      this.render(false)
    },
    factors () {
      const path = `http://127.0.0.1:5000/data/factors`
      const postData = {
        Factors: this.basicValuesFact
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
          console.log('The client send the new factors! Done.')
          this.RetrieveNewColors()
        })
        .catch(error => {
          console.log(error)
        })
    },
    RetrieveNewColors () {
      const path = `http://127.0.0.1:5000/data/UpdateOverv`

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
          this.sumPerClassifierSel = response.data.Results
          console.log('Server successfully send the new colors!')
          EventBus.$emit('getColors',this.sumPerClassifierSel)
        })
        .catch(error => {
          console.log(error)
        })
    },
    updateToggle () {
      var toggles = []
      toggles.push(this.toggle1)
      toggles.push(this.toggle2)
      toggles.push(this.toggle3)
      EventBus.$emit('emittedEventCallingTogglesUpdate', toggles)
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
    window.addEventListener('resize', this.change)
  },
  mounted() {
    this.render(true)
    loadProgressBar()
    window.onbeforeunload = function(e) {
      return 'Dialog text here.'
    }
    $(window).on("unload", function(e) {
      alert('Handler for .unload() called.');
    })
    EventBus.$on('ReturningBrushedPointsIDs',  data => { this.modelsUpdate = data })
    //EventBus.$on('ReturningBrushedPointsIDs',  this.UpdateBarChartFeatures )
    EventBus.$on('ConfirmDataSet', this.fileNameSend)
    EventBus.$on('reset', this.Reset)
    EventBus.$on('UploadedFile', this.Reset)
    EventBus.$on('UploadedFile', this.UploadProcess)
    EventBus.$on('ReturningAlgorithms', data => { this.selectedAlgorithms = data })
    EventBus.$on('ReturningBrushedPointsParams', data => { this.parametersofModels = data; })
    EventBus.$on('SendSelectedPointsToServerEvent', data => { this.ClassifierIDsList = data })
    EventBus.$on('SendSelectedPointsToServerEvent', this.SendSelectedPointsToServer)
    EventBus.$on('SendSelectedDataPointsToServerEvent', data => { this.DataPointsSel = data })
    EventBus.$on('SendSelectedDataPointsToServerEvent', this.SendSelectedDataPointsToServer)
    EventBus.$on('SendSelectedFeaturesEvent', data => { this.SelectedFeaturesPerClassifier = data })
    EventBus.$on('SendSelectedFeaturesEvent', this.UpdateBasedonFeatures )
    EventBus.$on('SendToServerDataSetConfirmation', data => { this.RetrieveValueFile = data })
    EventBus.$on('PCPCall', data => { this.selectedAlgorithm = data })
    EventBus.$on('toggle1', data => { this.toggle1 = data })
    EventBus.$on('toggle2', data => { this.toggle2 = data })
    EventBus.$on('toggle3', data => { this.toggle3 = data })
    EventBus.$on('toggle1', this.updateToggle)
    EventBus.$on('toggle2', this.updateToggle)
    EventBus.$on('toggle3', this.updateToggle)
    EventBus.$on('PCPCall', this.CallPCP)
    EventBus.$on('PCPCallDB', this.SendBrushedParameters)
    EventBus.$on('UpdateBoxPlot', data => { this.brushedBoxPlotUpdate = data })
    EventBus.$on('UpdateBoxPlot', this.UpdateBrushBoxPlot)
    EventBus.$on('CallFactorsView', data => { this.basicValuesFact = data })
    EventBus.$on('CallFactorsView', this.factors)
    EventBus.$on('AllAlModels', data => {
      this.valueSel = data
      this.valueAll = data
    })
    EventBus.$on('sendPointsNumber', data => {this.OverSelLength = data})
    EventBus.$on('sendPointsNumber', data => {this.OverAllLength = data})
    EventBus.$on('AllSelModels', data => {this.valueSel = data})
    EventBus.$on('RemoveFromStack', this.RemoveFromStackModels)
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

body {
  left: 0px;
  right: 0px;
  top: 0px;
  bottom: 0px;
  margin: 0px;
}
</style>