<template>
    <div>
                <p><font-awesome-icon icon="balance-scale"/> Optimize Selection:<b-form-slider ref="basic1" v-model="basicValue" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue }}%</p>
    </div>
</template>

<script>
    import bFormSlider from 'vue-bootstrap-slider/es/form-slider';
    import 'bootstrap-slider/dist/css/bootstrap-slider.css'
    import { EventBus } from '../main.js'

    export default {
        name: 'BalancePredictions',
        data () {
            return {
            basicValue: 0,
            }
        },
        methods: {
            slideStart () {
            },
            slideStop () {
                //var basicValues = []
                //EventBus.$emit('CallFactorsView', basicValues)
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