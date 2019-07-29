<template>
  <button
  id="Execute"
  v-on:click="execute">
  <font-awesome-icon icon="play" />
  {{ value }}
  </button>
</template>

<script>
export default {
  name: 'ParametersSetting',
  data () {
    return {
        InitializeEnsemble: false,
        value: 'Execute'
    };
  },
  methods: {
    execute () {
        this.InitializeEnsemble = true
        this.value = 'ReExecute'
        this.$emit('InitializeEnsembleLearningEvent')
    }
  }
}
</script>