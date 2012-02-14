$('#play_button').click(function(event) {
    $.post('/play');
});
$('#stop_button').click(function(event) {
    $.post('/stop');
});
$('#prev_button').click(function(event) {
    $.post('/prev');
});
$('#next_button').click(function(event) {
    $.post('/next');
});
