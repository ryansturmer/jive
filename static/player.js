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

$('#db_search').submit(function(event) {
    event.preventDefault();
    $.post('/search_db', $('#db_search').serialize(), function(data) {
        refresh();
    });
});
