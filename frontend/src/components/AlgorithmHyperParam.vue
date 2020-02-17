<template>
  <div id="PCP" class="parcoords" style="min-height: 307px;"></div>
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
      pc: 0,
      factors: [1,1,1,0,0
      ,1,0,0,1,0
      ,0,1,0,0,0
      ,0,0,1,0,0
      ,0,1,1,1
      ],
      KNNModels: 576 //KNN models
    }
  },
  methods: {
    reset () {
      d3.selectAll("#PCP > *").remove(); 
    },
    PCPView () {
      d3.selectAll("#PCP > *").remove(); 
      if (this.selAlgorithm != '') {
        var colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
        var colorGiv = 0
        
        var factorsLocal = this.factors
        var divide = 0

        factorsLocal.forEach(element => {
          divide = element + divide
        });

        var Mc1 = []
        const performanceAlg1 = JSON.parse(this.ModelsPerformance[6])

        for (let j = 0; j < Object.values(performanceAlg1['mean_test_accuracy']).length; j++) {
          let sum
          sum = (factorsLocal[0] * Object.values(performanceAlg1['mean_test_accuracy'])[j]) + (factorsLocal[1] * (Object.values(performanceAlg1['mean_test_neg_mean_absolute_error'])[j]) + 1) + (factorsLocal[2] * (Object.values(performanceAlg1['mean_test_neg_root_mean_squared_error'])[j]) + 1) + (factorsLocal[3] * Object.values(performanceAlg1['geometric_mean_score_micro'])[j]) + (factorsLocal[4] * Object.values(performanceAlg1['geometric_mean_score_macro'])[j])
            + (factorsLocal[5] * Object.values(performanceAlg1['geometric_mean_score_weighted'])[j]) + (factorsLocal[6] * Object.values(performanceAlg1['mean_test_precision_micro'])[j]) + (factorsLocal[7] * Object.values(performanceAlg1['mean_test_precision_macro'])[j]) + (factorsLocal[8] * Object.values(performanceAlg1['mean_test_precision_weighted'])[j]) + (factorsLocal[9] * Object.values(performanceAlg1['mean_test_recall_micro'])[j])
            + (factorsLocal[10] * Object.values(performanceAlg1['mean_test_recall_macro'])[j]) + (factorsLocal[11] * Object.values(performanceAlg1['mean_test_recall_weighted'])[j]) + (factorsLocal[12] * Object.values(performanceAlg1['f5_micro'])[j]) + (factorsLocal[13] * Object.values(performanceAlg1['f5_macro'])[j]) + (factorsLocal[14] * Object.values(performanceAlg1['f5_weighted'])[j]) + (factorsLocal[15] * Object.values(performanceAlg1['f1_micro'])[j])
            + (factorsLocal[16] * Object.values(performanceAlg1['f1_macro'])[j]) + (factorsLocal[17] * Object.values(performanceAlg1['f1_weighted'])[j]) + (factorsLocal[18] * Object.values(performanceAlg1['f2_micro'])[j]) + (factorsLocal[19] * Object.values(performanceAlg1['f2_macro'])[j]) + (factorsLocal[20] * Object.values(performanceAlg1['f2_weighted'])[j]) + (factorsLocal[21] * Object.values(performanceAlg1['matthews_corrcoef'])[j])
            + (factorsLocal[22] * Object.values(performanceAlg1['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[23] * (1 - Object.values(performanceAlg1['log_loss'])[j]))
          Mc1.push((sum/divide)*100)
        }

        var Mc2 = []
        const performanceAlg2 = JSON.parse(this.ModelsPerformance[14])
        for (let j = 0; j < Object.values(performanceAlg2['mean_test_accuracy']).length; j++) {
          let sum2
          sum2 = (factorsLocal[0] * Object.values(performanceAlg2['mean_test_accuracy'])[j]) + (factorsLocal[1] * (Object.values(performanceAlg2['mean_test_neg_mean_absolute_error'])[j]) + 1) + (factorsLocal[2] * (Object.values(performanceAlg2['mean_test_neg_root_mean_squared_error'])[j]) + 1) + (factorsLocal[3] * Object.values(performanceAlg2['geometric_mean_score_micro'])[j]) + (factorsLocal[4] * Object.values(performanceAlg2['geometric_mean_score_macro'])[j])
            + (factorsLocal[5] * Object.values(performanceAlg2['geometric_mean_score_weighted'])[j]) + (factorsLocal[6] * Object.values(performanceAlg2['mean_test_precision_micro'])[j]) + (factorsLocal[7] * Object.values(performanceAlg2['mean_test_precision_macro'])[j]) + (factorsLocal[8] * Object.values(performanceAlg2['mean_test_precision_weighted'])[j]) + (factorsLocal[9] * Object.values(performanceAlg2['mean_test_recall_micro'])[j])
            + (factorsLocal[10] * Object.values(performanceAlg2['mean_test_recall_macro'])[j]) + (factorsLocal[11] * Object.values(performanceAlg2['mean_test_recall_weighted'])[j]) + (factorsLocal[12] * Object.values(performanceAlg2['f5_micro'])[j]) + (factorsLocal[13] * Object.values(performanceAlg2['f5_macro'])[j]) + (factorsLocal[14] * Object.values(performanceAlg2['f5_weighted'])[j]) + (factorsLocal[15] * Object.values(performanceAlg2['f1_micro'])[j])
            + (factorsLocal[16] * Object.values(performanceAlg2['f1_macro'])[j]) + (factorsLocal[17] * Object.values(performanceAlg2['f1_weighted'])[j]) + (factorsLocal[18] * Object.values(performanceAlg2['f2_micro'])[j]) + (factorsLocal[19] * Object.values(performanceAlg2['f2_macro'])[j]) + (factorsLocal[20] * Object.values(performanceAlg2['f2_weighted'])[j]) + (factorsLocal[21] * Object.values(performanceAlg2['matthews_corrcoef'])[j])
            + (factorsLocal[22] * Object.values(performanceAlg2['mean_test_roc_auc_ovo_weighted'])[j]) + (factorsLocal[23] * (1 - Object.values(performanceAlg2['log_loss'])[j]))
          Mc2.push((sum2/divide)*100)
        }

        var Combined = 0
        if (this.selAlgorithm == 'KNN') {    
          Combined = JSON.parse(this.ModelsPerformance[1])
          colorGiv = colors[0]
        } else {
          Combined = JSON.parse(this.ModelsPerformance[9])
          colorGiv = colors[1]
        }
        var valuesPerf = Object.values(Combined['params'])
        
        var ObjectsParams = Combined['params']
        var newObjectsParams = []
        var newObjectsParams2 = []
        var ArrayCombined = []
        var temp
        for (var i = 0; i < valuesPerf.length; i++) {
          if (this.selAlgorithm === 'KNN') {
            // There is a problem here!
            newObjectsParams.push({model: i,'performance (%)': Mc1[i],'n_neighbors':ObjectsParams[i].n_neighbors,'metric':ObjectsParams[i].metric,'algorithm':ObjectsParams[i].algorithm,'weights':ObjectsParams[i].weights})
            ArrayCombined[i] = newObjectsParams[i]
          } else {
            newObjectsParams2.push({model: this.KNNModels + i,'performance (%)': Mc2[i],'n_estimators':ObjectsParams[i].n_estimators,'criterion':ObjectsParams[i].criterion})
            ArrayCombined[i] = newObjectsParams2[i]
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

    // reset view
    EventBus.$on('resetViews', this.reset)
    EventBus.$on('clearPCP', this.reset)
  }
}
</script>