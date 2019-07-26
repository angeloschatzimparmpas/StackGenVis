<template>
  <button
  id="Execute"
  v-on:click="execute">
  <font-awesome-icon icon="play" />
  Execute</button>
</template>

<script>
export default {
  name: 'ParametersSetting',
  data () {
    return {
        InitializeEnsemble: false,
    };
  },
  methods: {
    execute () {
        this.InitializeEnsemble = true
        this.$emit('InitializeEnsembleLearningEvent')
    }
  }
}
</script>