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
      datafromCheckbox: '',
      loop: 0
    }
  },
  methods: {
      FeatureSelection () { 
        
        document.getElementById("myDynamicTable").innerHTML = "";
        let Features= JSON.parse(this.GetResults[7])
        let ClassifierswithoutFI = JSON.parse(this.GetResults[8])
        let ClassifierswithFI = JSON.parse(this.GetResults[9])
        const limit = JSON.parse(this.GetResults[12])
        var Classifiers
        Classifiers = ClassifierswithoutFI.concat(ClassifierswithFI)
        var limitList = []
        if (limit == '') {
            for (let i = 0; i < Classifiers.length; i++) {
                limitList.push(Classifiers[i])
            }
        } else {
            limitList = []
            for (let i = 0; i < limit.length; i++) {
                for (let j = 0; j < Classifiers.length; j++) {
                    if (Number(limit[i].match(/\d+/)[0]) == Classifiers[j]) {
                        limitList.push(Number(limit[i].match(/\d+/)[0]))
                    }
                }
            }
        }
        var myTableDiv = document.getElementById("myDynamicTable");
        var table = document.createElement('TABLE');
        table.border = '1';

        var tableBody = document.createElement('TBODY');
        table.appendChild(tableBody);

        var checkBoxArray = []
        for (var i = 0; i < limitList.length+1; i++) {
            var tr = document.createElement('TR');
            tableBody.appendChild(tr);
            for (var j = 0; j < Features.length; j++) {
                if (j == 0){
                    if (i == 0) {
                        var td = document.createElement('TD');
                        td.width = '75';
                        td.appendChild(document.createTextNode(''));
                        tr.appendChild(td);
                    } else {
                        var td = document.createElement('TD');
                        td.width = '90';
                        td.appendChild(document.createTextNode('M ' + (i - 1)));
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
                    checkbox.name = i-1;
                    checkbox.text = "F " + j
                    checkbox.value = "value";
                    checkbox.id = "M " + (i-1) + ", F " + j;
                    checkBoxArray.push(checkbox)
                    var td = document.createElement('TD');
                    td.appendChild(myTableDiv.appendChild(checkbox));
                    tr.appendChild(td);
                }
            
            }
        }
        //if (this.loop == 0) {
            myTableDiv.appendChild(table);
        //}
        this.loop++
        this.datafromCheckbox = checkBoxArray
      },
      getFeatureSelection () {

        var results = new Array()
        this.datafromCheckbox.forEach(eachCheckbox => {
            if (eachCheckbox.checked == true) {
                results.push('ClassifierID: ' + eachCheckbox.name, 'FeatureName: ' + eachCheckbox.text, 'Check: 1')
            }
            else {
                results.push('ClassifierID: ' + eachCheckbox.name, 'FeatureName: ' + eachCheckbox.text, 'Check: 0')
            }
        });
        EventBus.$emit('SendSelectedFeaturesEvent', results)
      }
  },
  mounted () {
        EventBus.$on('emittedEventCallingTableView', data => { this.GetResults = data })
        EventBus.$on('emittedEventCallingTableView', this.FeatureSelection)
    }
}
</script>