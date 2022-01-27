$(document).ready(function () {
    $(".dws-progress-bar").circularProgress({
        color: "#2af7eb",
        line_width: 20,
        height: "350px",
        width: "350px",
        percent: 0,
        counter_clockwise: false,
        starting_position: 50
    }).circularProgress('animate', 100, 1800);
});

$(window).on('load', function () {
    var $preloader = $('#preloader');
    $preloader.delay(2000).fadeOut('slow');
});