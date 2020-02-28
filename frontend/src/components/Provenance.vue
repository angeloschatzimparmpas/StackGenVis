<template>
    <div>
        <div class="squares-container" style="min-height: 307px;">
        <div id="tooltip"></div>	<!-- new  -->
            <canvas id="main-canvas" ></canvas>
            <br>
            <div id="dynamic-buttons"></div>
        </div>
    </div>
</template>

<script>
import * as d3Base from 'd3'

import { EventBus } from '../main.js'
import $ from 'jquery'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

import * as Stardust from 'stardust-core'
import * as StardustGL from 'stardust-webgl'

export default {
  name: 'Provenance',
  data () {
    return {
      stackInformation: '',
      WH: [],
      data: [],
      counter: 0,
      typeCounter: [],
      typeColumnCounter: [],
      SVCModels: 576,
      GausNBModels: 736, 
      MLPModels: 1236,
      LRModels: 1356, 
      LDAModels: 1996,
      QDAModels: 2196,
      RFModels: 2446,
      ExtraTModels: 2606,
      AdaBModels: 2766,
      GradBModels: 2926,
      AllDetails: '',
      platform: '',
      count: 0,
      storeData: [],
      storePerformance: [],
      storeParameters: []
    }
  },
  methods: {
    reset () {
      if (this.platform == '') {

      } else {
        this.platform.clear();
      }
    },
    clean(obj) {
      var propNames = Object.getOwnPropertyNames(obj);
      for (var i = 0; i < propNames.length; i++) {
        var propName = propNames[i];
        if (obj[propName] === null || obj[propName] === undefined) {
          delete obj[propName];
        }
      }
    },
    provenance () {
      var canvas = document.getElementById("main-canvas");
      var width = this.WH[0]*7 // interactive visualization
      var height = this.WH[1]*0.58 // interactive visualization

      var flagKNN = 0
      var flagSVC = 0
      var flagGausNB = 0
      var flagMLP = 0
      var flagLR = 0
      var flagLDA = 0
      var flagQDA = 0
      var flagRF = 0
      var flagExtraT = 0
      var flagAdaB = 0
      var flagGradB = 0

      var localStackStore = []
      var StackInfo = JSON.parse(this.stackInformation[1])
      var arrayOfNumbers = StackInfo.map(Number)
      this.storeData.push(arrayOfNumbers)
      localStackStore = this.storeData.slice()

      var localPerfStore = []
      var performanceLoc = JSON.parse(this.AllDetails[0])
      this.storePerformance.push(performanceLoc)
      localPerfStore = this.storePerformance.slice()

      var localParamsStore = []
      var parameters = JSON.parse(this.AllDetails[2])
      var parameters = JSON.parse(parameters)
      this.storeParameters.push(parameters)
      localParamsStore = this.storeParameters.slice()

      var stringParameters = []
      var temp = 0
      for (let i = 0; i < StackInfo.length; i++) {
        this.clean(parameters[i])
        temp = JSON.stringify(Object.assign({ID: StackInfo[i]}, parameters[i]))
        stringParameters.push(temp)
      }

      // Create a WebGL 2D platform on the canvas:
      var plat = Stardust.platform("webgl-2d", canvas, width, height);
      plat.pixelRatio = window.devicePixelRatio || 1;
      this.platform = plat

      for (let i = 0; i < StackInfo.length; i++) {
        if (StackInfo[i] < this.SVCModels){
          this.data.push({
            type:0, column:this.counter, height:height
          })
          flagKNN = 1
        } else if (StackInfo[i] < this.GausNBModels){
          this.data.push({
            type:1, column:this.counter, height:height
          })
          flagSVC = 1
        } else if (StackInfo[i] < this.MLPModels){
          this.data.push({
            type:2, column:this.counter, height:height
          })
          flagGausNB = 1
        } else if (StackInfo[i] < this.LRModels){
          this.data.push({
            type:3, column:this.counter, height:height
          })
          flagMLP = 1
        } else if (StackInfo[i] < this.LDAModels){
          this.data.push({
            type:4, column:this.counter, height:height
          })
          flagLR = 1
        } else if (StackInfo[i] < this.QDAModels){
          this.data.push({
            type:5, column:this.counter, height:height
          })
          flagLDA = 1
        } else if (StackInfo[i] < this.RFModels){
          this.data.push({
            type:6, column:this.counter, height:height
          })
          flagQDA = 1
        } else if (StackInfo[i] < this.ExtraTModels){
          this.data.push({
            type:7, column:this.counter, height:height
          })
          flagRF = 1
        } else if (StackInfo[i] < this.AdaBModels){
          this.data.push({
            type:8, column:this.counter, height:height
          })
          flagExtraT = 1
        } else if (StackInfo[i] < this.GradBModels){
          this.data.push({
            type:9, column:this.counter, height:height
          })
          flagAdaB = 1
        } else {
          this.data.push({
            type:10, column:this.counter, height:height
          })
          flagGradB = 1
        }
      }

      if (flagKNN == 1) {
        this.typeCounter.push(0)
      }
      if (flagSVC == 1) {
        this.typeCounter.push(0)
      }
      if (flagGausNB == 1) {
        this.typeCounter.push(0)
      }
      if (flagMLP == 1) {
        this.typeCounter.push(0)
      }
      if (flagLR == 1) {
        this.typeCounter.push(0)
      }
      if (flagLDA == 1) {
        this.typeCounter.push(0)
      }
      if (flagQDA == 1) {
        this.typeCounter.push(0)
      }
      if (flagRF == 1) {
        this.typeCounter.push(0)
      }
      if (flagExtraT == 1) {
        this.typeCounter.push(0)
      }
      if (flagAdaB == 1) {
        this.typeCounter.push(0)
      }
      if (flagGradB == 1) {
        this.typeCounter.push(0)
      }
      this.typeColumnCounter.push(0)
      
      this.data.forEach(d => {
        if (d.column == this.counter) {
          d.typeIndex = this.typeCounter[d.type]++;
          d.typeColumnIndex = this.typeColumnCounter[d.column]++;
        }
      });

      // Convert the SVG file to Stardust mark spec.
      let isotype = new Stardust.mark.circle();

      // Create the mark object.
      let isotypes = Stardust.mark.create(isotype, plat);

      let isotypeHeight = 18;
      let colors = [[166,206,227], [31,120,180], [178,223,138], [51,160,44], [251,154,153], [227,26,28], [253,191,111], [255,127,0], [202,178,214], [106,61,154], [255,255,153], [177,89,40]];
      colors = colors.map(x => [x[0] / 255, x[1] / 255, x[2] / 255, 1]);

      let pScale = Stardust.scale.custom(`
              Vector2(
                  20 + column * 100 + typeColumnIndex % 5 * 8,
                  height - 10 - floor(typeColumnIndex / 5) * 10
              )
          `);
      pScale.attr("typeColumnIndex", d => d.typeColumnIndex);
      pScale.attr("column", d => d.column);
      pScale.attr("typeIndex", d => d.typeIndex);
      pScale.attr("type", d => d.type);
      pScale.attr("height", d => d.height);

      let qScale = Stardust.scale.custom(`
              Vector2(
                  65 + typeIndex % 30 * 8,
                  height - 10 - floor(typeIndex / 15) * 18
              )
          `);
      qScale.attr("typeIndex", d => d.typeIndex);
      qScale.attr("type", d => d.type);
      qScale.attr("height", d => d.height);

      let interpolateScale = Stardust.scale.interpolate("Vector2");
      interpolateScale.t(0);

      isotypes.attr("center", interpolateScale(pScale(), qScale()));
      isotypes.attr("radius", 4.0);
      isotypes.attr("color", d => colors[d.type]);

      isotypes.data(this.data);

      EventBus.$emit('ExtractResults', stringParameters)
      isotypes.render();
      this.counter = this.counter + 1

      plat.beginPicking(canvas.width, canvas.height);
      isotypes.attr("radius", 6.0);
      isotypes.render();
      plat.endPicking();
      
      var isDragging = false;
      var draggingLocation = null;
      // Handle dragging.
      canvas.onmousedown = function (e) {
        var x = e.clientX - canvas.getBoundingClientRect().left;
        var y = e.clientY - canvas.getBoundingClientRect().top;
        var p = platform.getPickingPixel(x * platform.pixelRatio, y * platform.pixelRatio);
        if (p) {
          selectedNode = nodes[p[1]];
          requestRender();
          isDragging = true;
          draggingLocation = [selectedNode.x, selectedNode.y];
          var onMove = function (e) {
            var nx = e.clientX - canvas.getBoundingClientRect().left;
            var ny = e.clientY - canvas.getBoundingClientRect().top;
            selectedNode.x = nx;
            selectedNode.y = ny;
            draggingLocation = [nx, ny];
            force.alphaTarget(0.3).restart();
            requestRender();
          };
          var onUp = function () {
            window.removeEventListener("mousemove", onMove);
            window.removeEventListener("mouseup", onUp);
            selectedNode = null;
            draggingLocation = null;
            isDragging = false;
          };
          window.addEventListener("mousemove", onMove);
          window.addEventListener("mouseup", onUp);
        }
      };
      canvas.onmousemove = function (e) {
        if (isDragging) return;
        var x = e.clientX - canvas.getBoundingClientRect().left;
        var y = e.clientY - canvas.getBoundingClientRect().top;
        var p = plat.getPickingPixel(x * plat.pixelRatio, y * plat.pixelRatio);

        var mergedIDs = [].concat.apply([], localStackStore)
        var mergedPerf = [].concat.apply([], localPerfStore)
        var mergedParams = [].concat.apply([], localParamsStore)

        if (p) {

				// Show the tooltip only when there is nodeData found by the mouse
          d3.select('#tooltip')
					.style('opacity', 0.8)
					.style('top', x + 5 + 'px')
					.style('left', y + 5 + 'px')
					.html('Model ID: '+mergedIDs[p[1]]+'<br>'+'Parameters: '+JSON.stringify(mergedParams[p[1]])+'<br> # Performance (%) #: '+mergedPerf[p[1]]);

			} else {

				// Hide the tooltip when there our mouse doesn't find nodeData

				d3.select('#tooltip')
					.style('opacity', 0);

			}
      }
      const stringStep = "Stack "
      var myButton = '<button id="HistoryReturnButtons'+this.counter+'" class="dynamic_buttons">'+stringStep+this.counter+'</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
      $("#dynamic-buttons").append(myButton);

   $(document).on('click','.dynamic_buttons', function() {
      var btns = document.getElementsByClassName('dynamic_buttons')

      btns.forEach(btnlocal => {
        btnlocal.style.fontWeight = 'normal';
      });

      function cleanLoc(obj) {
        var propNames = Object.getOwnPropertyNames(obj);
        for (var i = 0; i < propNames.length; i++) {
          var propName = propNames[i];
          if (obj[propName] === null || obj[propName] === undefined) {
            delete obj[propName];
          }
        }
      }

      var btn = document.getElementById($(this).attr('id'));
      btn.style.fontWeight = 'bold';

      EventBus.$emit('ChangeKey', 0)
      EventBus.$emit('SendSelectedPointsToServerEvent', localStackStore[parseInt($(this).attr('id').replace(/\D/g,''))-1])
      
      stringParameters = []
      temp = 0
      for (let i = 0; i < localStackStore[parseInt($(this).attr('id').replace(/\D/g,''))-1].length; i++) {
        cleanLoc(localPerfStore[parseInt($(this).attr('id').replace(/\D/g,''))-1][i])
        temp = JSON.stringify(Object.assign({ID: localStackStore[parseInt($(this).attr('id').replace(/\D/g,''))-1][i]}, localPerfStore[parseInt($(this).attr('id').replace(/\D/g,''))-1][i]))
        stringParameters.push(temp)
      }
      EventBus.$emit('ExtractResults', stringParameters)

      }
    );
  },
  },
  mounted () {
    EventBus.$on('ParametersProvenance', data => {this.AllDetails = data})
    EventBus.$on('InitializeProvenance', data => {this.stackInformation = data})
    EventBus.$on('InitializeProvenance', this.provenance)
    EventBus.$on('Responsive', data => {
    this.WH = data})
    EventBus.$on('ResponsiveandChange', data => {
    this.WH = data})

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }

}
</script>

<style scoped>
#main-canvas {
  overflow-x: auto;
  overflow-y: auto;
}

div#tooltip {
  position: absolute !important;        
  display: inline-block;
  padding: 10px;
  font-family: 'Open Sans' sans-serif;
  color: #000;
  background-color: #fff;
  border: 1px solid #999;
  border-radius: 2px;
  pointer-events: none;
  opacity: 0;
  z-index: 1;
}

</style>