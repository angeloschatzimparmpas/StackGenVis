<template>
    <div id="chart"></div>      
</template>

<script>
import * as d3Base from 'd3'
import { loom, string } from 'd3-loom'
import { EventBus } from '../main.js'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base, { loom, string })

export default {
  name: "StretchedChord",
  data () {
    return {
      AllResults: '',
    }
  },
  methods: {
      StretchChord () {
        const FeatureImportance = JSON.parse(this.AllResults[3])
        const ClassNames = JSON.parse(this.AllResults[5])    

        var SortFeaturesPerClass = []
        FeatureImportance.forEach(classifier => {
            for (let i = 0; i < length; i++) {
                SortFeaturesPerClass.push(this.sortObject(classifier[i]))
            }
        })

        var margin = {left:80, top:40, right:120, bottom:50},
            width = Math.max( Math.min(window.innerWidth, 1100) - margin.left - margin.right - 20, 400),
            height = Math.max( Math.min(window.innerHeight - 250, 900) - margin.top - margin.bottom - 20, 400),
            innerRadius = Math.min(width * 0.33, height * .45),
            outerRadius = innerRadius * 1.05;
            
            //Recalculate the width and height now that we know the radius
            width = outerRadius * 2 + margin.right + margin.left;
            height = outerRadius * 2 + margin.top + margin.bottom;
                
            //Reset the overall font size
            var newFontSize = Math.min(70, Math.max(40, innerRadius * 62.5 / 250));
            d3.select("html").style("font-size", newFontSize + "%");

            ////////////////////////////////////////////////////////////
            ////////////////// Set-up Chord parameters /////////////////
            ////////////////////////////////////////////////////////////
                
            var pullOutSize = 20 + 30/135 * innerRadius;
            var numFormat = d3.format(",.0f");
            var defaultOpacity = 0.85,
                fadeOpacity = 0.075;
                                    
            var loom = d3.loom()
                .padAngle(0.05)
                //.sortSubgroups(sortAlpha)
                //.heightInner(28)
                .emptyPerc(0.2)
                .widthInner(30)
                //.widthInner(function(d) { return 6 * d.length; })
                .value(function(d) { return d.words; })
                .inner(function(d) { return d.character; })
                .outer(function(d) { return d.location; });

            var arc = d3.arc()
                .innerRadius(innerRadius*1.01)
                .outerRadius(outerRadius);

            var string = d3.string()
                .radius(innerRadius)
                .pullout(pullOutSize);
                
            var characterNotes = [];

            characterNotes["Iris Setosa"] = "Speaking almost twice as many words as the second most abundant speaker, Gandalf is taking up a large portion of dialogue in almost every location he's in, but stays rather quiet in Mordor";
            characterNotes["Iris Versicolour"] = "An unexpected runner up to having spoken the most words, Sam flourishes after the battle at Amon Hen, taking up a considerable portion of the words said in both Mordor and Gondor";
            characterNotes["Iris Virginica"] = "Although eventually being crowned in Minas Tirith, Gondor, Aragorn is by far most talkative in that other human region, Rohan, fighting a battle at Helm's Deep and convincing an army of dead";

            ////////////////////////////////////////////////////////////
            ////////////////////// Create SVG //////////////////////////
            ////////////////////////////////////////////////////////////
                        
            var svg = d3.select("#chart").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);

            ////////////////////////////////////////////////////////////
            ///////////////////// Read in data /////////////////////////
            ////////////////////////////////////////////////////////////
                        

                ////////////////////////////////////////////////////////////
                ///////////////////// Prepare the data /////////////////////
                ////////////////////////////////////////////////////////////
                
                //Sort the inner characters based on the total number of words spoken
                var dataAgg = [
            {
                "location": "Classifier 1",
                "character": "Iris Setosa",
                "words": 94
            },
            {
                "location": "Classifier 1",
                "character": "Iris Versicolour",
                "words": 100
            },
            {
                "location": "Classifier 1",
                "character": "Iris Virginica",
                "words": 100
            },
            {
                "location": "Feature 1",
                "character": "Iris Virginica",
                "words": 40
            },
            {
                "location": "Feature 2",
                "character": "Iris Virginica",
                "words": 60
            },
            ]			
            //Find the total number of words per character
            var dataChar = d3.nest()
                .key(function(d) { return d.character; })
                .rollup(function(leaves) { return d3.sum(leaves, function(d) { return d.words; }); })
                .entries(dataAgg)
                .sort(function(a, b){ return d3.descending(a.value, b.value); });				
            //Unflatten the result
            var characterOrder = dataChar.map(function(d) { return d.key })
            //Sort the characters on a specific order
            function sortCharacter(a, b) {
                return characterOrder.indexOf(a) - characterOrder.indexOf(b)
            }//sortCharacter
            
            //Set more loom functions
            loom
                .sortSubgroups(sortCharacter)
                .heightInner(innerRadius*0.75/characterOrder.length)
            
            ////////////////////////////////////////////////////////////
            ///////////////////////// Colors ///////////////////////////
            ////////////////////////////////////////////////////////////
                            
            var locations = ["Iris Setosa", "Iris Versicolour", "Iris Virginica"]
            var colors = ["#5a3511", "#47635f", "#223e15"]
            var color = d3.scaleOrdinal()
                .domain(locations)
                .range(colors)
            
            //Create a group that already holds the data
            var g = svg.append("g")
                .attr("transform", "translate(" + (width/2 + margin.left) + "," + (height/2 + margin.top) + ")")
                .datum(loom(dataAgg))	

            ////////////////////////////////////////////////////////////
            ///////////////////// Set-up title /////////////////////////
            ////////////////////////////////////////////////////////////

            var titles = g.append("g")
                .attr("class", "texts")
                .style("opacity", 0)
                
            titles.append("text")
                .attr("class", "name-title")
                .attr("x", 0)
                .attr("y", -innerRadius*5/6)
                
            titles.append("text")
                .attr("class", "value-title")
                .attr("x", 0)
                .attr("y", -innerRadius*5/6 + 25)
            
            //The character pieces	
            titles.append("text")
                .attr("class", "character-note")
                .attr("x", 0)
                .attr("y", innerRadius/2)
                .attr("dy", "0.35em")
                            
            ////////////////////////////////////////////////////////////
            ////////////////////// Draw outer arcs /////////////////////
            ////////////////////////////////////////////////////////////

            var arcs = g.append("g")
                .attr("class", "arcs")
            .selectAll("g")
                .data(function(s) { 
                    return s.groups 
                })
            .enter().append("g")
                .attr("class", "arc-wrapper")
                .each(function(d) { 
                    d.pullOutSize = (pullOutSize * ( d.startAngle > Math.PI + 1e-2 ? -1 : 1)) 
                })
                .on("mouseover", function(d) {
                    
                    //Hide all other arcs	
                    d3.selectAll(".arc-wrapper")
                        .transition()
                        .style("opacity", function(s) { return s.outername === d.outername ? 1 : 0.5 })
                    
                    //Hide all other strings
                    d3.selectAll(".string")
                        .transition()
                        .style("opacity", function(s) { return s.outer.outername === d.outername ? 1 : fadeOpacity })
                        
                    //Find the data for the strings of the hovered over location
                    var locationData = loom(dataAgg).filter(function(s) { return s.outer.outername === d.outername })
                    //Hide the characters who haven't said a word
                    d3.selectAll(".inner-label")
                        .transition()
                        .style("opacity", function(s) {
                            //Find out how many words the character said at the hovered over location
                            var char = locationData.filter(function(c) { return c.outer.innername === s.name })
                            return char.length === 0 ? 0.1 : 1
                        })
                })
                .on("mouseout", function(d) {
                    
                    //Sjow all arc labels
                    d3.selectAll(".arc-wrapper")
                        .transition()
                        .style("opacity", 1)
                    
                    //Show all strings again
                    d3.selectAll(".string")
                        .transition()
                        .style("opacity", defaultOpacity)
                        
                    //Show all characters again
                    d3.selectAll(".inner-label")
                        .transition()
                        .style("opacity", 1)
                })

            var outerArcs = arcs.append("path")
                .attr("class", "arc")
                .style("fill", function(d) { return color(d.innername) })
                .attr("d", arc)
                .attr("transform", function(d, i) { //Pull the two slices apart
                    return "translate(" + d.pullOutSize + ',' + 0 + ")"
                })
                                    
            ////////////////////////////////////////////////////////////
            //////////////////// Draw outer labels /////////////////////
            ////////////////////////////////////////////////////////////

            //The text needs to be rotated with the offset in the clockwise direction
            var outerLabels = arcs.append("g")
                .each(function(d) { d.angle = ((d.startAngle + d.endAngle) / 2) })
                .attr("class", "outer-labels")
                .attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null })
                .attr("transform", function(d,i) { 
                    var c = arc.centroid(d)
                    return "translate(" + (c[0] + d.pullOutSize) + "," + c[1] + ")"
                    + "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
                    + "translate(" + 26 + ",0)"
                    + (d.angle > Math.PI ? "rotate(180)" : "")
                })
                
            //The outer name
            outerLabels.append("text")
                .attr("class", "outer-label")
                .attr("dy", ".35em")
                .text(function(d,i){ return d.outername })
                
            //The value below it
            outerLabels.append("text")
                .attr("class", "outer-label-value")
                .attr("dy", "1.5em")
                .text(function(d,i){ return numFormat(d.value) + " words" })

            ////////////////////////////////////////////////////////////
            ////////////////// Draw inner strings //////////////////////
            ////////////////////////////////////////////////////////////
            
            var strings = g.append("g")
                .attr("class", "stringWrapper")
                .style("isolation", "isolate")
            .selectAll("path")
                .data(function(strings) { 
                    return strings 
                })
            .enter().append("path")
                .attr("class", "string")
                .style("mix-blend-mode", "multiply")
                .attr("d", string)
                .style("fill", function(d) { return d3.rgb( color(d.outer.innername) ).brighter(0.2)  })
                .style("opacity", defaultOpacity)
                
            ////////////////////////////////////////////////////////////
            //////////////////// Draw inner labels /////////////////////
            ////////////////////////////////////////////////////////////
                    
            //The text also needs to be displaced in the horizontal directions
            //And also rotated with the offset in the clockwise direction
            var innerLabels = g.append("g")
                .attr("class","inner-labels")
            .selectAll("text")
                .data(function(s) { 
                    return s.innergroups 
                })
            .enter().append("text")
                .attr("class", "inner-label")
                .attr("x", function(d,i) { return d.x })
                .attr("y", function(d,i) { return d.y })
                .style("text-anchor", "middle")
                .attr("dy", ".35em")
                .text(function(d,i) { return d.name })
                .on("mouseover", function(d) {
                    
                    //Show all the strings of the highlighted character and hide all else
                    d3.selectAll(".string")
                        .transition()
                        .style("opacity", function(s) {
                            return s.outer.innername !== d.name ? fadeOpacity : 1
                        })
                        
                    //Update the word count of the outer labels
                    var characterData = loom(dataAgg).filter(function(s) { return s.outer.innername === d.name })
                    d3.selectAll(".outer-label-value")
                        .text(function(s,i){
                            //Find which characterData is the correct one based on location
                            var loc = characterData.filter(function(c) { return c.outer.outername === s.outername })
                            if(loc.length === 0) {
                                var value = 0
                            } else {
                                var value = loc[0].outer.value
                            }
                            return numFormat(value) + (value === 1 ? " word" : " words") 
                            
                        })
                    
                    //Hide the arc where the character hasn't said a thing
                    d3.selectAll(".arc-wrapper")
                        .transition()
                        .style("opacity", function(s) {
                            //Find which characterData is the correct one based on location
                            var loc = characterData.filter(function(c) { return c.outer.outername === s.outername })
                            return loc.length === 0 ? 0.1 : 1
                        })
                            
                    //Update the title to show the total word count of the character
                    d3.selectAll(".texts")
                        .transition()
                        .style("opacity", 1)	
                    d3.select(".name-title")
                        .text(d.name)
                    d3.select(".value-title")
                        .text(function() {
                            var words = dataChar.filter(function(s) { return s.key === d.name })
                            return numFormat(words[0].value)
                        })
                        
                    //Show the character note
                    d3.selectAll(".character-note")
                        .text(characterNotes[d.name])
                        .call(wrap, 2.25*pullOutSize)
                        
                })
                .on("mouseout", function(d) {
                    
                    //Put the string opacity back to normal
                    d3.selectAll(".string")
                        .transition()
                        .style("opacity", defaultOpacity)
                        
                    //Return the word count to what it was
                    d3.selectAll(".outer-label-value")	
                        .text(function(s,i){ return numFormat(s.value) + " words" })
                        
                    //Show all arcs again
                    d3.selectAll(".arc-wrapper")
                        .transition()
                        .style("opacity", 1)
                    
                    //Hide the title
                    d3.selectAll(".texts")
                        .transition()
                        .style("opacity", 0)
                    
                })

        ////////////////////////////////////////////////////////////
        ///////////////////// Extra functions //////////////////////
        ////////////////////////////////////////////////////////////

        //Sort alphabetically
        function sortAlpha(a, b){
                if(a < b) return -1
                if(a > b) return 1
                return 0
        }//sortAlpha

        //Sort on the number of words
        function sortWords(a, b){
                if(a.words < b.words) return -1
                if(a.words > b.words) return 1
                return 0
        }//sortWords

        /*Taken from http://bl.ocks.org/mbostock/7555321
        //Wraps SVG text*/
        function wrap(text, width) {
        text.each(function() {
            var text = d3.select(this),
                words = text.text().split(/\s+/).reverse(),
                word,
                line = [],
                lineNumber = 0,
                lineHeight = 1.2, // ems
                y = parseFloat(text.attr("y")),
                x = parseFloat(text.attr("x")),
                dy = parseFloat(text.attr("dy")),
                tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em")

            while (word = words.pop()) {
            line.push(word)
            tspan.text(line.join(" "))
            if (tspan.node().getComputedTextLength() > width) {
                line.pop()
                tspan.text(line.join(" "))
                line = [word]
                tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word)
            }
            }
        })
        }//wrap
        },
        sortObject (obj) {
            var arr = []
            for (var prop in obj) {
                if (Object.prototype.hasOwnProperty.call(obj, prop)) {
                    if ((this.LimitFeatureImportance/100) < Math.abs(obj[prop])) {
                        arr.push({
                        'FeatureID': prop,
                        'ImportanceValue': obj[prop]
                        })
                    }
                }
            }
            arr = arr.sort(function (a, b) { return Math.abs(b.ImportanceValue) - Math.abs(a.ImportanceValue) })
            return arr
        },
        ObjectSize (obj) {
            let size = 0
            let key
            for (key in obj) {
                if (Object.prototype.hasOwnProperty.call(obj, key)) size++
            }
            return size
        }                  
    },
    mounted () {
        EventBus.$on('emittedEventCallingChordView', data => { this.AllResults = data })
        EventBus.$on('emittedEventCallingChordView', this.StretchChord)
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
html { font-size: 62.5%; } 

body {
font-family: 'Cormorant', serif;
font-size: 1.2rem;
fill: #b9b9b9;
}

.lotr-content-wrapper {
max-width: 900px;
margin: 0 auto;
}

#lotr-title {
font-size: 42px;
font-weight: 300;
margin: 40px 30px 0px 30px;
color: #272727;
}

