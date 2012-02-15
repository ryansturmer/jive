jQuery.extend({
       postJSON: function( url, data, callback) {
          return jQuery.post(url, data, callback, "json");
       }
});

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
playlist = 0;
title = 0;
$('#db_search').submit(function(event) {
    event.preventDefault();
    $.postJSON('/db_search', $('#db_search').serialize(), function(json) {
        $('#songs tr').remove();
        playlist = json;
        for(song in json) {
            song = json[song]
            row = document.createElement('tr');
            td = document.createElement('td');
            td.appendChild(document.createTextNode(song.title));
            row.appendChild(td)
            
            td = document.createElement('td');
            td.appendChild(document.createTextNode(song.artist));
            row.appendChild(td)
            $('#songs').append(row);
        }
    });
    //$.post('/search_db', $('#db_search').serialize(), function(data) {
  //      refresh();
   // });
});
