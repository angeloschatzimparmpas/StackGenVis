<!-- Main Visualization View -->

<template>
  <div>
    <LoadFile
    />
  </div>
</template>

<script>
import Vue from 'vue'
import LoadFile from './LoadFile.vue'

export default Vue.extend({
  name: 'Main',
  components: {
    LoadFile
  },
  data: function () {
    return {
      nothing: 0
    }
  },
  methods: {

  },
  props: [],
  computed: {

  }
})
</script>
