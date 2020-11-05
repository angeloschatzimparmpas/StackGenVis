var os = require('os');

var platform = os.platform();

if(platform == "darwin") {
    if(process.version.match(/^v6.*/)) {
        module.exports = require("./darwin_x64/allofw.v6.node");
    }
    if(process.version.match(/^v7.*/)) {
        module.exports = require("./darwin_x64/allofw.v7.node");
    }
    if(process.version.match(/^v8.*/)) {
        module.exports = require("./darwin_x64/allofw.v8.node");
    }
    if(process.version.match(/^v9.*/)) {
        module.exports = require("./darwin_x64/allofw.v9.node");
    }
}
if(platform == "win32") {
    module.exports = require("./win32_x64/allofw.node");
    module.exports.OpenVR = require("./win32_x64/allofw_openvr.node");
}
if(platform == "linux") {
    module.exports = require("./linux_x64/allofw.node");
}
