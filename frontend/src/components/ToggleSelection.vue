<template>
    <div id="toggles" style="visibility:hidden">
        Univariate FS:&nbsp;<input type="checkbox" id="toggle-uni" data-toggle="toggle" checked="checked" data-on="Enabled" data-off="Disabled" data-size="small">&nbsp;&nbsp;&nbsp;
        Permutation FI:&nbsp;<input type="checkbox" id="toggle-per" data-toggle="toggle" checked="checked" data-on="Enabled" data-off="Disabled" data-size="small">&nbsp;&nbsp;&nbsp;
        Accuracy FI:&nbsp;<input type="checkbox" id="toggle-fi" data-toggle="toggle" checked="checked" data-on="Enabled" data-off="Disabled" data-size="small">
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
        toggleDeepLocal: 1
    }
  },
  methods: {
      ResetPosition () {
        $('input[type=checkbox]').each(function() { 
                $(this).bootstrapToggle('on'); //you can set "on" or "off" 
        });
      },
      ToggleManage () { 
      if(this.toggleDeepLocal == 0) {
        document.getElementById('toggles').style.visibility = "hidden"
      } else {
        document.getElementById('toggles').style.visibility = "visible"
      }
      }
  },
  mounted () {
    this.ToggleManage()
    EventBus.$on('toggleDeep', data => {this.toggleDeepLocal = data})
    EventBus.$on('toggleDeep', this.ToggleManage)

    EventBus.$on('resetToggles', this.ResetPosition)
    $('#toggle-uni').bootstrapToggle({
        on: 'On',
        off: 'Off',
        width: '8%',
    });
    $('#toggle-uni').change(function() {
        var toggleIDUni = document.getElementById('toggle-uni')
        var toggleIDPer = document.getElementById('toggle-per')
        var toggleIDFi = document.getElementById('toggle-fi')
        if (toggleIDUni.checked === false) {
            EventBus.$emit('toggle1', 0)
        } else {
            EventBus.$emit('toggle1', 1)
        }
    })
    $('#toggle-per').bootstrapToggle({
        on: 'On',
        off: 'Off',
        width: '8%',
    });
    $('#toggle-per').change(function() {
        var toggleIDUni = document.getElementById('toggle-uni')
        var toggleIDPer = document.getElementById('toggle-per')
        var toggleIDFi = document.getElementById('toggle-fi')
        if (toggleIDPer.checked === false) {
            EventBus.$emit('toggle2', 0)
        } else {
            EventBus.$emit('toggle2', 1)
        }
    })
    $('#toggle-fi').bootstrapToggle({
        on: 'On',
        off: 'Off',
        width: '8%',
    });
    $('#toggle-fi').change(function() {
        var toggleIDUni = document.getElementById('toggle-uni')
        var toggleIDPer = document.getElementById('toggle-per')
        var toggleIDFi = document.getElementById('toggle-fi')
        if (toggleIDFi.checked === false) {
            EventBus.$emit('toggle3', 0)
        } else {
            EventBus.$emit('toggle3', 1)
        }
    })
  }
}
</script>