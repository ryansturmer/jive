jQuery.extend({
       postJSON: function( url, data, callback) {
          return jQuery.post(url, data, callback, "json");
       }
});

$('.mpd_play_button').click(function(event) {
    $.post('/play');
});
$('.mpd_stop_button').click(function(event) {
    $.post('/stop');
});
$('.mpd_previous_button').click(function(event) {
    $.post('/prev');
});
$('.mpd_next_button').click(function(event) {
    $.post('/next');
});

playlist = 0;
search_results = 0;
title = 0;

function show_page(page) {
    $('.mpd_page').hide();
    $(page).show();
}

function status_update() {
    $.getJSON('/status', null, function(json) {
        $('#volume').slider('value', json.volume)})
}

function playlist_update() {
    $.getJSON('/playlist', null, function(json) {
        $('.mpd_playlist_item').remove();
        playlist = json;
        for(song in json) {
            song = json[song]
            new_row = $('#mpd_playlist_row_template').clone()
            new_row.addClass('mpd_playlist_item')
            $('.mpd_title', new_row).text(song.title)
            $('.mpd_artist', new_row).text(song.artist)
            new_row.show()
            $('#mpd_playlist').append(new_row);
        }
    });
}

// init stuff
$("#songpos").slider({min:0, max:100});
playlist_update();

//setInterval(status_update, 100);
