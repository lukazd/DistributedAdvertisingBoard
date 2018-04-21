"use strict";


const sense = require("sense-hat-led").sync;

//IMU Sensor Code
var util = require('util')
var nodeimu  = require('nodeimu');
var IMU = new nodeimu.IMU();

console.time("sync");

function getIMUData() {
  var tic = new Date();
  var data = IMU.getValueSync();
  var toc = new Date();

  var str = data.timestamp.toISOString() + " ";
    console.log(data.temperature);
    console.log(data.humidity);
    console.log(data.pressure);
  var str2 = "";
	return { temp: data.temperature.toFixed(4),
		pressure: data.pressure.toFixed(4),
		humidity: data.humidity.toFixed(4) };
  }
  
}



//MAIN METHOD
getIMUData();
setInterval(function() {
    getIMUData();
}, 6000)
