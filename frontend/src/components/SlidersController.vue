<template>
<div>
<b-row>
    <b-col cols="12">
      <table class="table table-borderless table-sm">
        <tbody>
          <tr>
            <td>(M1) Accuracy:</td>
            <td><b-form-slider ref="basic1" v-model="basicValue1" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;"></b-form-slider>{{ basicValue1 }}%</td>
            <td style="text-align: center; width: 70px"><font-awesome-icon class="fa-lg" icon="dice-four"/></td>
          </tr>
          <tr>
            <td>(M2*) G-Mean:</td>
            <td><b-form-slider ref="basic2" v-model="basicValue2" :min="0" :max="100" trigger-change-event @slide-start="slideStart"  @slide-stop="slideStop" style="padding-right: 15px;"></b-form-slider>{{ basicValue2 }}%</td>
            <td style="text-align: center; width: 70px"></td>
          </tr>
          <tr>
            <td>(M3*) Precision:</td>
            <td><b-form-slider ref="basic3" v-model="basicValue3" :min="0" :max="100" trigger-change-event @slide-start="slideStart"  @slide-stop="slideStop" style="padding-right: 15px; "></b-form-slider>{{ basicValue3 }}%</td>
            <td style="text-align: center; width: 70px"><font-awesome-icon class="fa-lg" icon="dice-three"/>&nbsp;<font-awesome-icon class="fa-lg" icon="dice-four"/></td>
          </tr>
          <tr>
            <td>(M4*) Recall:</td>
            <td><b-form-slider ref="basic4" v-model="basicValue4" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; "></b-form-slider>{{ basicValue4 }}%</td>
            <td style="text-align: center; width: 70px"><font-awesome-icon class="fa-lg" icon="dice-three"/>&nbsp;<font-awesome-icon class="fa-lg" icon="dice-four"/></td>
          </tr>
          <tr>
            <td width="185">(M5*) <select id="selectFilterBeta" @change="selectAppliedFilterBeta()" >
        <option value="one" selected>F1 Score</option>
        <option value="half">F0.5 Score</option>
        <option value="two">F2 Score</option>
      </select>:</td>
            <td><b-form-slider ref="basic5" v-model="basicValue5" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; "></b-form-slider >{{ basicValue5 }}%</td>
            <td style="text-align: center; width: 70px"><font-awesome-icon class="fa-lg" icon="dice-three"/>&nbsp;<font-awesome-icon class="fa-lg" icon="dice-four"/></td>
          </tr>
          <tr>
            <td>(M6) MCC:</td>
            <td><b-form-slider ref="basic6" v-model="basicValue6" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; "></b-form-slider>{{ basicValue6 }}%</td>
            <td style="text-align: center; width: 70px"></td>
          </tr>
          <tr>
            <td>(M7) ROC AUC:</td>
            <td><b-form-slider ref="basic7" v-model="basicValue7" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;"></b-form-slider>{{ basicValue7 }}%</td>
            <td style="text-align: center; width: 70px"></td>
          </tr>
          <tr>
            <td>(M8) Log Loss:</td>
            <td><b-form-slider ref="basic8" v-model="basicValue8" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;"></b-form-slider>{{ basicValue8 }}%</td>
            <td style="text-align: center; width: 70px"></td>
          </tr>
        </tbody>
      </table>
    </b-col>
</b-row>
<b-row>
    <b-col cols="6">
        <p>(*) Aver.: <select id="selectFilterAverage" @change="selectAppliedFilterAverage()">
        <option value="weighted" selected>Weighted</option>
        <option value="micro">Micro</option>
        <option value="macro">Macro</option>
      </select></p>
    </b-col>
    <b-col cols="6">
        <p>Feat. Search: <input type="checkbox" id="toggleDeepID" data-toggle="toggle" checked="checked" data-on="Enabled" data-off="Disabled" data-size="small"></p>
    </b-col>
</b-row>
</div>
</template>

