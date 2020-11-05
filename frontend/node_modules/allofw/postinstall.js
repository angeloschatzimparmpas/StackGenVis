console.log("Downloading allofw prebuilt binaries...");

var info = {
    "darwin": {
        "x64": [
            "https://donghaoren.github.io/Allofw/binaries/v0.1.0/darwin_x64.tar.gz",
            "d867c34c80e72c6633afcd0f7ba340fdbdf6507b6fcf478afb09881dfbd05b1e"
        ]
    },
    "win32": {
        "x64": [
            "https://donghaoren.github.io/Allofw/binaries/v0.1.0/win32_x64.tar.gz",
            "3eefe6d0c12e5b5804f987f069cee2705cba5267813f40a91622d83719b1a9e1"
        ]
    },
    "linux": {
        "x64": [
            "https://donghaoren.github.io/Allofw/binaries/v0.1.0/linux_x64.tar.gz",
            "a2fa45943b88c1d11d72abddc51290beff4573969ec8572b57a59764934ff75b"
        ]
    }
};

var os = require('os');
var crypto = require('crypto');
var https = require('https');
var fs = require('fs');
var tar = require('tar');

function downloadAndVerify(url, sha256) {
    return new Promise(function (resolve, reject) {
        console.log("Downloading " + url + "...");
        var reader = https.get(url, function (response) {
            if (response.statusCode == 200) {
                var buffers = [];
                var sizeReceived = 0;
                response.setEncoding("binary");
                var size = parseInt(response.headers["content-length"]);
                response.on("data", function (buffer) {
                    buffer = new Buffer(buffer, "binary");
                    buffers.push(buffer);
                    sizeReceived += buffer.length;
                });
                response.on("end", function (buffer) {
                    var result = Buffer.concat(buffers);
                    var hash = crypto.createHash("sha256");
                    hash.update(result);
                    var digest = hash.digest("hex");
                    if (digest != sha256) {
                        reject(new Error("checksum error"));
                    }
                    resolve(result);
                });
                response.on("error", function () {
                    reject(new Error("cannot get from " + url));
                });
            } else {
                reject(new Error("cannot get from " + url));
            }
        });
    });
}

var platform = os.platform();
if (platform == "darwin") {
    downloadAndVerify(info.darwin.x64[0], info.darwin.x64[1]).then(function (data) {
        var x = tar.x();
        x.write(data);
        x.end();
    });
}
if (platform == "win32") {
    downloadAndVerify(info.win32.x64[0], info.darwin.x64[1]).then(function (data) {
        var x = tar.x();
        x.write(data);
        x.end();
    });
}
if (platform == "linux") {
    downloadAndVerify(info.linux.x64[0], info.darwin.x64[1]).then(function (data) {
        var x = tar.x();
        x.write(data);
        x.end();
    });
}
