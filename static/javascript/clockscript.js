// Doomsday
var countDownDate = new Date("Jan 1, 2028").getTime();

// Update every second
var x = setInterval(function() {

    // Get today's date and time
    var now = new Date().getTime();
    
    // Find the distance between now and the count down date
    var distance = countDownDate - now;
    
    // Time calculations for years, days, hours, minutes and seconds (2 integer places)
    var days = Math.floor((distance / (1000 * 60 * 60 * 24)) % 365.25 );
    var years = Math.floor(distance / (1000 * 60 * 60 * 24 * 365.25));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});
    var seconds = Math.floor((distance % (1000 * 60)) / 1000).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});
    
    // Output result
    document.getElementById("clock").innerHTML = years + "y " + days + "d " + hours + ":" + minutes + ":" + seconds;
}, 1000);