<script>
    import $ from 'jquery'
    import { bootstrapToggle } from 'bootstrap-toggle'
    import 'bootstrap-toggle/css/bootstrap-toggle.css'
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
              factorsLocal: [1,0,0
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
                this.factorsLocal[1] = this.basicValue2/100
                this.factorsLocal[2] = 0
                this.factorsLocal[3] = 0
                this.factorsLocal[4] = this.basicValue3/100
                this.factorsLocal[5] = 0
                this.factorsLocal[6] = 0
                this.factorsLocal[7] = this.basicValue4/100
                this.factorsLocal[8] = 0
                this.factorsLocal[9] = 0
                if (this.userSelectedFilterBeta == 'half') {
                  this.factorsLocal[10] = this.basicValue5/100
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[28] = 0
                } else if (this.userSelectedFilterBeta == 'two') {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = this.basicValue5/100
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                } else {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = this.basicValue5/100
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                }
              } else if (this.userSelectedFilterAver == 'macro') {
                this.factorsLocal[1] = 0
                this.factorsLocal[2] = this.basicValue2/100
                this.factorsLocal[3] = 0
                this.factorsLocal[4] = 0
                this.factorsLocal[5] = this.basicValue3/100
                this.factorsLocal[6] = 0
                this.factorsLocal[7] = 0
                this.factorsLocal[8] = this.basicValue4/100
                this.factorsLocal[9] = 0
                if (this.userSelectedFilterBeta == 'half') {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = this.basicValue5/100
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                } else if (this.userSelectedFilterBeta == 'two') {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = this.basicValue5/100
                  this.factorsLocal[18] = 0
                } else {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = this.basicValue5/100
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                }
              } else {
                this.factorsLocal[1] = 0
                this.factorsLocal[2] = 0
                this.factorsLocal[3] = this.basicValue2/100
                this.factorsLocal[4] = 0
                this.factorsLocal[5] = 0
                this.factorsLocal[6] = this.basicValue3/100
                this.factorsLocal[7] = 0
                this.factorsLocal[8] = 0
                this.factorsLocal[9] = this.basicValue4/100
                if (this.userSelectedFilterBeta == 'half') {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = this.basicValue5/100
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                } else if (this.userSelectedFilterBeta == 'two') {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = 0
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = this.basicValue5/100
                } else {
                  this.factorsLocal[10] = 0
                  this.factorsLocal[11] = 0
                  this.factorsLocal[12] = 0
                  this.factorsLocal[13] = 0
                  this.factorsLocal[14] = 0
                  this.factorsLocal[15] = this.basicValue5/100
                  this.factorsLocal[16] = 0
                  this.factorsLocal[17] = 0
                  this.factorsLocal[18] = 0
                }
              }
              this.factorsLocal[0] = this.basicValue1/100
              this.factorsLocal[19] = this.basicValue6/100
              this.factorsLocal[20] = this.basicValue7/100
              this.factorsLocal[21] = this.basicValue8/100
              EventBus.$emit('CallFactorsView', this.factorsLocal)
          },
        },
        mounted () {
          EventBus.$on('Responsive', data => {

            this.WH = data
            var myClasses = document.getElementsByClassName('slider slider-horizontal')

            for(var i = 0; i < myClasses.length; i++){
              if (this.WH[0] > 125) {
                myClasses[i].style.width = "260px"; // or
              }
              else {
                myClasses[i].style.width = "60px"; // depending on what you're doing
              }
            }
          })

          $('#toggleDeepID').bootstrapToggle({
            on: 'On',
            off: 'Off',
            width: '20%',
         });
        $('#toggleDeepID').change(function() {
          var toggleDeepSlid = document.getElementById('toggleDeepID')
          if (toggleDeepSlid.checked === false) {
            EventBus.$emit('toggleDeep', 0)
          } else {
            EventBus.$emit('toggleDeep', 1)
          }
        })
        }
    }
</script>

<style>
p {
    margin: 0 !important;
    padding: 0 !important;
}

.toggle-on.btn-sm {
  padding-right: 20px
}

.toggle-off.btn-sm {
  padding-right: 0px
}

.slider-handle {
    background: black;
}
</style>