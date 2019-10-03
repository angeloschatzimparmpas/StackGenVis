<template>
    <div id="WrapSliders">
                <p>Acc<b-form-slider ref="basic1" v-model="basicValue1" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue1 }}%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Met6<b-form-slider ref="basic1" v-model="basicValue6" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue6 }}%</p>
                <p>F1s<b-form-slider ref="basic2" v-model="basicValue2" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider >{{ basicValue2 }}%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Met7<b-form-slider ref="basic1" v-model="basicValue7" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue7 }}%</p>
                <p>Pre<b-form-slider ref="basic3" v-model="basicValue3" :min="0" :max="100" trigger-change-event @slide-start="slideStart"  @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue3 }}%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Met8<b-form-slider ref="basic1" v-model="basicValue8" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue8 }}%</p>
                <p>Rec<b-form-slider ref="basic4" v-model="basicValue4" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue4 }}%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Met9<b-form-slider ref="basic1" v-model="basicValue9" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue9 }}%</p>
                <p>Jac<b-form-slider ref="basic5" v-model="basicValue5" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue5 }}%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Me10<b-form-slider ref="basic1" v-model="basicValue10" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue10 }}%</p>
    </div>
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
            basicValue10: 100
            }
        },
        methods: {
            slideStart () {
            },
            slideStop () {
                var basicValues = []
                basicValues.push(this.basicValue1/100)
                basicValues.push(this.basicValue2/100)
                basicValues.push(this.basicValue3/100)
                basicValues.push(this.basicValue4/100)
                basicValues.push(this.basicValue5/100)
                EventBus.$emit('CallFactorsView', basicValues)
            },
        },
    }
</script>

<style>
p {
    margin: 0 !important;
    padding: 0 !important;
}
.slider.slider-horizontal {
    width: 150px !important;
}
.slider-handle {
    background: black;
}
</style>