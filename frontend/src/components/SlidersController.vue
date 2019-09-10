<template>
    <div id="WrapSliders" style="display:none">
                <p>Accuracy:<b-form-slider ref="basic1" v-model="basicValue1" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px;padding-left:15px"></b-form-slider>{{ basicValue1 }}%</p>
                <p>F1_Score:<b-form-slider ref="basic2" v-model="basicValue2" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider >{{ basicValue2 }}%</p>
                <p>Precision:<b-form-slider ref="basic3" v-model="basicValue3" :min="0" :max="100" trigger-change-event @slide-start="slideStart"  @slide-stop="slideStop"style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue3 }}%</p>
                <p>Recall:<b-form-slider ref="basic4" v-model="basicValue4" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue4 }}%</p>
                <p>Jaccard_Score:<b-form-slider ref="basic5" v-model="basicValue5" :min="0" :max="100" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 15px; padding-left:15px"></b-form-slider>{{ basicValue5 }}%</p>
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
            basicValue5: 100
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
            Enable () {
                document.getElementById('WrapSliders').style.cssText='height:200px;display:""';
            },
            Disable () {
                document.getElementById('WrapSliders').style.cssText='display:none';
            }
        },
        mounted () {
            EventBus.$on('slidersOn', this.Enable)
            EventBus.$on('PCPCall', this.Disable)
        }
    }
</script>
