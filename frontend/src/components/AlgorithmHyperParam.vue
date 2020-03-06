<template>
  <div id="PCP" class="parcoords" style="min-height: 285px;"></div>
</template>

<script>
import 'parcoord-es/dist/parcoords.css';
import ParCoords from 'parcoord-es';
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

import { EventBus } from '../main.js'

export default {
  name: 'AlgorithmHyperParam',
  data () {
    return {
      ModelsPerformance: 0,
      selAlgorithm: 0,
      keyAllOrClass: true,
      listClassPerf: [],
      pc: 0,
      factors: [1,0,0
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
    }
  },
  methods: {
    reset () {
      d3.selectAll("#PCP > *").remove(); 
    },
    PCPView () {
      d3.selectAll("#PCP > *").remove(); 
      if (this.selAlgorithm != '') {
        var colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#b15928']
        var colorGiv = 0
        
        var factorsLocal = this.factors
        var divide = 0

        factorsLocal.forEach(element => {
          divide = element + divide
        });

        var McKNN = []
        const performanceAlgKNN = JSON.parse(this.ModelsPerformance[6])
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
        const performanceAlgSVC = JSON.parse(this.ModelsPerformance[15])
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
        const performanceAlgGausNB = JSON.parse(this.ModelsPerformance[24])
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
        const performanceAlgMLP = JSON.parse(this.ModelsPerformance[33])
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
        const performanceAlgLR = JSON.parse(this.ModelsPerformance[42])
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
        const performanceAlgLDA = JSON.parse(this.ModelsPerformance[51])
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
        const performanceAlgQDA = JSON.parse(this.ModelsPerformance[60])
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
        const performanceAlgRF = JSON.parse(this.ModelsPerformance[69])
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
        const performanceAlgExtraT = JSON.parse(this.ModelsPerformance[78])
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
        const performanceAlgAdaB = JSON.parse(this.ModelsPerformance[87])
        for (let j = 0; j < Object.values(performanceAlgAdaB['mean_test_accuracy']).length; j++) {
        let sumAdaB
        sumAdaB = (factorsLocal[0] * Object.values(performanceAlgAdaB['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgAdaB['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgAdaB['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgAdaB['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgAdaB['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgAdaB['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgAdaB['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgAdaB['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgAdaB['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgAdaB['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgAdaB['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgAdaB['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgAdaB['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgAdaB['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgAdaB['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgAdaB['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgAdaB['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgAdaB['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgAdaB['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgAdaB['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgAdaB['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgAdaB['log_loss'])[j]))
          McAdaB.push((sumAdaB/divide)*100)
        }
        var McGradB = []
        const performanceAlgGradB = JSON.parse(this.ModelsPerformance[96])
        for (let j = 0; j < Object.values(performanceAlgGradB['mean_test_accuracy']).length; j++) {
          let sumGradB
        sumGradB = (factorsLocal[0] * Object.values(performanceAlgGradB['mean_test_accuracy'])[j]) + (factorsLocal[1] * Object.values(performanceAlgGradB['geometric_mean_score_micro'])[j]) + (factorsLocal[2] * Object.values(performanceAlgGradB['geometric_mean_score_macro'])[j])
          + (factorsLocal[3] * Object.values(performanceAlgGradB['geometric_mean_score_weighted'])[j]) + (factorsLocal[4] * Object.values(performanceAlgGradB['mean_test_precision_micro'])[j]) + (factorsLocal[5] * Object.values(performanceAlgGradB['mean_test_precision_macro'])[j]) + (factorsLocal[6] * Object.values(performanceAlgGradB['mean_test_precision_weighted'])[j]) + (factorsLocal[7] * Object.values(performanceAlgGradB['mean_test_recall_micro'])[j])
          + (factorsLocal[8] * Object.values(performanceAlgGradB['mean_test_recall_macro'])[j]) + (factorsLocal[9] * Object.values(performanceAlgGradB['mean_test_recall_weighted'])[j]) + (factorsLocal[10] * Object.values(performanceAlgGradB['f5_micro'])[j]) + (factorsLocal[11] * Object.values(performanceAlgGradB['f5_macro'])[j]) + (factorsLocal[12] * Object.values(performanceAlgGradB['f5_weighted'])[j]) + (factorsLocal[13] * Object.values(performanceAlgGradB['f1_micro'])[j])
          + (factorsLocal[14] * Object.values(performanceAlgGradB['f1_macro'])[j]) + (factorsLocal[15] * Object.values(performanceAlgGradB['f1_weighted'])[j]) + (factorsLocal[16] * Object.values(performanceAlgGradB['f2_micro'])[j]) + (factorsLocal[17] * Object.values(performanceAlgGradB['f2_macro'])[j]) + (factorsLocal[18] * Object.values(performanceAlgGradB['f2_weighted'])[j]) + (factorsLocal[19] * Math.abs(Object.values(performanceAlgGradB['matthews_corrcoef'])[j]))
          + (factorsLocal[20] * Object.values(performanceAlgGradB['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[21] * (1 - Object.values(performanceAlgGradB['log_loss'])[j]))
          McGradB.push((sumGradB/divide)*100)
        }

        var Combined = 0
        if (this.selAlgorithm == 'KNN') {    
          Combined = JSON.parse(this.ModelsPerformance[1])
          colorGiv = colors[0]
        } else if (this.selAlgorithm == 'SVC') {    
          Combined = JSON.parse(this.ModelsPerformance[10])
          colorGiv = colors[1]
        } else if (this.selAlgorithm == 'GauNB') {    
          Combined = JSON.parse(this.ModelsPerformance[19])
          colorGiv = colors[2]
        } else if (this.selAlgorithm == 'MLP') {    
          Combined = JSON.parse(this.ModelsPerformance[28])
          colorGiv = colors[3]
        } else if (this.selAlgorithm == 'LR') {    
          Combined = JSON.parse(this.ModelsPerformance[37])
          colorGiv = colors[4]
        } else if (this.selAlgorithm == 'LDA') {    
          Combined = JSON.parse(this.ModelsPerformance[46])
          colorGiv = colors[5]
        } else if (this.selAlgorithm == 'QDA') {    
          Combined = JSON.parse(this.ModelsPerformance[55])
          colorGiv = colors[6]
        } else if (this.selAlgorithm == 'RF') {    
          Combined = JSON.parse(this.ModelsPerformance[64])
          colorGiv = colors[7]
        } else if (this.selAlgorithm == 'ExtraT') {    
          Combined = JSON.parse(this.ModelsPerformance[73])
          colorGiv = colors[8]
        } else if (this.selAlgorithm == 'AdaB') {    
          Combined = JSON.parse(this.ModelsPerformance[82])
          colorGiv = colors[9]
        } else {
          Combined = JSON.parse(this.ModelsPerformance[91])
          colorGiv = colors[10]
        }
        var valuesPerf = Object.values(Combined['params'])
        
        var ObjectsParams = Combined['params']
        var newObjectsParamsΚΝΝ = []
        var newObjectsParamsSVC = []
        var newObjectsParamsGausNB = []
        var newObjectsParamsMLP = []
        var newObjectsParamsLR = []
        var newObjectsParamsLDA = []
        var newObjectsParamsQDA = []
        var newObjectsParamsRF = []
        var newObjectsParamsExtraT = []
        var newObjectsParamsAdaB = []
        var newObjectsParamsGradB = []
        var ArrayCombined = []
        var temp
        for (var i = 0; i < valuesPerf.length; i++) {
          if (this.keyAllOrClass) {
            if (this.selAlgorithm === 'KNN') {
              newObjectsParamsΚΝΝ.push({model: i,'# Perf (%) #': McKNN[i],'n_neighbors':ObjectsParams[i].n_neighbors,'metric':ObjectsParams[i].metric,'algorithm':ObjectsParams[i].algorithm,'weights':ObjectsParams[i].weights})
              ArrayCombined[i] = newObjectsParamsΚΝΝ[i]
            } else if (this.selAlgorithm === 'SVC') {
              newObjectsParamsSVC.push({model: this.SVCModels + i,'# Perf (%) #': McSVC[i],'C':ObjectsParams[i].C,'kernel':ObjectsParams[i].kernel})
              ArrayCombined[i] = newObjectsParamsSVC[i]
            } else if (this.selAlgorithm === 'GauNB') {
              newObjectsParamsGausNB.push({model: this.GausNBModels + i,'# Perf (%) #': McGausNB[i],'var_smoothing':ObjectsParams[i].var_smoothing})
              ArrayCombined[i] = newObjectsParamsGausNB[i]
            } else if (this.selAlgorithm === 'MLP') {
              newObjectsParamsMLP.push({model: this.MLPModels + i,'# Perf (%) #': McMLP[i],'alpha':ObjectsParams[i].alpha,'tol':ObjectsParams[i].tol,'activation':ObjectsParams[i].activation,'max_iter':ObjectsParams[i].max_iter,'solver':ObjectsParams[i].solver})
              ArrayCombined[i] = newObjectsParamsMLP[i]
            } else if (this.selAlgorithm === 'LR') {
              newObjectsParamsLR.push({model: this.LRModels + i,'# Perf (%) #': McLR[i],'C':ObjectsParams[i].C,'max_iter':ObjectsParams[i].max_iter,'solver':ObjectsParams[i].solver,'penalty':ObjectsParams[i].penalty})
              ArrayCombined[i] = newObjectsParamsLR[i]
            } else if (this.selAlgorithm === 'LDA') {
              newObjectsParamsLDA.push({model: this.LDAModels + i,'# Perf (%) #': McLDA[i],'shrinkage':ObjectsParams[i].shrinkage,'solver':ObjectsParams[i].solver})
              ArrayCombined[i] = newObjectsParamsLDA[i]
            } else if (this.selAlgorithm === 'QDA') {
              newObjectsParamsQDA.push({model: this.QDAModels + i,'# Perf (%) #': McQDA[i],'reg_param':ObjectsParams[i].reg_param,'tol':ObjectsParams[i].tol})
              ArrayCombined[i] = newObjectsParamsQDA[i]
            } else if (this.selAlgorithm === 'RF') {
              newObjectsParamsRF.push({model: this.RFModels + i,'# Perf (%) #': McRF[i],'n_estimators':ObjectsParams[i].n_estimators,'criterion':ObjectsParams[i].criterion})
              ArrayCombined[i] = newObjectsParamsRF[i]
            } else if (this.selAlgorithm === 'ExtraT') {
              newObjectsParamsExtraT.push({model: this.ExtraTModels + i,'# Perf (%) #': McExtraT[i],'n_estimators':ObjectsParams[i].n_estimators,'criterion':ObjectsParams[i].criterion})
              ArrayCombined[i] = newObjectsParamsExtraT[i]
            } else if (this.selAlgorithm === 'AdaB') {
              newObjectsParamsAdaB.push({model: this.AdaBModels + i,'# Perf (%) #': McAdaB[i],'n_estimators':ObjectsParams[i].n_estimators,'learning_rate':ObjectsParams[i].learning_rate,'algorithm':ObjectsParams[i].algorithm})
              ArrayCombined[i] = newObjectsParamsAdaB[i]
            } else {
              newObjectsParamsGradB.push({model: this.GradBModels + i,'# Perf (%) #': McGradB[i],'n_estimators':ObjectsParams[i].n_estimators,'criterion':ObjectsParams[i].criterion,'learning_rate':ObjectsParams[i].learning_rate})
              ArrayCombined[i] = newObjectsParamsGradB[i]
            }
          } else {
            if (this.selAlgorithm === 'KNN') {
              newObjectsParamsΚΝΝ.push({model: i,'# Perf (%) #': this.listClassPerf[0][i],'n_neighbors':ObjectsParams[i].n_neighbors,'metric':ObjectsParams[i].metric,'algorithm':ObjectsParams[i].algorithm,'weights':ObjectsParams[i].weights})
              ArrayCombined[i] = newObjectsParamsΚΝΝ[i]
            } else if (this.selAlgorithm === 'SVC') {
              newObjectsParamsSVC.push({model: this.SVCModels + i,'# Perf (%) #': this.listClassPerf[1][i],'C':ObjectsParams[i].C,'kernel':ObjectsParams[i].kernel})
              ArrayCombined[i] = newObjectsParamsSVC[i]
            } else if (this.selAlgorithm === 'GauNB') {
              newObjectsParamsGausNB.push({model: this.GausNBModels + i,'# Perf (%) #': this.listClassPerf[2][i],'var_smoothing':ObjectsParams[i].var_smoothing})
              ArrayCombined[i] = newObjectsParamsGausNB[i]
            } else if (this.selAlgorithm === 'MLP') {
              newObjectsParamsMLP.push({model: this.MLPModels + i,'# Perf (%) #': this.listClassPerf[3][i],'alpha':ObjectsParams[i].alpha,'tol':ObjectsParams[i].tol,'activation':ObjectsParams[i].activation,'max_iter':ObjectsParams[i].max_iter,'solver':ObjectsParams[i].solver})
              ArrayCombined[i] = newObjectsParamsMLP[i]
            } else if (this.selAlgorithm === 'LR') {
              newObjectsParamsLR.push({model: this.LRModels + i,'# Perf (%) #': this.listClassPerf[4][i],'C':ObjectsParams[i].C,'max_iter':ObjectsParams[i].max_iter,'solver':ObjectsParams[i].solver,'penalty':ObjectsParams[i].penalty})
              ArrayCombined[i] = newObjectsParamsLR[i]
            } else if (this.selAlgorithm === 'LDA') {
              newObjectsParamsLDA.push({model: this.LDAModels + i,'# Perf (%) #': this.listClassPerf[5][i],'shrinkage':ObjectsParams[i].shrinkage,'solver':ObjectsParams[i].solver})
              ArrayCombined[i] = newObjectsParamsLDA[i]
            } else if (this.selAlgorithm === 'QDA') {
              newObjectsParamsQDA.push({model: this.QDAModels + i,'# Perf (%) #': this.listClassPerf[6][i],'reg_param':ObjectsParams[i].reg_param,'tol':ObjectsParams[i].tol})
              ArrayCombined[i] = newObjectsParamsQDA[i]
            } else if (this.selAlgorithm === 'RF') {
              newObjectsParamsRF.push({model: this.RFModels + i,'# Perf (%) #': this.listClassPerf[7][i],'n_estimators':ObjectsParams[i].n_estimators,'criterion':ObjectsParams[i].criterion})
              ArrayCombined[i] = newObjectsParamsRF[i]
            } else if (this.selAlgorithm === 'ExtraT') {
              newObjectsParamsExtraT.push({model: this.ExtraTModels + i,'# Perf (%) #': this.listClassPerf[8][i],'n_estimators':ObjectsParams[i].n_estimators,'criterion':ObjectsParams[i].criterion})
              ArrayCombined[i] = newObjectsParamsExtraT[i]
            } else if (this.selAlgorithm === 'AdaB') {
              newObjectsParamsAdaB.push({model: this.AdaBModels + i,'# Perf (%) #': this.listClassPerf[9][i],'n_estimators':ObjectsParams[i].n_estimators,'learning_rate':ObjectsParams[i].learning_rate,'algorithm':ObjectsParams[i].algorithm})
              ArrayCombined[i] = newObjectsParamsAdaB[i]
            } else {
              newObjectsParamsGradB.push({model: this.GradBModels + i,'# Perf (%) #': this.listClassPerf[10][i],'n_estimators':ObjectsParams[i].n_estimators,'criterion':ObjectsParams[i].criterion,'learning_rate':ObjectsParams[i].learning_rate})
              ArrayCombined[i] = newObjectsParamsGradB[i]
            }
          }
        }
        EventBus.$emit('AllAlModels', ArrayCombined.length)
        this.pc = ParCoords()("#PCP")
            .data(ArrayCombined)
            .color(colorGiv)
            .hideAxis(['model'])
            .bundlingStrength(0) // set bundling strength
            .smoothness(0)
            .showControlPoints(false)
            .render()
            .brushMode('1D-axes')
            .reorderable()
            .interactive();

        this.pc.on("brushend", function(d) {
          EventBus.$emit('AllSelModels', d.length)
          EventBus.$emit('UpdateBoxPlot', d)
        });
      }
    },
    sliders () {

    },

    clear () {
        d3.selectAll("#PCP > *").remove(); 
    },
  },
  mounted() {
    EventBus.$on('ReturningBrushedPointsModels', this.brushed)
    EventBus.$on('emittedEventCallingModelSelect', data => { this.selAlgorithm = data })
    EventBus.$on('emittedEventCallingModel', data => { this.ModelsPerformance = data })
    EventBus.$on('emittedEventCallingModel', this.PCPView)
    EventBus.$on('ResponsiveandChange', this.PCPView)
    EventBus.$on('emittedEventCallingModelClear', this.clear)

    EventBus.$on('CallFactorsView', data => { this.factors = data })
    EventBus.$on('CallFactorsView', this.PCPView)

    EventBus.$on('boxplotSet', data => { this.listClassPerf = data })
    EventBus.$on('boxplotCall', data => { this.keyAllOrClass = data })

    // reset view
    EventBus.$on('resetViews', this.reset)
    EventBus.$on('clearPCP', this.reset)
  }
}
</script>