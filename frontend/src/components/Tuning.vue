<template>
  <div>
    <div>Limiting Feature Importance<vue-slider v-model="LimitFeatureImportance"></vue-slider></div>
    <div>{{ LimitFeatureImportance }}</div>
  </div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

export default {
  name: 'Tuning',
  components: {
    VueSlider
  },
  data () {
    return {
      LimitFeatureImportance: 10
    }
  },
  mounted () {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.slidecontainer {
width: 100%;
}

.slider {
-webkit-appearance: none;
width: 100%;
height: 15px;
border-radius: 5px;
background: #d3d3d3;
outline: none;
opacity: 0.7;
-webkit-transition: .2s;
transition: opacity .2s;
}

.slider:hover {
opacity: 1;
}

.slider::-webkit-slider-thumb {
-webkit-appearance: none;
appearance: none;
width: 25px;
height: 25px;
border-radius: 50%;
background: #4CAF50;
cursor: pointer;
}

.slider::-moz-range-thumb {
width: 25px;
height: 25px;
border-radius: 50%;
background: #4CAF50;
cursor: pointer;
}
</style>
