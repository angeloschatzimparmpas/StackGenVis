<template>
  <div>
    <div id="exploding_boxplot" class="exploding_boxplot" style="min-height: 450px;"></div>
  </div>
</template>

<script>
import { EventBus } from '../main.js'
import * as d3Base from 'd3'
import * as exploding_boxplot from 'd3_exploding_boxplot'
import 'd3_exploding_boxplot/src/d3_exploding_boxplot.css'
import $ from 'jquery'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default {
  name: 'Algorithms',
  data () {
    return {
      PerformanceAllModels: '',
      brushedBoxPl: [],
      previousColor: 0,
      selectedAlgorithm: 0,
      AllAlgorithms: ['KNN','SVC','GauNB','MLP','LR','LDA','QDA','RF','ExtraT','AdaB','GradB'],
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
      listClassPerf: [],
      WH: [],
      keyAllOrClass: true,
      parameters: [],
      algorithm1: [],
      algorithm2: [],
      activeTabVal: true,
      factors: [1,0,0
      ,1,0,0,1,0
      ,0,1,0,0,0
      ,0,0,1,0,0
      ,0,1,1,1
      ],
      chart: '',
      flagEmpty: 0,
      ActiveModels: [],
    }
  },
  methods: {
    reset () {
      d3.selectAll("#exploding_boxplot > *").remove()
    },
    boxplot () {
      // reset the boxplot
      d3.selectAll("#exploding_boxplot > *").remove()

      // retrieve models ID
      const AlgorKNNIDs = this.PerformanceAllModels[0]
      const AlgorSVCIDs = this.PerformanceAllModels[9]
      const AlgorGausNBIDs = this.PerformanceAllModels[18]
      const AlgorMLPIDs = this.PerformanceAllModels[27]
      const AlgorLRIDs = this.PerformanceAllModels[36]
      const AlgorLDAIDs = this.PerformanceAllModels[45]
      const AlgorQDAIDs = this.PerformanceAllModels[54]
      const AlgorRFIDs = this.PerformanceAllModels[63]
      const AlgorExtraTIDs = this.PerformanceAllModels[72]
      const AlgorAdaBIDs = this.PerformanceAllModels[81]
      const AlgorGradBIDs = this.PerformanceAllModels[90]

      var factorsLocal = this.factors
      var divide = 0

      factorsLocal.forEach(element => {
        divide = element + divide
      });
      
      var McKNN = []
      const performanceAlgKNN = JSON.parse(this.PerformanceAllModels[6])
      for (let j = 0; j < Object.values(performanceAlgKNN['mean_test_accuracy']).length; j++) {
        let sumKNN
        sumKNN = (factorsLocal[0] * Object.values(performanceAlgKNN['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgKNN['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgKNN['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgKNN['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgKNN['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgKNN['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgKNN['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgKNN['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgKNN['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgKNN['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgKNN['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgKNN['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgKNN['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgKNN['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgKNN['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgKNN['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgKNN['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgKNN['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgKNN['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgKNN['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgKNN['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgKNN['log_loss'])[j]))
        McKNN.push((sumKNN/divide)*100)
      }
      var McSVC = []
      const performanceAlgSVC = JSON.parse(this.PerformanceAllModels[15])
      for (let j = 0; j < Object.values(performanceAlgSVC['mean_test_accuracy']).length; j++) {
        let sumSVC
        sumSVC = (factorsLocal[0] * Object.values(performanceAlgSVC['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgSVC['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgSVC['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgSVC['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgSVC['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgSVC['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgSVC['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgSVC['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgSVC['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgSVC['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgSVC['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgSVC['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgSVC['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgSVC['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgSVC['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgSVC['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgSVC['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgSVC['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgSVC['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgSVC['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgSVC['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgSVC['log_loss'])[j]))
        McSVC.push((sumSVC/divide)*100)
      }
      var McGausNB = []
      const performanceAlgGausNB = JSON.parse(this.PerformanceAllModels[24])
      for (let j = 0; j < Object.values(performanceAlgGausNB['mean_test_accuracy']).length; j++) {
        let sumGausNB 
        sumGausNB = (factorsLocal[0] * Object.values(performanceAlgGausNB['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgGausNB['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgGausNB['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgGausNB['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgGausNB['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgGausNB['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgGausNB['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgGausNB['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgGausNB['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgGausNB['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgGausNB['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgGausNB['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgGausNB['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgGausNB['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgGausNB['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgGausNB['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgGausNB['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgGausNB['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgGausNB['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgGausNB['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgGausNB['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgGausNB['log_loss'])[j]))
        McGausNB.push((sumGausNB/divide)*100)
      }
      var McMLP = []
      const performanceAlgMLP = JSON.parse(this.PerformanceAllModels[33])
      for (let j = 0; j < Object.values(performanceAlgMLP['mean_test_accuracy']).length; j++) {
        let sumMLP
        sumMLP = (factorsLocal[0] * Object.values(performanceAlgMLP['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgMLP['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgMLP['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgMLP['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgMLP['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgMLP['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgMLP['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgMLP['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgMLP['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgMLP['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgMLP['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgMLP['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgMLP['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgMLP['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgMLP['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgMLP['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgMLP['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgMLP['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgMLP['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgMLP['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgMLP['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgMLP['log_loss'])[j]))
      McMLP.push((sumMLP/divide)*100)
      }
      var McLR = []
      const performanceAlgLR = JSON.parse(this.PerformanceAllModels[42])
      for (let j = 0; j < Object.values(performanceAlgLR['mean_test_accuracy']).length; j++) {
        let sumLR
        sumLR = (factorsLocal[0] * Object.values(performanceAlgLR['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgLR['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgLR['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgLR['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgLR['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgLR['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgLR['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgLR['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgLR['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgLR['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgLR['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgLR['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgLR['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgLR['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgLR['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgLR['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgLR['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgLR['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgLR['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgLR['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgLR['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgLR['log_loss'])[j]))
      McLR.push((sumLR/divide)*100)
      }
      var McLDA = []
      const performanceAlgLDA = JSON.parse(this.PerformanceAllModels[51])
      for (let j = 0; j < Object.values(performanceAlgLDA['mean_test_accuracy']).length; j++) {
        let sumLDA
        sumLDA = (factorsLocal[0] * Object.values(performanceAlgLDA['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgLDA['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgLDA['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgLDA['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgLDA['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgLDA['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgLDA['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgLDA['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgLDA['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgLDA['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgLDA['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgLDA['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgLDA['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgLDA['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgLDA['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgLDA['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgLDA['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgLDA['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgLDA['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgLDA['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgLDA['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgLDA['log_loss'])[j]))
        McLDA.push((sumLDA/divide)*100)
      }
      var McQDA = []
      const performanceAlgQDA = JSON.parse(this.PerformanceAllModels[60])
      for (let j = 0; j < Object.values(performanceAlgQDA['mean_test_accuracy']).length; j++) {
        let sumQDA
        sumQDA = (factorsLocal[0] * Object.values(performanceAlgQDA['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgQDA['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgQDA['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgQDA['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgQDA['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgQDA['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgQDA['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgQDA['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgQDA['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgQDA['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgQDA['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgQDA['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgQDA['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgQDA['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgQDA['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgQDA['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgQDA['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgQDA['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgQDA['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgQDA['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgQDA['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgQDA['log_loss'])[j]))
        McQDA.push((sumQDA/divide)*100)
      }
      var McRF = []
      const performanceAlgRF = JSON.parse(this.PerformanceAllModels[69])
      for (let j = 0; j < Object.values(performanceAlgRF['mean_test_accuracy']).length; j++) {
        let sumRF
        sumRF = (factorsLocal[0] * Object.values(performanceAlgRF['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgRF['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgRF['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgRF['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgRF['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgRF['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgRF['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgRF['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgRF['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgRF['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgRF['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgRF['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgRF['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgRF['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgRF['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgRF['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgRF['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgRF['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgRF['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgRF['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgRF['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgRF['log_loss'])[j]))
        McRF.push((sumRF/divide)*100)
      }
      var McExtraT = []
      const performanceAlgExtraT = JSON.parse(this.PerformanceAllModels[78])
      for (let j = 0; j < Object.values(performanceAlgExtraT['mean_test_accuracy']).length; j++) {
        let sumExtraT
        sumExtraT = (factorsLocal[0] * Object.values(performanceAlgExtraT['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgExtraT['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgExtraT['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgExtraT['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgExtraT['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgExtraT['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgExtraT['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgExtraT['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgExtraT['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgExtraT['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgExtraT['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgExtraT['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgExtraT['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgExtraT['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgExtraT['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgExtraT['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgExtraT['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgExtraT['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgExtraT['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgExtraT['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgExtraT['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgExtraT['log_loss'])[j]))
        McExtraT.push((sumExtraT/divide)*100)
      }
      var McAdaB = []
      const performanceAlgAdaB = JSON.parse(this.PerformanceAllModels[87])
      for (let j = 0; j < Object.values(performanceAlgAdaB['mean_test_accuracy']).length; j++) {
        let sumAdaB
        sumAdaB = (factorsLocal[0] * Object.values(performanceAlgAdaB['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgAdaB['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgAdaB['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgAdaB['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgAdaB['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgAdaB['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgAdaB['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgAdaB['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgAdaB['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgAdaB['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgAdaB['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgAdaB['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgAdaB['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgAdaB['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgAdaB['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgAdaB['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgAdaB['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgAdaB['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgAdaB['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgAdaB['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgAdaB['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgAdaB['log_loss'])[j]))
        if (sumAdaB <= 0) {
          sumAdaB = 0
        }
        McAdaB.push((sumAdaB/divide)*100)
      }
      var McGradB = []
      const performanceAlgGradB = JSON.parse(this.PerformanceAllModels[96])
      for (let j = 0; j < Object.values(performanceAlgGradB['mean_test_accuracy']).length; j++) {
        let sumGradB
        sumGradB = (factorsLocal[0] * Object.values(performanceAlgGradB['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgGradB['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgGradB['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgGradB['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgGradB['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgGradB['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgGradB['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgGradB['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgGradB['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgGradB['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgGradB['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgGradB['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgGradB['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgGradB['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgGradB['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgGradB['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgGradB['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgGradB['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgGradB['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgGradB['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgGradB['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgGradB['log_loss'])[j]))
        McGradB.push((sumGradB/divide)*100)
      }
      
      // retrieve the results like performance
      const PerformAlgorKNN = JSON.parse(this.PerformanceAllModels[1])
      const PerformAlgorSVC = JSON.parse(this.PerformanceAllModels[10])
      const PerformAlgorGausNB = JSON.parse(this.PerformanceAllModels[19])
      const PerformAlgorMLP = JSON.parse(this.PerformanceAllModels[28])
      const PerformAlgorLR = JSON.parse(this.PerformanceAllModels[37])
      const PerformAlgorLDA = JSON.parse(this.PerformanceAllModels[46])
      const PerformAlgorQDA = JSON.parse(this.PerformanceAllModels[55])
      const PerformAlgorRF = JSON.parse(this.PerformanceAllModels[64])
      const PerformAlgorExtraT = JSON.parse(this.PerformanceAllModels[73])
      const PerformAlgorAdaB = JSON.parse(this.PerformanceAllModels[82])
      const PerformAlgorGradB = JSON.parse(this.PerformanceAllModels[91])

      // initialize/instansiate algorithms and parameters
      this.algorithmKNN = []
      this.algorithmSVC = []
      this.algorithmGausNB = []
      this.algorithmMLP = []
      this.algorithmLR = []
      this.algorithmLDA = []
      this.algorithmQDA = []
      this.algorithmRF = []
      this.algorithmExtraT = []
      this.algorithmAdaB = []
      this.algorithmGradB = []
      this.parameters = []
      if (this.keyAllOrClass) {
        for (var j = 0; j < Object.keys(PerformAlgorKNN['params']).length; j++) {
          this.algorithmKNN.push({'# Performance (%) #': McKNN[j],Algorithm:'KNN',Model:'Model ID: ' + AlgorKNNIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorKNN['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorKNNIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorKNN['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorSVC['params']).length; j++) {
          this.algorithmSVC.push({'# Performance (%) #': McSVC[j],Algorithm:'SVC',Model:'Model ID: ' + AlgorSVCIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorSVC['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorSVCIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorSVC['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorGausNB['params']).length; j++) {
          this.algorithmGausNB.push({'# Performance (%) #': McGausNB[j],Algorithm:'GauNB',Model:'Model ID: ' + AlgorGausNBIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorGausNB['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorGausNBIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorGausNB['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorMLP['params']).length; j++) {
          this.algorithmMLP.push({'# Performance (%) #': McMLP[j],Algorithm:'MLP',Model:'Model ID: ' + AlgorMLPIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorMLP['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorMLPIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorMLP['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorLR['params']).length; j++) {
          this.algorithmLR.push({'# Performance (%) #': McLR[j],Algorithm:'LR',Model:'Model ID: ' + AlgorLRIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorLR['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorLRIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorLR['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorLDA['params']).length; j++) {
          this.algorithmLDA.push({'# Performance (%) #': McLDA[j],Algorithm:'LDA',Model:'Model ID: ' + AlgorLDAIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorLDA['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorLDAIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorLDA['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorQDA['params']).length; j++) {
          this.algorithmQDA.push({'# Performance (%) #': McQDA[j],Algorithm:'QDA',Model:'Model ID: ' + AlgorQDAIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorQDA['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorQDAIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorQDA['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorRF['params']).length; j++) {
          this.algorithmRF.push({'# Performance (%) #': McRF[j],Algorithm:'RF',Model:'Model ID: ' + AlgorRFIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorRF['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorRFIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorRF['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorExtraT['params']).length; j++) {
          this.algorithmExtraT.push({'# Performance (%) #': McExtraT[j],Algorithm:'ExtraT',Model:'Model ID: ' + AlgorExtraTIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorExtraT['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorExtraTIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorExtraT['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorAdaB['params']).length; j++) {
          this.algorithmAdaB.push({'# Performance (%) #': McAdaB[j],Algorithm:'AdaB',Model:'Model ID: ' + AlgorAdaBIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorAdaB['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorAdaBIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorAdaB['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorGradB['params']).length; j++) {
          this.algorithmGradB.push({'# Performance (%) #': McGradB[j],Algorithm:'GradB',Model:'Model ID: ' + AlgorGradBIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorGradB['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorGradBIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorGradB['params'])[j]))
        }
       } else {
        for (var j = 0; j < Object.keys(PerformAlgorKNN['params']).length; j++) {
          this.algorithmKNN.push({'# Performance (%) #': this.listClassPerf[0][j],Algorithm:'KNN',Model:'Model ID: ' + AlgorKNNIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorKNN['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorKNNIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorKNN['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorSVC['params']).length; j++) {
          this.algorithmSVC.push({'# Performance (%) #': this.listClassPerf[1][j],Algorithm:'SVC',Model:'Model ID: ' + AlgorSVCIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorSVC['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorSVCIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorSVC['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorGausNB['params']).length; j++) {
          this.algorithmGausNB.push({'# Performance (%) #': this.listClassPerf[2][j],Algorithm:'GauNB',Model:'Model ID: ' + AlgorGausNBIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorGausNB['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorGausNBIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorGausNB['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorMLP['params']).length; j++) {
          this.algorithmMLP.push({'# Performance (%) #': this.listClassPerf[3][j],Algorithm:'MLP',Model:'Model ID: ' + AlgorMLPIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorMLP['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorMLPIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorMLP['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorLR['params']).length; j++) {
          this.algorithmLR.push({'# Performance (%) #': this.listClassPerf[4][j],Algorithm:'LR',Model:'Model ID: ' + AlgorLRIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorLR['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorLRIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorLR['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorLDA['params']).length; j++) {
          this.algorithmLDA.push({'# Performance (%) #': this.listClassPerf[5][j],Algorithm:'LDA',Model:'Model ID: ' + AlgorLDAIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorLDA['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorLDAIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorLDA['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorQDA['params']).length; j++) {
          this.algorithmQDA.push({'# Performance (%) #': this.listClassPerf[6][j],Algorithm:'QDA',Model:'Model ID: ' + AlgorQDAIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorQDA['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorQDAIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorQDA['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorRF['params']).length; j++) {
          this.algorithmRF.push({'# Performance (%) #': this.listClassPerf[7][j],Algorithm:'RF',Model:'Model ID: ' + AlgorRFIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorRF['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorRFIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorRF['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorExtraT['params']).length; j++) {
          this.algorithmExtraT.push({'# Performance (%) #': this.listClassPerf[8][j],Algorithm:'ExtraT',Model:'Model ID: ' + AlgorExtraTIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorExtraT['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorExtraTIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorExtraT['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorAdaB['params']).length; j++) {
          this.algorithmAdaB.push({'# Performance (%) #': this.listClassPerf[9][j],Algorithm:'AdaB',Model:'Model ID: ' + AlgorAdaBIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorAdaB['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorAdaBIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorAdaB['params'])[j]))
        }
        for (let j = 0; j < Object.keys(PerformAlgorGradB['params']).length; j++) {
          this.algorithmGradB.push({'# Performance (%) #': this.listClassPerf[10][j],Algorithm:'GradB',Model:'Model ID: ' + AlgorGradBIDs[j] + '<br> Parameters: '+JSON.stringify(Object.values(PerformAlgorGradB['params'])[j])+'<br> # Performance (%) #',ModelID:AlgorGradBIDs[j]})
          this.parameters.push(JSON.stringify(Object.values(PerformAlgorGradB['params'])[j]))
        }
      }
      EventBus.$emit('ParametersAll', this.parameters)

      // concat the data
      var data = this.algorithmKNN
      var data = this.algorithmKNN.concat(this.algorithmSVC)
      var data = data.concat(this.algorithmGausNB)
      var data = data.concat(this.algorithmMLP)
      var data = data.concat(this.algorithmLR)
      var data = data.concat(this.algorithmLDA)
      var data = data.concat(this.algorithmQDA)
      var data = data.concat(this.algorithmRF)
      var data = data.concat(this.algorithmExtraT)
      var data = data.concat(this.algorithmAdaB)
      var data = data.concat(this.algorithmGradB)
      // aesthetic :
      // y : point's value on y axis
      // group : how to group data on x axis
      // color : color of the point / boxplot
      // label : displayed text in toolbox
      this.chart = exploding_boxplot(data, {y:'# Performance (%) #',group:'Algorithm',color:'Algorithm',label:'Model'})
      this.chart.width(this.WH[0]*10.225) // interactive visualization
      this.chart.height(this.WH[1]*0.95) // interactive visualization
      //call chart on a div
      this.chart('#exploding_boxplot')       

      // colorscale
      const previousColor = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#b15928']
      // check for brushing
      var el = document.getElementsByClassName('d3-exploding-boxplot boxcontent')
      var overall = document.getElementsByClassName('overall')
      this.brushStatus = document.getElementsByClassName('extent')
      // on clicks
      
      var flagEmptyKNN = 0
      var flagEmptySVC = 0
      var flagEmptyGausNB = 0
      var flagEmptyMLP = 0
      var flagEmptyLR = 0
      var flagEmptyLDA = 0
      var flagEmptyQDA = 0
      var flagEmptyRF = 0
      var flagEmptyExtraT = 0
      var flagEmptyAdaB = 0
      var flagEmptyGradB = 0

      el[0].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point KNN')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[0]
          allPoints[i].style.opacity = '1.0'
        } 

        if (flagEmptyKNN == 0) {
          flagEmptyKNN = 1
        } else {
          flagEmptyKNN = 0
        } 

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagKNN', flagEmptyKNN)
        if (flagEmptyKNN == 1) {
          EventBus.$emit('PCPCall', 'KNN')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[1].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point SVC')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[1]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptySVC == 0) {
          flagEmptySVC = 1
        } else {
          flagEmptySVC = 0
        }

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagSVC', flagEmptySVC)
        if (flagEmptySVC == 1) {
          EventBus.$emit('PCPCall', 'SVC')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[2].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point GauNB')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[2]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyGausNB == 0) {
          flagEmptyGausNB = 1
        } else {
          flagEmptyGausNB = 0
        }

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagGauNB', flagEmptyGausNB)
        if (flagEmptyGausNB == 1) {
          EventBus.$emit('PCPCall', 'GauNB')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[3].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point MLP')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[3]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyMLP == 0) {
          flagEmptyMLP = 1
        } else {
          flagEmptyMLP = 0
        }
        
        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagMLP', flagEmptyMLP)
        if (flagEmptyMLP == 1) {
          EventBus.$emit('PCPCall', 'MLP')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[4].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point LR')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[4]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyLR == 0) {
          flagEmptyLR = 1
        } else {
          flagEmptyLR = 0
        }

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagLR', flagEmptyLR)
        if (flagEmptyLR == 1) {
          EventBus.$emit('PCPCall', 'LR')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[5].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point LDA')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[5]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyLDA == 0) {
          flagEmptyLDA = 1
        } else {
          flagEmptyLDA = 0
        }

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagLDA', flagEmptyLDA)
        if (flagEmptyLDA == 1) {
          EventBus.$emit('PCPCall', 'LDA')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[6].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point QDA')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[6]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyQDA == 0) {
          flagEmptyQDA = 1
        } else {
          flagEmptyQDA = 0
        }
      
        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagQDA', flagEmptyQDA)
        if (flagEmptyQDA == 1) {
          EventBus.$emit('PCPCall', 'QDA')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[7].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point RF')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[7]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyRF == 0) {
          flagEmptyRF = 1
        } else {
          flagEmptyRF = 0
        }
      
        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagRF', flagEmptyRF)
        if (flagEmptyRF == 1) {
          EventBus.$emit('PCPCall', 'RF')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[8].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point ExtraT')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[8]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyExtraT == 0) {
          flagEmptyExtraT = 1
        } else {
          flagEmptyExtraT = 0
        }

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagExtraT', flagEmptyExtraT)
        if (flagEmptyExtraT == 1) {
          EventBus.$emit('PCPCall', 'ExtraT')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[9].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point AdaB')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[9]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyAdaB == 0) {
          flagEmptyAdaB = 1
        } else {
          flagEmptyAdaB = 0
        }

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagAdaB', flagEmptyAdaB)
        if (flagEmptyAdaB == 1) {
          EventBus.$emit('PCPCall', 'AdaB')
        }
        EventBus.$emit('updateBarChart', [])
      }
      el[10].onclick = function() {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point GradB')
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.fill = previousColor[10]
          allPoints[i].style.opacity = '1.0'
        }

         if (flagEmptyGradB == 0) {
          flagEmptyGradB = 1
        } else {
          flagEmptyGradB = 0
        }

        EventBus.$emit('clearPCP')
        EventBus.$emit('updateFlagGradB', flagEmptyGradB)
        if (flagEmptyGradB == 1) {
          EventBus.$emit('PCPCall', 'GradB')
        }
        EventBus.$emit('updateBarChart', [])
      }

      overall[0].ondblclick = function () {
        flagEmptyKNN = 0
        flagEmptySVC = 0
        flagEmptyGausNB = 0
        flagEmptyMLP = 0
        flagEmptyLR = 0
        flagEmptyLDA = 0
        flagEmptyQDA = 0
        flagEmptyRF = 0
        flagEmptyExtraT = 0
        flagEmptyAdaB = 0
        flagEmptyGradB = 0
        EventBus.$emit('clearPCP')
        EventBus.$emit('alternateFlagLock')
        EventBus.$emit('updateBarChart', [])
      }
      const myObserver = new ResizeObserver(entries => {
        if (this.activeTabVal) {
          (EventBus.$emit('brusheAllOn'))
        }
      })
      var brushRect = document.querySelector('.extent')
      myObserver.observe(brushRect);
    },
    brushActivationAll () {
      // continue here and select the correct points.
      var limiter = this.chart.returnBrush()

      var algorithm = []
      const previousColor = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#b15928']
      var modelsActive = []
      for (var j = 0; j < this.AllAlgorithms.length; j++) {
        algorithm = []
        if (this.AllAlgorithms[j] === 'KNN') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point KNN')
          algorithm = this.algorithmKNN
        } else if (this.AllAlgorithms[j] === 'SVC') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point SVC')
          algorithm = this.algorithmSVC
        } else if (this.AllAlgorithms[j] === 'GauNB') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point GauNB')
          algorithm = this.algorithmGausNB
        } else if (this.AllAlgorithms[j] === 'MLP') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point MLP')
          algorithm = this.algorithmMLP
        } else if (this.AllAlgorithms[j] === 'LR') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point LR')
          algorithm = this.algorithmLR
        } else if (this.AllAlgorithms[j] === 'LDA') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point LDA')
          algorithm = this.algorithmLDA
        } else if (this.AllAlgorithms[j] === 'QDA') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point QDA')
          algorithm = this.algorithmQDA
        } else if (this.AllAlgorithms[j] === 'RF') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point RF')
          algorithm = this.algorithmRF
        } else if (this.AllAlgorithms[j] === 'ExtraT') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point ExtraT')
          algorithm = this.algorithmExtraT
        } else if (this.AllAlgorithms[j] === 'AdaB') {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point AdaB')
          algorithm = this.algorithmAdaB
        } else {
          var allPoints = document.getElementsByClassName('d3-exploding-boxplot point GradB')
          algorithm = this.algorithmGradB
        }
        for (let k = 0; k < allPoints.length; k++) {
          if (algorithm[k]['# Performance (%) #'] < limiter[0] && algorithm[k]['# Performance (%) #'] > limiter[1]) {
            modelsActive.push(algorithm[k].ModelID)
          }
        }
        for (let i = 0; i < allPoints.length; i++) {
          if (this.AllAlgorithms[j] === 'KNN') {
            allPoints[i].style.fill = previousColor[0]
          } else if (this.AllAlgorithms[j] === 'SVC') {
            allPoints[i].style.fill = previousColor[1]
          } else if (this.AllAlgorithms[j] === 'GauNB') {
            allPoints[i].style.fill = previousColor[2]
          } else if (this.AllAlgorithms[j] === 'MLP') {
            allPoints[i].style.fill = previousColor[3]
          } else if (this.AllAlgorithms[j] === 'LR') {
            allPoints[i].style.fill = previousColor[4]
          } else if (this.AllAlgorithms[j] === 'LDA') {
            allPoints[i].style.fill = previousColor[5]
          } else if (this.AllAlgorithms[j] === 'QDA') {
            allPoints[i].style.fill = previousColor[6]
          } else if (this.AllAlgorithms[j] === 'RF') {
            allPoints[i].style.fill = previousColor[7]
          } else if (this.AllAlgorithms[j] === 'ExtraT') {
            allPoints[i].style.fill = previousColor[8]
          } else if (this.AllAlgorithms[j] === 'AdaB') {
            allPoints[i].style.fill = previousColor[9]
          } else {
            allPoints[i].style.fill = previousColor[10]
          }
        }
        if (modelsActive.length == 0) {
          for (let i = 0; i < allPoints.length; i++) {
            //if (modelsActive.indexOf(i) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '1.0'
            //}
          }
        } else if (modelsActive.length == allPoints.length) {
          for (let i = 0; i < allPoints.length; i++) {
            if (this.AllAlgorithms[j] === 'KNN') {
              allPoints[i].style.fill = previousColor[0]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'SVC') {
              allPoints[i].style.fill = previousColor[1]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'GauNB') {
              allPoints[i].style.fill = previousColor[2]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'MLP') {
              allPoints[i].style.fill = previousColor[3]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'LR') {
              allPoints[i].style.fill = previousColor[4]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'LDA') {
              allPoints[i].style.fill = previousColor[5]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'QDA') {
              allPoints[i].style.fill = previousColor[6]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'RF') {
              allPoints[i].style.fill = previousColor[7]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'ExtraT') {
              allPoints[i].style.fill = previousColor[8]
              allPoints[i].style.opacity = '1.0'
            } else if (this.AllAlgorithms[j] === 'AdaB') {
              allPoints[i].style.fill = previousColor[9]
              allPoints[i].style.opacity = '1.0'
            } else {
              allPoints[i].style.fill = previousColor[10]
              allPoints[i].style.opacity = '1.0'
            }
          }
        } else {
          for (let i = 0; i < allPoints.length; i++) {
            allPoints[i].style.opacity = '1.0'
            if (this.AllAlgorithms[j] === 'KNN') {
              if (modelsActive.indexOf(i) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'SVC') {
              if (modelsActive.indexOf(i+this.SVCModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'GauNB') {
              if (modelsActive.indexOf(i+this.GausNBModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'MLP') {
              if (modelsActive.indexOf(i+this.MLPModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'LR') {
              if (modelsActive.indexOf(i+this.LRModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'LDA') {
              if (modelsActive.indexOf(i+this.LDAModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'QDA') {
              if (modelsActive.indexOf(i+this.QDAModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'RF') {
              if (modelsActive.indexOf(i+this.RFModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'ExtraT') {
              if (modelsActive.indexOf(i+this.ExtraTModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else if (this.AllAlgorithms[j] === 'AdaB') {
              if (modelsActive.indexOf(i+this.AdaBModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            } else {
              if (modelsActive.indexOf(i+this.GradBModels) == -1) {
                allPoints[i].style.fill = "#d3d3d3"
                allPoints[i].style.opacity = '0.4'
              }
            }
          }
        }
      }
      EventBus.$emit('flagBrushedAll', 1)
      EventBus.$emit('sendParameters', this.parameters)
      EventBus.$emit('updateActiveModels', modelsActive)
      this.UpdateBarChart()
    },
    brushed () {
      if (this.selectedAlgorithm === 'KNN') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point KNN')
      } else if (this.selectedAlgorithm === 'SVC') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point SVC')
      } else if (this.selectedAlgorithm === 'GauNB') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point GauNB')
      } else if (this.selectedAlgorithm === 'MLP') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point MLP')
      } else if (this.selectedAlgorithm === 'LR') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point LR')
      } else if (this.selectedAlgorithm === 'LDA') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point LDA')
      } else if (this.selectedAlgorithm === 'QDA') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point QDA')
      } else if (this.selectedAlgorithm === 'RF') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point RF')
      } else if (this.selectedAlgorithm === 'ExtraT') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point ExtraT')
      } else if (this.selectedAlgorithm === 'AdaB') {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point AdaB')
      } else {
        var allPoints = document.getElementsByClassName('d3-exploding-boxplot point GradB')
      }
      const previousColor = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#b15928']
      var modelsActive = []
      for (let j = 0; j < this.brushedBoxPl.length; j++) {
        modelsActive.push(this.brushedBoxPl[j].model)
      }
      for (let i = 0; i < allPoints.length; i++) {
        if (this.selectedAlgorithm === 'KNN') {
          allPoints[i].style.fill = previousColor[0]
        } else if (this.selectedAlgorithm === 'SVC') {
          allPoints[i].style.fill = previousColor[1]
        } else if (this.selectedAlgorithm === 'GauNB') {
          allPoints[i].style.fill = previousColor[2]
        } else if (this.selectedAlgorithm === 'MLP') {
          allPoints[i].style.fill = previousColor[3]
        } else if (this.selectedAlgorithm === 'LR') {
          allPoints[i].style.fill = previousColor[4]
        } else if (this.selectedAlgorithm === 'LDA') {
          allPoints[i].style.fill = previousColor[5]
        } else if (this.selectedAlgorithm === 'QDA') {
          allPoints[i].style.fill = previousColor[6]
        } else if (this.selectedAlgorithm === 'RF') {
          allPoints[i].style.fill = previousColor[7]
        } else if (this.selectedAlgorithm === 'ExtraT') {
          allPoints[i].style.fill = previousColor[8]
        } else if (this.selectedAlgorithm === 'AdaB') {
          allPoints[i].style.fill = previousColor[9]
        } else {
          allPoints[i].style.fill = previousColor[10]
        }
      }
      if (modelsActive.length == 0) {
        for (let i = 0; i < allPoints.length; i++) {
          //if (modelsActive.indexOf(i) == -1) {
            allPoints[i].style.fill = "#d3d3d3"
            allPoints[i].style.opacity = '1.0'
          //}
        }
      } else if (modelsActive.length == allPoints.length) {
        for (let i = 0; i < allPoints.length; i++) {
          if (this.selectedAlgorithm === 'KNN') {
            allPoints[i].style.fill = previousColor[0]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'SVC') {
            allPoints[i].style.fill = previousColor[1]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'GauNB') {
            allPoints[i].style.fill = previousColor[2]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'MLP') {
            allPoints[i].style.fill = previousColor[3]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'LR') {
            allPoints[i].style.fill = previousColor[4]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'LDA') {
            allPoints[i].style.fill = previousColor[5]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'QDA') {
            allPoints[i].style.fill = previousColor[6]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'RF') {
            allPoints[i].style.fill = previousColor[7]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'ExtraT') {
            allPoints[i].style.fill = previousColor[8]
            allPoints[i].style.opacity = '1.0'
          } else if (this.selectedAlgorithm === 'AdaB') {
            allPoints[i].style.fill = previousColor[9]
            allPoints[i].style.opacity = '1.0'
          } else {
            allPoints[i].style.fill = previousColor[10]
            allPoints[i].style.opacity = '1.0'
          }
        }
      } else {
        for (let i = 0; i < allPoints.length; i++) {
          allPoints[i].style.opacity = '1.0'
          if (this.selectedAlgorithm === 'KNN') {
            if (modelsActive.indexOf(i) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'SVC') {
            if (modelsActive.indexOf(i+this.SVCModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'GauNB') {
            if (modelsActive.indexOf(i+this.GausNBModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'MLP') {
            if (modelsActive.indexOf(i+this.MLPModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'LR') {
            if (modelsActive.indexOf(i+this.LRModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'LDA') {
            if (modelsActive.indexOf(i+this.LDAModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'QDA') {
            if (modelsActive.indexOf(i+this.QDAModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'RF') {
            if (modelsActive.indexOf(i+this.RFModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'ExtraT') {
            if (modelsActive.indexOf(i+this.ExtraTModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else if (this.selectedAlgorithm === 'AdaB') {
            if (modelsActive.indexOf(i+this.AdaBModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          } else {
            if (modelsActive.indexOf(i+this.GradBModels) == -1) {
              allPoints[i].style.fill = "#d3d3d3"
              allPoints[i].style.opacity = '0.4'
            }
          }
        }
      }
      EventBus.$emit('flagBrushedAll', 0)
      EventBus.$emit('sendParameters', this.parameters)
      EventBus.$emit('updateActiveModels', modelsActive)
      this.UpdateBarChart()
    },
    UpdateBarChart () {
      var allPoints = document.getElementsByClassName('d3-exploding-boxplot point')
      var activeModels = []
      var algorithmsSelected = []
      var modelsSelected =[]
      for (let i = 0; i < allPoints.length; i++) {
        if (allPoints[i].style.fill != "rgb(211, 211, 211)") {
          activeModels.push(allPoints[i].__data__.Model)
          if (allPoints[i].__data__.Algorithm === 'KNN') {
            algorithmsSelected.push('KNN')
          } else if (allPoints[i].__data__.Algorithm === 'SVC') {
            algorithmsSelected.push('SVC')
          } else if (allPoints[i].__data__.Algorithm === 'GauNB') {
            algorithmsSelected.push('GauNB')
          } else if (allPoints[i].__data__.Algorithm === 'MLP') {
            algorithmsSelected.push('MLP')
          } else if (allPoints[i].__data__.Algorithm === 'LR') {
            algorithmsSelected.push('LR')
          } else if (allPoints[i].__data__.Algorithm === 'LDA') {
            algorithmsSelected.push('LDA')
          } else if (allPoints[i].__data__.Algorithm === 'QDA') {
            algorithmsSelected.push('QDA')
          } else if (allPoints[i].__data__.Algorithm === 'RF') {
            algorithmsSelected.push('RF')
          } else if (allPoints[i].__data__.Algorithm === 'ExtraT') {
            algorithmsSelected.push('ExtraT')
          } else if (allPoints[i].__data__.Algorithm === 'AdaB') {
            algorithmsSelected.push('AdaB')
          } else {
            algorithmsSelected.push('GradB')
          }
        }
      }
      if (activeModels.length == 0){
      } else {
        for (let i = 0; i<activeModels.length; i++) {
          var array = activeModels[i].split(' ')
          var temp = array[2].split('<br>')
          modelsSelected.push(temp[0])
        }
      }
      EventBus.$emit('updateBarChartAlgorithm', algorithmsSelected)
      EventBus.$emit('updateBarChart', modelsSelected)
    },
    selectedPointsPerAlgorithm () {
      var allPoints = document.getElementsByClassName('d3-exploding-boxplot point')
      var activeModels = []
      var algorithmsSelected = []
      var models = []
      for (let i = 0; i < allPoints.length; i++) {
        if (allPoints[i].style.fill != "rgb(211, 211, 211)") {
          activeModels.push(allPoints[i].__data__.Model)
          if (allPoints[i].__data__.Algorithm === 'KNN') {
            algorithmsSelected.push('KNN')
          } else if (allPoints[i].__data__.Algorithm === 'SVC') {
            algorithmsSelected.push('SVC')
          } else if (allPoints[i].__data__.Algorithm === 'GauNB') {
            algorithmsSelected.push('GauNB')
          } else if (allPoints[i].__data__.Algorithm === 'MLP') {
            algorithmsSelected.push('MLP')
          } else if (allPoints[i].__data__.Algorithm === 'LR') {
            algorithmsSelected.push('LR')
          } else if (allPoints[i].__data__.Algorithm === 'LDA') {
            algorithmsSelected.push('LDA')
          } else if (allPoints[i].__data__.Algorithm === 'QDA') {
            algorithmsSelected.push('QDA')
          } else if (allPoints[i].__data__.Algorithm === 'RF') {
            algorithmsSelected.push('RF')
          } else if (allPoints[i].__data__.Algorithm === 'ExtraT') {
            algorithmsSelected.push('ExtraT')
          } else if (allPoints[i].__data__.Algorithm === 'AdaB') {
            algorithmsSelected.push('AdaB')
          } else {
            algorithmsSelected.push('GradB')
          }
        }
      }
      if (activeModels.length == 0){
        alert('No models selected, please, retry!')
      } else {
        for (let i = 0; i<activeModels.length; i++) {
          var array = activeModels[i].split(' ')
          var temp = array[2].split('<br>')
          models.push(temp[0]) 
        }
        EventBus.$emit('ReturningAlgorithms', algorithmsSelected)
        EventBus.$emit('ReturningBrushedPointsIDs', models)
      }
    },
    previousBoxPlotState () {
      var el = document.getElementsByClassName('d3-exploding-boxplot box')
      if (document.getElementById('PCP').style.display == 'none') {
        
      } else {
        if (this.selectedAlgorithm == 'KNN') {
          $(el)[0].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'SVC') {
          $(el)[1].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'GauNB') {
          $(el)[2].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'MLP') {
          $(el)[3].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'LR') {
          $(el)[4].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'LDA') {
          $(el)[5].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'QDA') {
          $(el)[6].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'RF') {
          $(el)[7].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'ExtraT') {
          $(el)[8].dispatchEvent(new Event('click'))
        } else if (this.selectedAlgorithm == 'AdaB') {
          $(el)[9].dispatchEvent(new Event('click'))
        } else {
          $(el)[10].dispatchEvent(new Event('click'))
        }
      }
    },
  },
  mounted () {
    EventBus.$on('Algorithm', data => { this.activeTabVal = data })

    EventBus.$on('emittedEventCallingModelBrushed', this.selectedPointsPerAlgorithm)
    EventBus.$on('emittedEventCallingAllAlgorithms', data => {
      this.PerformanceAllModels = data})
    EventBus.$on('emittedEventCallingAllAlgorithms', this.boxplot)
    EventBus.$on('emittedEventCallingBrushedBoxPlot', data => {
      this.brushedBoxPl = data})
    EventBus.$on('emittedEventCallingBrushedBoxPlot', this.brushed),
    EventBus.$on('Responsive', data => {
      this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
      this.WH = data})
    EventBus.$on('ResponsiveandChange', this.boxplot)
    EventBus.$on('ResponsiveandChange', this.previousBoxPlotState)
    EventBus.$on('emittedEventCallingSelectedALgorithm', data => {
      this.selectedAlgorithm = data})
    EventBus.$on('brusheAllOn', this.brushActivationAll)

    EventBus.$on('CallFactorsView', data => { this.factors = data })
    EventBus.$on('CallFactorsView', this.boxplot)

    EventBus.$on('boxplotSet', data => { this.listClassPerf = data })
    EventBus.$on('boxplotCall', data => { this.keyAllOrClass = data })
    EventBus.$on('boxplotCall', this.boxplot)

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }
}
</script>