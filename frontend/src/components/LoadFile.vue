<template>
    <b-container fluid class="bv-example-row">
        <b-row>
            <b-col cols="4">
                <mdb-card style="width: 22rem;">
                    <mdb-card-header color="primary-color" tag="h5" class="text-center">Hyper-Parameters Panel</mdb-card-header>
                        <mdb-card-body>
                            <mdb-card-text class="text-center">
                                <select id="selectFile">
                                    <option value="DiabetesC.csv">Pima Indian Diabetes</option>
                                    <option value="BreastC.csv">Breast Cancer Winconsin</option>
                                    <option value="IrisC.csv" selected>Iris</option>
                                    <option value="" hidden></option>
                                </select>
                                <button
                                id="fileInput"
                                type="file"
                                @click="upload">
                                <font-awesome-icon icon="upload" />
                                Upload</button>
                                <button
                                id="Execute"
                                @click="execute">
                                <font-awesome-icon icon="play" />
                                Execute</button>
                            </mdb-card-text>
                        </mdb-card-body>
                </mdb-card>
            </b-col>
            <b-col cols="4">
                <mdb-card style="width: 80rem;">
                    <mdb-card-header color="primary-color" tag="h5" class="text-center">Stacking Ensemble Learning Overview</mdb-card-header>
                        <mdb-card-body>
                          <div id="OverviewPlotly" class="OverviewPlotly"></div>
                        </mdb-card-body>
                </mdb-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
// import Papa from 'papaparse'
import axios from 'axios'
import { mdbCard, mdbCardBody, mdbCardText, mdbCardHeader } from 'mdbvue'
import * as Plotly from 'plotly.js'

export default {
  data () {
    return {
      Collection: 0,
      RetrieveValueCSV: 'IrisC',
      OverviewResults: 0
    }
  },
  methods: {
    DataBaseRequestDataSetName (fileName) {
      const path = `http://127.0.0.1:5000/data/ServerRequest`
      const postData = {
        fileName: fileName
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
          console.log('Send request to server! Excellent!')
        })
        .catch(error => {
          console.log(error)
        })
    },
    execute () {
      // const that = this
      // const fileToLoad = event.target.files[0]
      // const reader = new FileReader()
      const fileName = document.getElementById('selectFile')
      this.RetrieveValueCSV = fileName.options[fileName.selectedIndex].value
      this.RetrieveValueCSV = this.RetrieveValueCSV.split('.')[0]
      this.DataBaseRequestDataSetName(this.RetrieveValueCSV)
      this.getCollection()
      this.getOverviewResults()
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
    upload () {
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
          console.log(this.Collection)
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
          const colors = JSON.parse(this.OverviewResults[0])
          const MDSData = JSON.parse(this.OverviewResults[1])
          const classifiersInfo = JSON.parse(this.OverviewResults[2])

          var classifiersInfoProcessing = []
          let step = 0
          let doubleStep = 1
          for (let i = 0; i < classifiersInfo.length / 2; i++) {
            step++
            classifiersInfoProcessing[i] = 'ClassifierID: ' + step + '; Details: '
            for (let j = 0; j < Object.values(classifiersInfo[doubleStep]).length; j++) {
              classifiersInfoProcessing[i] = classifiersInfoProcessing[i] + Object.keys(classifiersInfo[doubleStep])[j] + ': ' + Object.values(classifiersInfo[doubleStep])[j]
            }
            doubleStep = doubleStep + 2
          }

          const trace = {
            x: MDSData[0],
            y: MDSData[1],
            mode: 'markers',
            text: classifiersInfoProcessing,
            marker: {
              color: colors,
              size: 12,
              colorscale: 'Viridis',
              colorbar: {
                title: 'Metrics Sum',
                titleside: 'Top'
              },
              reversescale: true
            }
          }
          const data = [trace]
          const layout = {
            title: 'Classifiers Performance MDS',
            xaxis: {
              visible: false
            },
            yaxis: {
              visible: false
            }
          }
          Plotly.newPlot('OverviewPlotly', data, layout)

          this.selectedPointsOverview()
        })
        .catch(error => {
          console.log(error)
        })
    },
    selectedPointsOverview () {
      const OverviewPlotly = document.getElementById('OverviewPlotly')
      OverviewPlotly.on('plotly_selected', function (evt) {
        const ClassifierIDsList = []
        for (let i = 0; evt.points.length; i++) {
          if (evt.points[i] === undefined) {
            break
          } else {
            const OnlyId = evt.points[i].text.split(';')
            ClassifierIDsList.push(OnlyId[0])
          }
        }
        const path = `http://127.0.0.1:5000/data/ServerRequestSelPoin`
        const postData = {
          ClassifiersList: ClassifierIDsList
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
            console.log('Send request to server! Excellent!')
          })
          .catch(error => {
            console.log(error)
          })
      })
    }
  },
  components: {
    mdbCard,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
