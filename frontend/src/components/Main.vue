<!-- Main Visualization View -->

<template>
<body>
    <b-container fluid class="bv-example-row">
      <b-row class="md-3">
        <b-col cols="3" >
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center" style="background-color: #C0C0C0;">Data Sets and Performance Metrics Manager</mdb-card-header>
              <mdb-card-body>
                <mdb-card-text class="text-left" style="font-size: 18.5px;">
                  <DataSetExecController/>
                  <SlidersController/>
                </mdb-card-text>
              </mdb-card-body>
          </mdb-card>
        </b-col>
        <b-col cols="6">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center" style="background-color: #C0C0C0;">History of the Stacking Ensemble<small class="float-right"><knowledge/></small></mdb-card-header>
            <mdb-card-body>
                <Provenance/>
            </mdb-card-body>
          </mdb-card>
        </b-col>
        <b-col cols="3">
            <mdb-card>
              <mdb-card-header color="primary-color" tag="h5" class="text-center" style="background-color: #C0C0C0;"><small class="float-left" style="padding-top: 3px;"><font-awesome-icon class="fa-lg" icon="dice-four"/>&nbsp;Metrics Support: [M1, M3-M5 (W)]</small>Metamodel's Performance</mdb-card-header>
              <mdb-card-body>
                <FinalResultsLinePlot/>
              </mdb-card-body>
            </mdb-card>
        </b-col>
      </b-row>
      <hr/>
      <ul class="nav nav-tabs" id="myTab" role="tablist" style="margin-top: 15px">
      <li class="nav-item">
        <a class="nav-link active" id="home-tab" data-toggle="tab" href="#home" role="tab" aria-controls="home" aria-selected="true">Algorithms' Exploration</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="profile-tab" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false">Data Wrangling</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="contact-tab" data-toggle="tab" href="#contact" role="tab" aria-controls="contact" aria-selected="false">Models' Exploration</a>
      </li>
      </ul>
      <div class="tab-content" id="myTabContent">
        <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
          <b-row class="md-3">
            <b-col cols="3">
              <mdb-card style="margin-top: 15px">
                <mdb-card-header color="primary-color" tag="h5" class="text-center">Overview of the Algorithms Space</mdb-card-header>
                <mdb-card-body class="text-center">
                  <Parameters/>
                </mdb-card-body>
              </mdb-card>
            </b-col>
            <b-col cols="9">
              <mdb-card style="margin-top: 15px;">
                <mdb-card-header color="primary-color" tag="h5" class="text-center"><small class="float-left" style="padding-top: 3px;">Metrics Support: [All]</small>Performance of the Algorithms [Sel: {{valueSel}} / All: {{valueAll}}]<small class="float-right" style="font-size:85% !important"><Controller/></small></mdb-card-header>
                  <mdb-card-body>
                      <Algorithms :width="width" :height="height"/>
                  </mdb-card-body>
              </mdb-card>
            </b-col>
          </b-row>
          <b-row class="md-3">
            <b-col cols="3">
              <mdb-card style="margin-top: 15px">
                <mdb-card-header color="primary-color" tag="h5" class="text-center"><small class="float-left" style="padding-top: 3px;">Metrics Support: [All]</small>Parameters Manipulation for Each Algorithm</mdb-card-header>
                <mdb-card-body>
                  <AlgorithmHyperParam/>
                </mdb-card-body>
              </mdb-card>
            </b-col>
            <b-col cols="9">
              <mdb-card style="margin-top: 15px;">
                <mdb-card-header color="primary-color" tag="h5" class="text-center"><small class="float-left" style="padding-top: 3px;"><font-awesome-icon class="fa-lg" icon="dice-three"/>&nbsp;Metrics Support: [M3*, M4*, M5* (F1 Score)]</small>Performance of the Algorithms for Each Class<small class="float-right"><ResetClass/></small></mdb-card-header>
                <mdb-card-body>
                    <BarChart/>
                </mdb-card-body>
              </mdb-card>
            </b-col>
          </b-row>
        </div>
        <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
          <b-row class="md-3">
              <b-col cols="6">
              <mdb-card style="margin-top: 15px;">
                  <mdb-card-header color="primary-color" tag="h5" class="text-center">Data Space</mdb-card-header>
                  <mdb-card-body>
                    <mdb-card-text class="text-center" style="min-height: 845px">
                      <DataSpace/>
                      <PCPData/>
                    </mdb-card-text>
                  </mdb-card-body>
                </mdb-card>
              </b-col>
              <b-col cols="6">
                <mdb-card style="margin-top: 15px;">
                  <mdb-card-header color="primary-color" tag="h5" class="text-center">Features Selection for Each Model<small class="float-right"><active/></small></mdb-card-header>
                    <mdb-card-body>
                      <mdb-card-text class="text-center" style="min-height: 845px">
                        <ToggleSelection/>
                        <br/>
                        <Heatmap/>
                      </mdb-card-text>
                    </mdb-card-body>
                </mdb-card>    
              </b-col>
            </b-row>
        </div>
        <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">
          <b-row class="md-3">
              <b-col cols="6">
                <mdb-card style="margin-top: 15px;">
                  <mdb-card-header color="primary-color" tag="h5" class="text-center"><small class="float-left" style="padding-top: 3px;">Metrics Support: [All]</small>Models' Space
                    [Sel: {{OverSelLength}} / All: {{OverAllLength}}]
                    </mdb-card-header>
                    <mdb-card-body>
                      <mdb-card-text class="text-center"  style="min-height: 845px">
                        <ScatterPlot/>
                        <PerMetricBarChart/>
                      </mdb-card-text>
                    </mdb-card-body>
                </mdb-card>
              </b-col>
              <b-col cols="6">
                <mdb-card style="margin-top: 15px;">
                  <mdb-card-header color="primary-color" tag="h5" class="text-center">Predictions' Space</mdb-card-header>
                  <mdb-card-body>
                    <mdb-card-text class="text-center"  style="min-height: 845px">
                      <PredictionsSpace/>
                      <BalancePredictions/>
                    </mdb-card-text>
                  </mdb-card-body>
                </mdb-card>
              </b-col>
            </b-row>
        </div>
      </div>
    </b-container>
  <div class="w3-container">
    <div id="myModal" class="w3-modal" style="position: fixed;">
      <div class="w3-modal-content w3-card-4 w3-animate-zoom">
        <header class="w3-container w3-blue"> 
        <h3 style="display:inline-block; font-size: 16px; margin-top: 15px; margin-bottom:15px">Serialized Data and Stacking Ensemble Learning Models using Cryo</h3>
        </header>
        <Export/>
        <div class="w3-container w3-light-grey w3-padding">
        <button style="float: right; margin-top: -3px; margin-bottom: -3px"
          id="closeModal" class="w3-button w3-right w3-white w3-border" 
          v-on:click="closeModalFun">
          <font-awesome-icon icon="window-close" />
          {{ valuePickled }}
          </button>
        </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>