#lotr-subtitle {
font-size: 14px;
color: #b1b1b1;
margin: 0px 30px 20px 30px;
font-weight: 300;
}

#lotr-intro {
font-size: 16px;
margin: 0px 30px 10px 30px;
max-width: 800px;
}

#lotr-note {
font-size: 14px;
margin: 0px 30px 10px 30px;
max-width: 800px;
color: #b1b1b1;
font-weight: 300;
}

#chart {
text-align: center;
}

#lotr-credit {
font-size: 14px;
margin: 10px 30px 5px 30px;
}

#lotr-sources {
font-size: 11px;
max-width: 300px;
margin: 15px 30px 5px 30px;
color: #9e9e9e;
font-weight: 300;
padding-bottom: 20px;
}

a:hover {
text-decoration: none;
border-bottom: 1px solid black;
}

a, a:link, a:visited, a:active {
text-decoration: none;
color: black;
border-bottom: 1px dotted rgba(0, 0, 0, .5);
}

.MiddleEarth {
font-family: 'Macondo', cursive;
color: #53821a;
}

/*--- chart ---*/

.name-title {
font-family: 'Macondo Swash Caps', cursive;
font-size: 2.8rem;
fill: #232323;
cursor: default;
text-anchor: middle;
}

.value-title {
text-anchor: middle;
font-size: 1.8rem;
fill: #b9b9b9;
}

.character-note {
text-anchor: middle;
font-size: 1.4rem;
fill: #232323;
}
			
.inner-label {
font-family: 'Macondo Swash Caps', cursive;
font-size: 1.4rem;
fill: #232323;
cursor: default;
}

.outer-label {
font-family: 'Macondo', cursive;
font-size: 1.6rem;
fill: #5f5f5f;
cursor: default;
}

.outer-label-value {
font-size: 1.2rem;
fill: #b9b9b9;
}

</style>
