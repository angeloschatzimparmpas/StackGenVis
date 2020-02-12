<template>
    <div id="toggles" style="visibility:hidden">
        Univariate Selection:<input type="checkbox" id="toggle-uni" data-toggle="toggle" checked="checked" data-on="Enabled" data-off="Disabled" data-size="small">
        Permutation Importance:<input type="checkbox" id="toggle-per" data-toggle="toggle" checked="checked" data-on="Enabled" data-off="Disabled" data-size="small">
        Feature Accuracy Importance:<input type="checkbox" id="toggle-fi" data-toggle="toggle" checked="checked" data-on="Enabled" data-off="Disabled" data-size="small">
    </div>
</template>

<script>
import { EventBus } from '../main.js'
import $ from 'jquery'
import { bootstrapToggle } from 'bootstrap-toggle'
import 'bootstrap-toggle/css/bootstrap-toggle.css'

export default {
  name: 'ToggleSelection',
  data () {
    return {
    }
  },
  methods: {
      ToggleSelection () { 
      },
      ToggleShow () { 
        document.getElementById('toggles').style.visibility = "visible"
      }
  },
  mounted () {
    $('#toggle-uni').bootstrapToggle({
        on: 'Enabled',
        off: 'Disabled'
    });
    $('#toggle-uni').change(function() {
        var toggleID = document.getElementById('toggle-uni')
        if (toggleID.checked === false) {
            EventBus.$emit('toggle1', 0)
        } else {
            EventBus.$emit('toggle1', 1)
        }
    })
    $('#toggle-per').bootstrapToggle({
        on: 'Enabled',
        off: 'Disabled'
    });
    $('#toggle-per').change(function() {
        var toggleID = document.getElementById('toggle-per')
        if (toggleID.checked === false) {
            EventBus.$emit('toggle2', 0)
        } else {
            EventBus.$emit('toggle2', 1)
        }
    })
    $('#toggle-fi').bootstrapToggle({
        on: 'Enabled',
        off: 'Disabled'
    });
    $('#toggle-fi').change(function() {
        var toggleID = document.getElementById('toggle-fi')
        if (toggleID.checked === false) {
            EventBus.$emit('toggle3', 0)
        } else {
            EventBus.$emit('toggle3', 1)
        }
    })
    EventBus.$on('emittedEventCallingToggles', this.ToggleShow)
  }
}
</script>