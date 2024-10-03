/*jshint strict:false */
/*jshint esversion: 8 */
/*global console*/

document.getElementById("top-logo").addEventListener("click", function() {
    window.location.href="index.html";
});

document.getElementById("click-here").addEventListener("click", function() {
    console.log("hello");
    window.location.href="create-account.html";
});

document.getElementById("login-button").addEventListener("click", function() {
    window.location.href="create-schedule.html";
});