import Vue from 'vue'
import DataSetExecController from './DataSetExecController.vue'
import Algorithms from './Algorithms.vue'
import AlgorithmHyperParam from './AlgorithmHyperParam.vue'
import Controller from './Controller.vue'
import ResetClass from './ResetClass.vue'
import Knowledge from './Knowledge.vue'
import Active from './Active.vue'
import Export from './Export.vue'
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
import PCPData from './PCPData.vue'
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import { mdbCard, mdbCardBody, mdbCardText, mdbCardHeader } from 'mdbvue'
import { EventBus } from '../main.js'
import * as jQuery from 'jquery' 
import $ from 'jquery'
import * as d3Base from 'd3'
import Papa from 'papaparse'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default Vue.extend({
  name: 'Main',
  components: {
    DataSetExecController,
    Algorithms,
    Export,
    AlgorithmHyperParam,
    Controller,
    ResetClass,
    Knowledge,
    Active,
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
    PCPData,
    FinalResultsLinePlot,
    mdbCard,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText
  },
  data () {
    return {
      valuePickled: 'Close',
      Collection: 0,
      OverviewResults: 0,
      preDataResults: '',
      DataResults: '',
      keyNow: 1,
      instancesImportance: '',
      RetrieveValueFile: 'HeartC', // this is for the default data set
      ClassifierIDsList: '',
      SelectedFeaturesPerClassifier: '',
      FinalResults: 0,
      Algorithms: ['KNN','SVC','GausNB','MLP','LR','LDA','QDA','RF','ExtraT','AdaB','GradB'],
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
      DataPointsModels: '',
      dataPointsSelfromDataSpace: '',
      userSelectedFilterMain: 'mean',
      actionData: '',
      filterData: '',
      provenanceData: '',
      localFile: '',
      toggleDeepMain: 1,
    }
  },
  methods: {
    openModalFun () {
      $('#myModal').modal('show')
    },
    closeModalFun () {
      $('#myModal').modal('hide')
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
            EventBus.$emit('ParametersProvenance', this.OverviewResults)
            EventBus.$emit('InitializeProvenance', this.selectedModels_Stack)
          }
          this.firstTimeFlag = 0
          EventBus.$emit('InitializeMetricsBarChart', this.OverviewResults)
          this.valueSel = 0
          this.valueAll = 0
          var toggles = []
          if (this.toggleDeepMain == 1) {
            toggles.push(this.toggle1)
            toggles.push(this.toggle2)
            toggles.push(this.toggle3)
          } else {
            toggles.push(1)
            toggles.push(0)
            toggles.push(0)
          }
          EventBus.$emit('emitToggles', this.OverviewResults)
          EventBus.$emit('emittedEventCallingToggles', toggles)
          EventBus.$emit('emittedEventCallingHeatmapView', this.OverviewResults)
          EventBus.$emit('emittedEventCallingPredictionsSpacePlotView', this.OverviewResults)
          EventBus.$emit('emittedEventCallingBalanceView', this.OverviewResults)
          this.DataSpaceCall()
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
    SendToServerData () {
      const path = `http://127.0.0.1:5000/data/SendtoSeverDataSet`

      const postData = {
        uploadedData: this.localFile
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
        console.log('Sent the new uploaded data to the server!')
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
        console.log(this.keyNow)
        this.OverSelLength = this.ClassifierIDsList.length
        const path = `http://127.0.0.1:5000/data/ServerRequestSelPoin`
        const postData = {
          ClassifiersList: this.ClassifierIDsList,
          keyNow: this.keyNow,
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
            if (this.keyNow == 0) {
              this.OverAllLength = this.ClassifierIDsList.length
              EventBus.$emit('GrayOutPoints', this.ClassifierIDsList)
            }
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
        ClassifiersList: this.ClassifierIDsList,
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
      EventBus.$emit('updateFlagForFinalResults', 0)
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
          if (this.keyNow == 1) {
            EventBus.$emit('InitializeProvenance', this.UpdatePredictions)
            EventBus.$emit('sendKeyScatt', 1)
            EventBus.$emit('GrayOutPoints', this.ClassifierIDsList)
          }
          EventBus.$emit('updatePredictionsSpace', this.UpdatePredictions)
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendSelectedDataPointsToServer () {
      // set a path from which the server will receive the seleceted predictions points
      const path = `http://127.0.0.1:5000/data/ServerRequestDataPoint`
      // brushing and linking between predictions space and data space 
      EventBus.$emit('updateDataSpaceHighlighting', this.DataPointsSel)

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
          var resultsPerMetricUpdated = JSON.parse(this.DataPointsModels[2])
          console.log('Server successfully sent the new models for the scatterplot!')
          EventBus.$emit('UpdateModelsScatterplot', this.DataPointsModels)
          EventBus.$emit('InitializeMetricsBarChartPrediction', JSON.stringify(resultsPerMetricUpdated))
          EventBus.$emit('UpdateBalanceView', this.DataPointsModels)
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
      if (this.RetrieveValueFile == "local") {
        this.DataSpaceCall()
        this.SendAlgorithmsToServer()
      } else {
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
      }
    },
    DataSpaceCall () {
       const path = `http://localhost:5000/data/requestDataSpaceResults`

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
          this.preDataResults = response.data.preDataResults
          EventBus.$emit('emittedEventCallingDataPCP', this.preDataResults)
          EventBus.$emit('emittedEventCallingDataSpacePlotView', this.preDataResults)
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendAlgorithmsToServer () {
      const path = `http://127.0.0.1:5000/data/ServerRequestSelParameters`
      const postData = {
        Algorithms: this.Algorithms,
        Toggle: this.toggleDeepMain
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
      console.log(this.SelectedFeaturesPerClassifier)
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
          EventBus.$emit('resetViews')
        })
        .catch(error => {
          console.log(error)
        })
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
      console.log(this.basicValuesFact)
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
          // this is if we need to change the factors even before models are there
          //if (this.OverviewResults != 0) {
            this.RetrieveNewColors()
         // }
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
    },
    DataSpaceFun () {
      const path = `http://127.0.0.1:5000/data/SendDataSpacPoints`
      const postData = {
        points: this.dataPointsSelfromDataSpace
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
          console.log('Send request to server! Brushed points sent successfully!')
        })
        .catch(error => {
          console.log(error)
        })
    },
    FilterFun () {
      const path = `http://127.0.0.1:5000/data/UpdateFilter`
      const postData = {
        filter: this.filterData
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
          console.log('Send request to server! Updated filter!')
        })
        .catch(error => {
          console.log(error)
        })
    },
    ActionFun () {
      const path = `http://127.0.0.1:5000/data/UpdateAction`
      const postData = {
        action: this.actionData
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
          console.log('Send request to server! Updated action!')
          this.getDatafromtheBackEnd()
        })
        .catch(error => {
          console.log(error)
        })
    },
    ProvenanceControlFun () {
      const path = `http://127.0.0.1:5000/data/UpdateProvenanceState`
      const postData = {
        provenance: this.provenanceData
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
          console.log('Send request to server! Updated provenance state!')
          if (this.provenanceData == 'restore') {
            this.getDatafromtheBackEnd()
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    Alg () {
      $('#profile-tab').on('click', function (e) {
        EventBus.$emit('Algorithm', false)
      })

      $('#contact-tab').on('click', function (e) {
        EventBus.$emit('Algorithm', false)
      })

      $('#home-tab').on('click', function (e) {
        var delayInMilliseconds = 1000; //1 second

        setTimeout(function() {
          EventBus.$emit('Algorithm', true)
        }, delayInMilliseconds);
      })
    },
  },
  created () {
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

    this.Alg()
    var modal = document.getElementById('myModal')
    window.onclick = function(event) {
      //alert(event.target)
        if (event.target == modal) {
            modal.style.display = "none";
        } 
    }
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
    EventBus.$on('ReturningAlgorithms', data => { this.selectedAlgorithms = data })
    EventBus.$on('ReturningBrushedPointsParams', data => { this.parametersofModels = data; })

    EventBus.$on('ChangeKey', data => { this.keyNow = data })
    EventBus.$on('SendSelectedPointsToServerEvent', data => { this.ClassifierIDsList = data })
    EventBus.$on('SendSelectedPointsToServerEvent', this.SendSelectedPointsToServer)

    EventBus.$on('SendSelectedDataPointsToServerEvent', data => { this.DataPointsSel = data })
    EventBus.$on('SendSelectedDataPointsToServerEvent', this.SendSelectedDataPointsToServer)
    EventBus.$on('SendSelectedFeaturesEvent', data => { this.SelectedFeaturesPerClassifier = data })
    EventBus.$on('sendToServerFeatures', this.UpdateBasedonFeatures)
    EventBus.$on('SendToServerDataSetConfirmation', data => { this.RetrieveValueFile = data })
    EventBus.$on('SendToServerLocalFile', data => { this.localFile = data })
    EventBus.$on('SendToServerLocalFile', this.SendToServerData)
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

    EventBus.$on('RemoveFromStack', data => { this.ClassifierIDsList = data })
    EventBus.$on('RemoveFromStack', this.RemoveFromStackModels)

    EventBus.$on('OpenModal', this.openModalFun)

    EventBus.$on('SendSelectedPointsToServerEventfromData', data => {this.dataPointsSelfromDataSpace = data})
    EventBus.$on('SendSelectedPointsToServerEventfromData', this.DataSpaceFun)

    EventBus.$on('SendFilter', data => {this.filterData = data})
    EventBus.$on('SendFilter', this.FilterFun)

    EventBus.$on('SendAction', data => {this.actionData = data})
    EventBus.$on('SendAction', this.ActionFun)

    EventBus.$on('SendProvenance', data => {this.provenanceData = data})
    EventBus.$on('SendProvenance', this.ProvenanceControlFun)

    EventBus.$on('toggleDeep', data => {this.toggleDeepMain = data})

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

<style lang="scss">

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
  font-family: 'Helvetica', 'Arial', sans-serif !important;
  left: 0px;
  right: 0px;
  top: 0px;
  bottom: 0px;
  margin-top: -4px !important;
}

.modal-backdrop {
  z-index: -1 !important;
}

.card-body {
   padding: 0.60rem !important;
}

hr {
  margin-top: 1rem;
  margin-bottom: 1rem;
  border: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

@import './../assets/w3.css';
</style>