<template>
<b-row>
    <b-col cols="12">
        <div id="barChart" class="barChart" style="min-height: 307px;"></div>
    </b-col>
</b-row>
</template>

<script>
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'BarChart',
  data () {
    return {
      PerformanceResults: '',
      ClassNamesOverview: '',
      algorithmsinBar: [],
      modelsSelectedinBar: [],
      factors: [1,1,1,0,0
      ,1,0,0,1,0
      ,0,1,0,0,0
      ,0,0,1,0,0
      ,0,1,1,1
      ],
      SVCModels: 576,
      GausNBModels: 736, 
      MLPModels: 1236,
      LRModels: 1356, 
      LDAModels: 1996,
      QDAModels: 2196,
      RFModels: 2446,
      ExtraTModels: 2606,
      AdaBModels: 2766,
      GradBModels: 2926,
      colorsValues: ['#808000','#008080','#bebada','#fccde5','#d9d9d9','#bc80bd','#ccebc5'],
      WH: []
    }
  },
  methods: {
    BarChartView () {
      const PerClassMetricsKNN = JSON.parse(this.PerformanceResults[2])
      const PerClassMetricsSVC = JSON.parse(this.PerformanceResults[10])
      const PerClassMetricsGausNB = JSON.parse(this.PerformanceResults[18])
      const PerClassMetricsMLP = JSON.parse(this.PerformanceResults[26])
      const PerClassMetricsLR = JSON.parse(this.PerformanceResults[34])
      const PerClassMetricsLDA = JSON.parse(this.PerformanceResults[42])
      const PerClassMetricsQDA = JSON.parse(this.PerformanceResults[50])
      const PerClassMetricsRF = JSON.parse(this.PerformanceResults[58])
      const PerClassMetricsExtraT = JSON.parse(this.PerformanceResults[66])
      const PerClassMetricsAdaB = JSON.parse(this.PerformanceResults[74])
      const PerClassMetricsGradB = JSON.parse(this.PerformanceResults[82])

      var KNNModels = []
      var SVCModels = []
      var GausNBModels = []
      var MLPModels = []
      var LRModels = []
      var LDAModels = []
      var QDAModels = []
      var RFModels = []
      var ExtraTModels = []
      var AdaBModels = []
      var GradBModels = []
      
      var factorsLocal = this.factors
      var divide = factorsLocal[6] + factorsLocal[7] + factorsLocal[8] + factorsLocal[9] + factorsLocal[10] + factorsLocal[11] + factorsLocal[15] + factorsLocal[16] + factorsLocal[17]
      var factorF1 = 1
      var factorPrec = 1
      var factorRecall = 1
      if (factorsLocal[15]!=0) {
        factorF1 = factorsLocal[15]
      } else if (factorsLocal[16]!=0) {
        factorF1 = factorsLocal[16]
      } else if (factorsLocal[17]!=0){
        factorF1 = factorsLocal[17]
      } else {
        factorF1 = 0
      }
      if (factorsLocal[6]!=0) {
        factorPrec = factorsLocal[6]
      } else if (factorsLocal[7]!=0) {
        factorPrec = factorsLocal[7]
      } else if (factorsLocal[8]!=0){
        factorPrec = factorsLocal[8]
      } else {
        factorPrec = 0
      }
      if (factorsLocal[9]!=0) {
        factorRecall = factorsLocal[9]
      } else if (factorsLocal[10]!=0) {
        factorRecall = factorsLocal[10]
      } else if (factorsLocal[11]!=0){
        factorRecall = factorsLocal[11]
      } else {
        factorRecall = 0
      }

      if (this.modelsSelectedinBar.length != 0){
          for (let i=0; i<this.algorithmsinBar.length;i++) {
              if (this.algorithmsinBar[i] === "KNN") {
                  KNNModels.push(JSON.parse(this.modelsSelectedinBar[i]))
              } else if (this.algorithmsinBar[i] === "SVC") {
                  SVCModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.SVCModels)
              } else if (this.algorithmsinBar[i] === "GausNB") {
                  GausNBModels.push(JSON.parse(this.modelsSelectedinBar[i] - this.GausNBModels))
              } else if (this.algorithmsinBar[i] === "MLP") {
                  MLPModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.MLPModels)
              } else if (this.algorithmsinBar[i] === "LR") {
                  LRModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.LRModels)
              } else if (this.algorithmsinBar[i] === "LDA") {
                  LDAModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.LDAModels)
              } else if (this.algorithmsinBar[i] === "QDA") {
                  QDAModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.QDAModels)
              } else if (this.algorithmsinBar[i] === "RF") {
                  RFModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.RFModels)
              } else if (this.algorithmsinBar[i] === "ExtraT") {
                  ExtraTModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.ExtraTModels)
              } else if (this.algorithmsinBar[i] === "AdaB") {
                  AdaBModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.AdaBModels)
              } else {
                  GradBModels.push(JSON.parse(this.modelsSelectedinBar[i]) - this.GradBModels)
              }
          }
      }
      
      var target_names
      target_names = Object.keys(PerClassMetricsKNN)

      var sum = []
      var tempKNN = 0
      var tempSVC = 0
      var tempGausNB = 0
      var tempMLP = 0
      var tempLR = 0
      var tempLDA = 0
      var tempQDA = 0
      var tempRF = 0
      var tempExtraT = 0
      var tempAdaB = 0
      var tempGradB = 0

      var storeKNN = []
      var storeSVC = []
      var storeGausNB = []
      var storeMLP = []
      var storeLR = []
      var storeLDA = []
      var storeQDA = []
      var storeRF = []
      var storeExtraT = []
      var storeAdaB = []
      var storeGradB = []

      for (var i=0;i<target_names.length;i++) {
        tempKNN = 0
        tempSVC = 0
        tempGausNB = 0
        tempMLP = 0
        tempLR = 0
        tempLDA = 0
        tempQDA = 0
        tempRF = 0
        tempExtraT = 0
        tempAdaB = 0
        tempGradB = 0
        storeKNN[target_names[i]] = []
        storeSVC[target_names[i]] = []
        storeGausNB[target_names[i]] = []
        storeMLP[target_names[i]] = []
        storeLR[target_names[i]] = []
        storeLDA[target_names[i]] = []
        storeQDA[target_names[i]] = []
        storeRF[target_names[i]] = []
        storeExtraT[target_names[i]] = []
        storeAdaB[target_names[i]] = []
        storeGradB[target_names[i]] = []
        for (var k=0;k<Object.keys(PerClassMetricsKNN[target_names[i]]).length;k++){
          tempKNN = tempKNN + ((Object.values(PerClassMetricsKNN)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsKNN)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsKNN)[i][k]['recall']*factorRecall))/divide
          storeKNN[target_names[i]][k] = 100*((Object.values(PerClassMetricsKNN)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsKNN)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsKNN)[i][k]['recall']*factorRecall))/divide
        }
        tempKNN = tempKNN/Object.keys(PerClassMetricsKNN[target_names[i]]).length
        sum.push(tempKNN)
        for (var k=0;k<Object.keys(PerClassMetricsSVC[target_names[i]]).length;k++){
          tempSVC = tempSVC + ((Object.values(PerClassMetricsSVC)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsSVC)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsSVC)[i][k]['recall']*factorRecall))/divide
          storeSVC[target_names[i]][k] = 100*((Object.values(PerClassMetricsSVC)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsSVC)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsSVC)[i][k]['recall']*factorRecall))/divide
        }
        tempSVC = tempSVC/Object.keys(PerClassMetricsSVC[target_names[i]]).length
        sum.push(tempSVC)
        for (var k=0;k<Object.keys(PerClassMetricsGausNB[target_names[i]]).length;k++){
          tempGausNB = tempGausNB + ((Object.values(PerClassMetricsGausNB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGausNB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGausNB)[i][k]['recall']*factorRecall))/divide
          storeGausNB[target_names[i]][k] = 100*((Object.values(PerClassMetricsGausNB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGausNB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGausNB)[i][k]['recall']*factorRecall))/divide
        }
        tempGausNB = tempGausNB/Object.keys(PerClassMetricsGausNB[target_names[i]]).length
        sum.push(tempGausNB)
        for (var k=0;k<Object.keys(PerClassMetricsMLP[target_names[i]]).length;k++){
          tempMLP = tempMLP + ((Object.values(PerClassMetricsMLP)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsMLP)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsMLP)[i][k]['recall']*factorRecall))/divide
          storeMLP[target_names[i]][k] = 100*((Object.values(PerClassMetricsMLP)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsMLP)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsMLP)[i][k]['recall']*factorRecall))/divide
        }
        tempMLP = tempMLP/Object.keys(PerClassMetricsMLP[target_names[i]]).length
        sum.push(tempMLP)
        for (var k=0;k<Object.keys(PerClassMetricsLR[target_names[i]]).length;k++){
          tempLR = tempLR + ((Object.values(PerClassMetricsLR)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLR)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLR)[i][k]['recall']*factorRecall))/divide
          storeLR[target_names[i]][k] = 100*((Object.values(PerClassMetricsLR)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLR)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLR)[i][k]['recall']*factorRecall))/divide
        }
        tempLR = tempLR/Object.keys(PerClassMetricsLR[target_names[i]]).length
        sum.push(tempLR)
        for (var k=0;k<Object.keys(PerClassMetricsLDA[target_names[i]]).length;k++){
          tempLDA = tempLDA + ((Object.values(PerClassMetricsLDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLDA)[i][k]['recall']*factorRecall))/divide
          storeLDA[target_names[i]][k] = 100*((Object.values(PerClassMetricsLDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLDA)[i][k]['recall']*factorRecall))/divide
        }
        tempLDA = tempLDA/Object.keys(PerClassMetricsLDA[target_names[i]]).length
        sum.push(tempLDA)
        for (var k=0;k<Object.keys(PerClassMetricsQDA[target_names[i]]).length;k++){
          tempQDA = tempQDA + ((Object.values(PerClassMetricsQDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsQDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsQDA)[i][k]['recall']*factorRecall))/divide
          storeQDA[target_names[i]][k] = 100*((Object.values(PerClassMetricsQDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsQDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsQDA)[i][k]['recall']*factorRecall))/divide
        }      
        tempQDA = tempQDA/Object.keys(PerClassMetricsQDA[target_names[i]]).length
        sum.push(tempQDA)
        for (var k=0;k<Object.keys(PerClassMetricsRF[target_names[i]]).length;k++){
          tempRF = tempRF + ((Object.values(PerClassMetricsRF)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsRF)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsRF)[i][k]['recall']*factorRecall))/divide
          storeRF[target_names[i]][k] = 100*((Object.values(PerClassMetricsRF)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsRF)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsRF)[i][k]['recall']*factorRecall))/divide
        }
        tempRF = tempRF/Object.keys(PerClassMetricsRF[target_names[i]]).length
        sum.push(tempRF)
        for (var k=0;k<Object.keys(PerClassMetricsExtraT[target_names[i]]).length;k++){
          tempExtraT = tempExtraT + ((Object.values(PerClassMetricsExtraT)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsExtraT)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsExtraT)[i][k]['recall']*factorRecall))/divide
          storeExtraT[target_names[i]][k] = 100*((Object.values(PerClassMetricsExtraT)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsExtraT)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsExtraT)[i][k]['recall']*factorRecall))/divide
        }
        tempExtraT = tempExtraT/Object.keys(PerClassMetricsExtraT[target_names[i]]).length
        sum.push(tempExtraT)
        for (var k=0;k<Object.keys(PerClassMetricsAdaB[target_names[i]]).length;k++){
          tempAdaB = tempAdaB + ((Object.values(PerClassMetricsAdaB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsAdaB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsAdaB)[i][k]['recall']*factorRecall))/divide
          storeAdaB[target_names[i]][k] =  100*((Object.values(PerClassMetricsAdaB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsAdaB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsAdaB)[i][k]['recall']*factorRecall))/divide
        }
        tempAdaB = tempAdaB/Object.keys(PerClassMetricsAdaB[target_names[i]]).length
        sum.push(tempAdaB)
        for (var k=0;k<Object.keys(PerClassMetricsGradB[target_names[i]]).length;k++){
          tempGradB = tempGradB + ((Object.values(PerClassMetricsGradB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGradB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGradB)[i][k]['recall']*factorRecall))/divide
          storeGradB[target_names[i]][k] = 100*((Object.values(PerClassMetricsGradB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGradB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGradB)[i][k]['recall']*factorRecall))/divide
        }
        tempGradB = tempGradB/Object.keys(PerClassMetricsGradB[target_names[i]]).length
        sum.push(tempGradB)
      }

      var sumLine = []
      tempKNN = 0
      tempSVC = 0
      tempGausNB = 0
      tempMLP = 0
      tempLR = 0
      tempLDA = 0
      tempQDA = 0
      tempRF = 0
      tempExtraT = 0
      tempAdaB = 0
      tempGradB = 0
      for (var i=0;i<target_names.length;i++) {
        tempKNN = 0
        tempSVC = 0
        tempGausNB = 0
        tempMLP = 0
        tempLR = 0
        tempLDA = 0
        tempQDA = 0
        tempRF = 0
        tempExtraT = 0
        tempAdaB = 0
        tempGradB = 0
        if (KNNModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsKNN[target_names[i]]).length;k++){
              tempKNN = tempKNN + ((Object.values(PerClassMetricsKNN)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsKNN)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsKNN)[i][k]['recall']*factorRecall))/divide
            }
            tempKNN = tempKNN/Object.keys(PerClassMetricsKNN[target_names[i]]).length
        } else {
            for (var k=0;k<KNNModels.length;k++){
              tempKNN = tempKNN + ((Object.values(PerClassMetricsKNN)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsKNN)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsKNN)[i][k]['recall']*factorRecall))/divide
            }
            tempKNN = tempKNN/KNNModels.length
        }
        sumLine.push(tempKNN)
        if (SVCModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsSVC[target_names[i]]).length;k++){
              tempSVC = tempSVC + ((Object.values(PerClassMetricsSVC)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsSVC)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsSVC)[i][k]['recall']*factorRecall))/divide
            }
            tempSVC = tempSVC/Object.keys(PerClassMetricsSVC[target_names[i]]).length
        } else {
            for (var k=0;k<SVCModels.length;k++){
              tempSVC = tempSVC + ((Object.values(PerClassMetricsSVC)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsSVC)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsSVC)[i][k]['recall']*factorRecall))/divide
            }
            tempSVC = tempSVC/SVCModels.length
        }
        sumLine.push(tempSVC)
        if (GausNBModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsGausNB[target_names[i]]).length;k++){
              tempGausNB = tempGausNB + ((Object.values(PerClassMetricsGausNB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGausNB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGausNB)[i][k]['recall']*factorRecall))/divide
            }
            tempGausNB = tempGausNB/Object.keys(PerClassMetricsGausNB[target_names[i]]).length
        } else {
            for (var k=0;k<GausNBModels.length;k++){
              tempGausNB = tempGausNB + ((Object.values(PerClassMetricsGausNB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGausNB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGausNB)[i][k]['recall']*factorRecall))/divide
            }
            tempGausNB = tempGausNB/GausNBModels.length
        }
        sumLine.push(tempGausNB)
        if (MLPModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsMLP[target_names[i]]).length;k++){
              tempMLP = tempMLP + ((Object.values(PerClassMetricsMLP)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsMLP)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsMLP)[i][k]['recall']*factorRecall))/divide
            }
            tempMLP = tempMLP/Object.keys(PerClassMetricsMLP[target_names[i]]).length
        } else {
            for (var k=0;k<MLPModels.length;k++){
              tempMLP = tempMLP + ((Object.values(PerClassMetricsMLP)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsMLP)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsMLP)[i][k]['recall']*factorRecall))/divide
            }
            tempMLP = tempMLP/MLPModels.length
        }
        sumLine.push(tempMLP)
        if (LRModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsLR[target_names[i]]).length;k++){
              tempLR = tempLR + ((Object.values(PerClassMetricsLR)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLR)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLR)[i][k]['recall']*factorRecall))/divide
            }
            tempLR = tempLR/Object.keys(PerClassMetricsLR[target_names[i]]).length
        } else {
            for (var k=0;k<LRModels.length;k++){
              tempLR = tempLR + ((Object.values(PerClassMetricsLR)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLR)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLR)[i][k]['recall']*factorRecall))/divide
            }
            tempLR = tempLR/LRModels.length
        }
        sumLine.push(tempLR)
        if (LDAModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsLDA[target_names[i]]).length;k++){
              tempLDA = tempLDA + ((Object.values(PerClassMetricsLDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLDA)[i][k]['recall']*factorRecall))/divide
            }
            tempLDA = tempLDA/Object.keys(PerClassMetricsLDA[target_names[i]]).length
        } else {
            for (var k=0;k<LDAModels.length;k++){
              tempLDA = tempLDA + ((Object.values(PerClassMetricsLDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsLDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsLDA)[i][k]['recall']*factorRecall))/divide
            }
            tempLDA = tempLDA/LDAModels.length
        }
        sumLine.push(tempLDA)
        if (QDAModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsQDA[target_names[i]]).length;k++){
              tempQDA = tempQDA + ((Object.values(PerClassMetricsQDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsQDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsQDA)[i][k]['recall']*factorRecall))/divide
            }
            tempQDA = tempQDA/Object.keys(PerClassMetricsQDA[target_names[i]]).length
        } else {
            for (var k=0;k<QDAModels.length;k++){
              tempQDA = tempQDA + ((Object.values(PerClassMetricsQDA)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsQDA)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsQDA)[i][k]['recall']*factorRecall))/divide
            }
            tempQDA = tempQDA/QDAModels.length
        }
        sumLine.push(tempQDA)
        if (RFModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsRF[target_names[i]]).length;k++){
              tempRF = tempRF + ((Object.values(PerClassMetricsRF)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsRF)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsRF)[i][k]['recall']*factorRecall))/divide
            }
            tempRF = tempRF/Object.keys(PerClassMetricsRF[target_names[i]]).length
        } else {
            for (var k=0;k<RFModels.length;k++){
              tempRF = tempRF + ((Object.values(PerClassMetricsRF)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsRF)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsRF)[i][k]['recall']*factorRecall))/divide
            }
            tempRF = tempRF/RFModels.length
        }
        sumLine.push(tempRF)
        if (ExtraTModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsExtraT[target_names[i]]).length;k++){
              tempExtraT = tempExtraT + ((Object.values(PerClassMetricsExtraT)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsExtraT)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsExtraT)[i][k]['recall']*factorRecall))/divide
            }
            tempExtraT = tempExtraT/Object.keys(PerClassMetricsExtraT[target_names[i]]).length
        } else {
            for (var k=0;k<ExtraTModels.length;k++){
              tempExtraT = tempExtraT + ((Object.values(PerClassMetricsExtraT)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsExtraT)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsExtraT)[i][k]['recall']*factorRecall))/divide
            }
            tempExtraT = tempExtraT/ExtraTModels.length
        }
        sumLine.push(tempExtraT)
        if (AdaBModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsAdaB[target_names[i]]).length;k++){
              tempAdaB = tempAdaB + ((Object.values(PerClassMetricsAdaB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsAdaB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsAdaB)[i][k]['recall']*factorRecall))/divide
            }
            tempAdaB = tempAdaB/Object.keys(PerClassMetricsAdaB[target_names[i]]).length
        } else {
            for (var k=0;k<AdaBModels.length;k++){
              tempAdaB = tempAdaB + ((Object.values(PerClassMetricsAdaB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsAdaB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsAdaB)[i][k]['recall']*factorRecall))/divide
            }
            tempAdaB = tempAdaB/AdaBModels.length
        }
        sumLine.push(tempAdaB)
        if (GradBModels.length == 0) {
            for (var k=0;k<Object.keys(PerClassMetricsGradB[target_names[i]]).length;k++){
              tempGradB = tempGradB + ((Object.values(PerClassMetricsGradB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGradB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGradB)[i][k]['recall']*factorRecall))/divide
            }
            tempGradB = tempGradB/Object.keys(PerClassMetricsGradB[target_names[i]]).length
        } else {
            for (var k=0;k<GradBModels.length;k++){
              tempGradB = tempGradB + ((Object.values(PerClassMetricsGradB)[i][k]['f1-score']*factorF1)+(Object.values(PerClassMetricsGradB)[i][k]['precision']*factorPrec)+(Object.values(PerClassMetricsGradB)[i][k]['recall']*factorRecall))/divide
            }
            tempGradB = tempGradB/GradBModels.length
        }
        sumLine.push(tempGradB)
      }
      Plotly.purge('barChart')
      
      var layout = {
        autosize: true,
        barmode: 'group',
        width: this.WH[0]*10,
        height: this.WH[1]*0.635,
            xaxis: {
                title: 'Algorithm',
                type:"category",
                showticklabels: true,
                tickangle: 'auto',
                exponentformat: 'e',
                showexponent: 'all',
                side: 'top'
            },
            yaxis: {
                title: '# Performance (%) #',
            },
            xaxis2: {
                overlaying: 'x',
                type:"category",
                showticklabels: true,
                tickangle: 'auto',
                exponentformat: 'e',
                showexponent: 'all',
                side: 'top'
            },
        bargap:0.1,
        bargroupgap: 0.2,
        margin: {
            l: 50,
            r: 0,
            b: 30,
            t: 30,
            pad: 0
            },
        legend: {orientation: 'h', xanchor: 'center', x: 0.5},
        hovermode: 'closest'
      }
        var traces = []
        var tracesSel = []
        var data = []
        var sumList = []
        var sumLineList = []
        var keepSum
        var keepSumLine
        var loopStartUntil = sum.length/target_names.length
        for (var i = 0; i < target_names.length; i++) {
          keepSum = []
          keepSumLine = []
          for (var k = i*loopStartUntil; k < (i+1)*loopStartUntil; k++) {
            keepSum.push(sum[k]*100)
            keepSumLine.push(sumLine[k]*100)
          }
          sumList[i] = keepSum
          sumLineList[i] = keepSumLine
        }

        for (var i = 0; i < target_names.length; i++) {
          traces[i] = {
            x: ['KNN','SVC','GausNB','MLP','LR','LDA','QDA','RF','ExtraT','AdaB','GradB'],
            y: sumList[i],
            name: target_names[i],
            opacity: 0.5,
            marker: {
                opacity: 0.5,
                color: this.colorsValues[i]
            },
            type: 'bar'
            };
          tracesSel[i] = {
              type: 'bar',
              x: ['KNN','SVC','GausNB','MLP','LR','LDA','QDA','RF','ExtraT','AdaB','GradB'],
              y: sumLineList[i],
              name: target_names[i]+' (Sel)',
              xaxis: 'x2',
              mode: 'markers',
              marker: {
                  opacity: 1.0,
                  color: this.colorsValues[i],
              },
              width: [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
              };
              data.push(traces[i])
              data.push(tracesSel[i])
          }
          var barc = document.getElementById('barChart');

          Plotly.newPlot(barc, data, layout)
          var X, Y;

          barc.on('plotly_click', (eventData) => {
            var tName 
            eventData.points.forEach((e) => {
              tName = e.data.name.replace(/ *\([^)]*\) */g, "")
            });

            EventBus.$emit('clearPCP')
            EventBus.$emit('alternateFlagLock')
            EventBus.$emit('boxplotSet', [storeKNN[tName],storeSVC[tName],storeGausNB[tName],storeMLP[tName],storeLR[tName],storeLDA[tName],storeQDA[tName],storeRF[tName],storeExtraT[tName],storeAdaB[tName],storeGradB[tName]])
            EventBus.$emit('boxplotCall', false)
          });
      },
      reset () 
      {
        setTimeout(() => {
          Plotly.purge('barChart')
        }, 50);
      }
    },
    mounted() {
      EventBus.$on('updateBarChartAlgorithm', data => { this.algorithmsinBar = data })
      EventBus.$on('updateBarChart', data => { this.modelsSelectedinBar = data })
      EventBus.$on('updateBarChart', this.BarChartView)
      EventBus.$on('emittedEventCallingBarChart', data => { this.PerformanceResults = data })
      EventBus.$on('emittedEventCallingBarChart', this.BarChartView)
      EventBus.$on('emittedEventCallingUpdateBarChart', data => { this.ModelsChosen = data })
      EventBus.$on('emittedEventCallingUpdateBarChart', this.BarChartView)

      EventBus.$on('Responsive', data => {
          this.WH = data})
      EventBus.$on('ResponsiveandChange', data => {
          this.WH = data})

      EventBus.$on('CallFactorsView', data => { this.factors = data })
      EventBus.$on('CallFactorsView', this.BarChartView)

      // reset view
      EventBus.$on('resetViews', this.reset)
    }
}
</script>