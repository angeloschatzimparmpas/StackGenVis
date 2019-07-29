<template>
  <div id="myDynamicTable" v-on:change="this.getFeatureSelection"></div>
</template>

<script>
import { EventBus } from '../main.js'

export default {
  name: 'FeatureSelection',
  data () {
    return {
      GetResults: '',
      datafromCheckbox: ''
    }
  },
  methods: {
      FeatureSelection () { 

        document.getElementById("myDynamicTable").innerHTML = "";

        var myTableDiv = document.getElementById("myDynamicTable");

        var table = document.createElement('TABLE');
        table.border = '1';

        var tableBody = document.createElement('TBODY');
        table.appendChild(tableBody);

        var checkBoxArray = []

        for (var i = 0; i < 3; i++) {
            var tr = document.createElement('TR');
            tableBody.appendChild(tr);
            for (var j = 0; j < 4; j++) {
                if (j == 0){
                    if (i == 0) {
                        var td = document.createElement('TD');
                        td.width = '75';
                        td.appendChild(document.createTextNode(''));
                        tr.appendChild(td);
                    } else {
                        var td = document.createElement('TD');
                        td.width = '90';
                        td.appendChild(document.createTextNode('Classifier ' + i));
                        tr.appendChild(td);
                    }
                }
                if (i == 0){
                    var td = document.createElement('TD');
                    td.width = '30';
                    td.appendChild(document.createTextNode('F ' + j));
                    tr.appendChild(td);
                } else {
                    var checkbox = document.createElement('input');
                    checkbox.type = "checkbox";
                    checkbox.checked = true;
                    checkbox.name = i;
                    checkbox.text = "F " + j
                    checkbox.value = "value";
                    checkbox.id = "Cl " + i + ", F " + j;
                    checkBoxArray.push(checkbox)
                    var td = document.createElement('TD');
                    td.appendChild(myTableDiv.appendChild(checkbox));
                    tr.appendChild(td);
                }
            
            }
        }
        myTableDiv.appendChild(table);
        this.datafromCheckbox = checkBoxArray
      },
      getFeatureSelection () {
        var results = new Array();
        this.datafromCheckbox.forEach(eachCheckbox => {
            if (eachCheckbox.checked == true) {
                results.push('ClassifierID: ' + eachCheckbox.name, 'FeatureName: ' + eachCheckbox.text, 'Check: 1')
            }
            else {
                results.push('ClassifierID: ' + eachCheckbox.name, 'FeatureName: ' + eachCheckbox.text, 'Check: 0')
            }
        });
        console.log(results)
        EventBus.$emit('SendSelectedFeaturesEvent', results)
      }
  },
  mounted () {
        EventBus.$on('emittedEventCallingTableView', data => { this.GetResults = data })
        EventBus.$on('emittedEventCallingTableView', this.FeatureSelection)
    }
}
</script>