<template>
<b-row>
    <b-col cols="9">
      <div id="WrapSliders">
        <p>(1) Accuracy:<b-form-slider ref="basic1" v-model="basicValue1" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue1 }}%</p>
        <p>(2) MAE:<b-form-slider ref="basic2" v-model="basicValue2" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue2 }}%</p>
        <p>(3) RMSE:<b-form-slider ref="basic3" v-model="basicValue3" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue3 }}%</p>
        <p>(4*) G-Mean:<b-form-slider ref="basic4" v-model="basicValue4" :min="0" :max="100" trigger-change-event @slide-start="slideStart"  @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue4 }}%</p>
        <p>(5*) Precision:<b-form-slider ref="basic5" v-model="basicValue5" :min="0" :max="100" trigger-change-event @slide-start="slideStart"  @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue5 }}%</p>
        <p>(6*) Recall:<b-form-slider ref="basic6" v-model="basicValue6" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue6 }}%</p>
        <p>(7*) F-Beta Score:<b-form-slider ref="basic7" v-model="basicValue7" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider >{{ basicValue7 }}%</p>
        <p>(8) MCC:<b-form-slider ref="basic8" v-model="basicValue8" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue8 }}%</p>
        <p>(9) ROC AUC:<b-form-slider ref="basic9" v-model="basicValue9" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue9 }}%</p>
        <p>(10) Log Loss:<b-form-slider ref="basic10" v-model="basicValue10" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue10 }}%</p>
      </div>
    </b-col>
    <b-col cols="3" style="padding-top: 55px">
        <p>(*) Average: 
        <select id="selectFilterAverage" @change="selectAppliedFilterAverage()">
        <option value="weighted" selected>Weighted</option>
        <option value="micro">Micro</option>
        <option value="macro">Macro</option>
      </select></p>
      <br />
        <p>(7) Beta Value: 
        <select id="selectFilterBeta" @change="selectAppliedFilterBeta()">
        <option value="one" selected>F1 Score</option>
        <option value="half">F0.5 Score</option>
        <option value="two">F2 Score</option>
      </select></p>
    </b-col>
</b-row>
</template>

<script>
    import bFormSlider from 'vue-bootstrap-slider/es/form-slider';
    import 'bootstrap-slider/dist/css/bootstrap-slider.css'
    import { EventBus } from '../main.js'

    export default {
        name: 'SlidersController',
        data () {
          return {
              basicValue1: 100,
              basicValue2: 100,
              basicValue3: 100,
              basicValue4: 100,
              basicValue5: 100,
              basicValue6: 100,
              basicValue7: 100,
              basicValue8: 100,
              basicValue9: 100,
              basicValue10: 100,
              factorsLocal: [1,1,1,0,0
              ,1,0,0,1,0
              ,0,1,0,0,0
              ,0,0,1,0,0
              ,0,1,1,1
              ],
              userSelectedFilterAver: 'weighted',
              userSelectedFilterBeta: 'one'
          }
        },
        methods: {
          selectAppliedFilterAverage () {
            var representationSelectionDocum = document.getElementById('selectFilterAverage')
            this.userSelectedFilterAver = representationSelectionDocum.options[representationSelectionDocum.selectedIndex].value
            this.slideStop()
          },
          selectAppliedFilterBeta () {
            var representationSelectionDocum = document.getElementById('selectFilterBeta')
            this.userSelectedFilterBeta = representationSelectionDocum.options[representationSelectionDocum.selectedIndex].value
            this.slideStop()
          },
          slideStart () {
          },
          slideStop () {
              if (this.userSelectedFilterAver == 'micro') {
                this.factorsLocal[3] = this.basicValue4
                this.factorsLocal[4] = 0
                this.factorsLocal[5] = 0
                this.factorsLocal[6] = this.basicValue5
                this.factorsLocal[7] = 0
                this.factorsLocal[8] = 0
                this.factorsLocal[9] = this.basicValue6
                this.factorsLocal[10] = 0
                this.factorsLocal[11] = 0
                if (this.userSelectedFilterBeta == 'half') {
                  this.factorsLocal[12] = this.basicValue7
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = 0
                } else if (this.userSelectedFilterBeta == 'two') {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = this.basicValue7
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = 0
                } else {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = this.basicValue7
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = 0
                }
              } else if (this.userSelectedFilterAver == 'macro') {
                this.factorsLocal[3] = 0
                this.factorsLocal[4] = this.basicValue4
                this.factorsLocal[5] = 0
                this.factorsLocal[6] = 0
                this.factorsLocal[7] = this.basicValue5
                this.factorsLocal[8] = 0
                this.factorsLocal[9] = 0
                this.factorsLocal[10] = this.basicValue6
                this.factorsLocal[11] = 0
                if (this.userSelectedFilterBeta == 'half') {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = this.basicValue7
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = 0
                } else if (this.userSelectedFilterBeta == 'two') {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = this.basicValue7
                  this.factorsLocal[20] = 0
                } else {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = this.basicValue7
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = 0
                }
              } else {
                this.factorsLocal[3] = 0
                this.factorsLocal[4] = 0
                this.factorsLocal[5] = this.basicValue4
                this.factorsLocal[6] = 0
                this.factorsLocal[7] = 0
                this.factorsLocal[8] = this.basicValue5
                this.factorsLocal[9] = 0
                this.factorsLocal[10] = 0
                this.factorsLocal[11] = this.basicValue6
                if (this.userSelectedFilterBeta == 'half') {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = this.basicValue7
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = 0
                } else if (this.userSelectedFilterBeta == 'two') {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = this.basicValue7
                } else {
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = this.basicValue7
                  this.factorsLocal[18] = 0
                  this.factorsLocal[19] = 0
                  this.factorsLocal[20] = 0
                }
              }
              this.factorsLocal[0] = this.basicValue1/100
              this.factorsLocal[1] = this.basicValue2/100
              this.factorsLocal[2] = this.basicValue3/100
              this.factorsLocal[21] = this.basicValue8/100
              this.factorsLocal[22] = this.basicValue9/100
              this.factorsLocal[23] = this.basicValue10/100
              EventBus.$emit('CallFactorsView', this.factorsLocal)
          },
        },
    }
</script>

<style>
p {
    margin: 0 !important;
    padding: 0 !important;
}

/*.slider.slider-horizontal {
    width: 300px !important;
}*/

.slider-handle {
    background: black;
}
</style>