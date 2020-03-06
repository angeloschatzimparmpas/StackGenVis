<template>
    <div>
        <div class="squares-container" style="min-height: 374px;">
        <div id="tooltip"></div>	<!-- new  -->
          <div id="performanceCapture" style="min-height: 150px; margin-top: -10px !important;"></div>	<!-- new  -->
          <canvas id="main-canvas" style="overflow-y: auto; overflow-x: auto; height:190px;"></canvas>
          <br>
          <div id="dynamic-buttons"></div>
        </div>
    </div>
</template>

<script>
import { EventBus } from '../main.js'
import $ from 'jquery'
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3v5 = Object.assign(d3Base)

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
      storeParameters: [],
      flagUpdated: 0,
      FinalResultsProv: [],
      Stack_scoresMean: [],
      Stack_scoresMean2: [],
      Stack_scoresMean3: [],
      Stack_scoresMean4: [],
      firstInside: 0
    }
  },
  methods: {
    reset () {
      if (this.platform == '') {

      } else {
        $('.dynamic_buttons').remove();
        this.platform.clear();
        var svg = d3.select("#performanceCapture");
        svg.selectAll("*").remove();
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
      var width = this.WH[0]*6.52 // interactive visualization
      var height = this.WH[1]*0.375 // interactive visualization

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
      let colors = [[166,206,227], [31,120,180], [178,223,138], [51,160,44], [251,154,153], [227,26,28], [253,191,111], [255,127,0], [202,178,214], [106,61,154], [177,89,40]];
      colors = colors.map(x => [x[0] / 255, x[1] / 255, x[2] / 255, 1]);
      // here 10 was 5!
      let pScale = Stardust.scale.custom(`
              Vector2(
                  20 + column * 195 + typeColumnIndex % 12 * 11.7,
                  height - 10 - floor(typeColumnIndex / 12) * 10
              )
          `);
      pScale.attr("typeColumnIndex", d => d.typeColumnIndex);
      pScale.attr("column", d => d.column);
      pScale.attr("typeIndex", d => d.typeIndex);
      pScale.attr("type", d => d.type);
      pScale.attr("height", d => d.height);

      let qScale = Stardust.scale.custom(`
              Vector2(
                  60 + typeIndex % 30 * 8,
                  height - 10 - floor(typeIndex / 15) * 40
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
					.html('Model ID: '+mergedIDs[p[1]]+'<br>'+'Parameters: '+JSON.stringify(mergedParams[p[1]])+'<br> # Performance (%) #: '+mergedPerf[p[1]].toFixed(2));

			} else {

				// Hide the tooltip when there our mouse doesn't find nodeData

				d3.select('#tooltip')
					.style('opacity', 0);

			}
      }
      const stringStep = "Stacking Ensemble "
      var myButton = '<button id="HistoryReturnButtons'+this.counter+'" class="dynamic_buttons">'+stringStep+this.counter+'</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
      $("#dynamic-buttons").append(myButton);

      EventBus.$emit('requestProven',this.counter-1)

      var btns = document.getElementsByClassName('dynamic_buttons')

      btns.forEach(btnlocal => {
        btnlocal.style.fontWeight = 'normal';
      });

       $(document).on('click','.dynamic_buttons', function() {
        var btns = document.getElementsByClassName('dynamic_buttons')

        btns.forEach(btnlocal => {
          btnlocal.style.fontWeight = 'normal';
        });

        var btn = document.getElementById($(this).attr('id'));
        btn.style.fontWeight = 'bold';


        EventBus.$emit('requestProven',parseInt($(this).attr('id').replace(/\D/g,''))-1)
        EventBus.$emit('ChangeKey', 0)
        }
      );
  },
  RadialPerf () {
    this.firstInside++
    var svgs = '<svg id=svg'+this.firstInside+'></svg>'
    $("#performanceCapture").append(svgs);

    var width = 160;
    var arcSize = (6 * width / 100);
    var innerRadius = arcSize * 3;

    this.Stack_scoresMean = []
    this.Stack_scoresMean2 = []
    this.Stack_scoresMean3 = []
    this.Stack_scoresMean4 = []

    this.Stack_scoresMean.push((JSON.parse(this.FinalResultsProv[0])*100).toFixed(0))
    this.Stack_scoresMean2.push((JSON.parse(this.FinalResultsProv[2])*100).toFixed(0))
    this.Stack_scoresMean3.push((JSON.parse(this.FinalResultsProv[4])*100).toFixed(0))
    this.Stack_scoresMean4.push((JSON.parse(this.FinalResultsProv[6])*100).toFixed(0))

    const colorsSingle = ['#fc9272','#fb6a4a','#ef3b2c','#cb181d','#a50f15','#67000d']

    var scaleColor = d3v5.scaleLinear()
      .domain([0,100,5])
      .range(colorsSingle)
      .interpolate(d3v5.interpolateRgb); //interpolateHsl interpolateHcl interpolateRgb;

    var data = [
      {value: this.Stack_scoresMean, label: "Accuracy", color: scaleColor(this.Stack_scoresMean)},
      {value: this.Stack_scoresMean2, label: "Precision", color: scaleColor(this.Stack_scoresMean2)},
      {value: this.Stack_scoresMean3, label: "Recall", color: scaleColor(this.Stack_scoresMean3)},
      {value: this.Stack_scoresMean4, label: "F1 Score", color: scaleColor(this.Stack_scoresMean4)}
    ];

    var svg = d3.select('#svg'+this.firstInside).attr('width', width).attr('height', width).style('margin-right', '25px');

    var arcs = data.map(function (obj, i) {
        return d3.svg.arc().innerRadius(i * arcSize + innerRadius).outerRadius((i + 1) * arcSize - (width / 100) + innerRadius);
    });
    var arcsGrey = data.map(function (obj, i) {
        return d3.svg.arc().innerRadius(i * arcSize + (innerRadius + ((arcSize / 2) - 2))).outerRadius((i + 1) * arcSize - ((arcSize / 2)) + (innerRadius));
    });

    var pieData = data.map(function (obj, i) {
        return [
            {value: obj.value * 0.75, arc: arcs[i], object: obj},
            {value: (100 - obj.value) * 0.75, arc: arcsGrey[i], object: obj},
            {value: 100 * 0.25, arc: arcs[i], object: obj}];
    });

    var pie = d3.layout.pie().sort(null).value(function (d) {
        return d.value;
    });

    var g = svg.selectAll('g').data(pieData).enter()
        .append('g')
        .attr('transform', 'translate(' + width / 2 + ',' + width / 2 + ') rotate(180)');
    var gText = svg.selectAll('g.textClass').data([{}]).enter()
        .append('g')
        .classed('textClass', true)
        .attr('transform', 'translate(' + width / 2 + ',' + width / 2 + ') rotate(180)');


    g.selectAll('path').data(function (d) {
        return pie(d);
    }).enter().append('path')
        .attr('id', function (d, i) {
            if (i == 1) {
                return "Text" + d.data.object.label
            }
        })
        .attr('d', function (d) {
            return d.data.arc(d);
        }).attr('fill', function (d, i) {
        return i == 0 ? d.data.object.color : i == 1 ? '#D3D3D3' : 'none';
    });

    svg.selectAll('g').each(function (d, index) {
        var el = d3.select(this);
        var path = el.selectAll('path').each(function (r, i) {
            if (i === 1) {
                var centroid = r.data.arc.centroid({
                    startAngle: r.startAngle + 0.05,
                    endAngle: r.startAngle + 0.001 + 0.05
                });
                var lableObj = r.data.object;
                g.append('text')
                    .attr('font-size', ((5 * width) / 100) + 2)
                    .attr('dominant-baseline', 'central')
                    /*.attr('transform', "translate(" + centroid[0] + "," + (centroid[1] + 10) + ") rotate(" + (180 / Math.PI * r.startAngle + 7) + ")")
                      .attr('alignment-baseline', 'middle')*/
                    .append("textPath")
                    .attr("textLength", function (d, i) {
                        return 0;
                    })
                    .attr("xlink:href", "#Text" + r.data.object.label)
                    .attr("startOffset", '5')
                    .attr("dy", '-3em')
                    .text(lableObj.value + '%');
            }
            if (i === 0) {
                var centroidText = r.data.arc.centroid({
                    startAngle: r.startAngle,
                    endAngle: r.startAngle
                });
                var lableObj = r.data.object;
                gText.append('text')
                    .attr('font-size', ((5 * width) / 100) + 2)
                    .text(lableObj.label)
                    .attr('transform', "translate(" + (centroidText[0] - ((1.5 * width) / 100)) + "," + (centroidText[1] + ") rotate(" + (180) + ")"))
                    .attr('dominant-baseline', 'central');
            }
        });
    });
  },
  updateExtraction () {
    EventBus.$emit('SendSelectedPointsToServerEvent', this.storeData[this.flagUpdated])
    
    var stringParameters = []
    var temp = 0
    for (let i = 0; i < this.storeData[this.flagUpdated].length; i++) {
      this.clean(this.storeData[this.flagUpdated][i])
      temp = JSON.stringify(Object.assign({ID: this.storeData[this.flagUpdated][i]}, this.storeParameters[this.flagUpdated][i]))
      stringParameters.push(temp)
    }
    EventBus.$emit('ExtractResults', stringParameters)
  }
  },
  mounted () {
    EventBus.$on('emittedEventCallingLinePlot', data => {
    this.FinalResultsProv = data})
    EventBus.$on('emittedEventCallingReally', this.RadialPerf)

    EventBus.$on('requestProven', data => {
    this.flagUpdated = data})
    EventBus.$on('requestProven', this.updateExtraction)

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