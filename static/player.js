jQuery.extend({
       postJSON: function( url, data, callback) {
          return jQuery.post(url, data, callback, "json");
       }
});
function mpd_play() {
    $.post('/play');
}
function mpd_stop() {
    $.post('/stop');
}
function mpd_previous() {
    $.post('prev');
}
function mpd_next() {
    $.post('/next');
}
function mpd_pause() {
    $.post('/pause');
}

// Play Controls in the header
$('.mpd_play_button').click(function(event) {
    mpd_play();
});
$('.mpd_stop_button').click(function(event) {
    mpd_stop();
});
$('.mpd_previous_button').click(function(event) {
    mpd_previous();
});
$('.mpd_next_button').click(function(event) {
    mpd_next();
});
$('.mpd_pause_button').click(function(event) {
    mpd_pause();
});

volume_slider = $('#mpd_header_volume');
volume_slider.slider({
    orientation:'horizontal', 
    min:0, 
    max:100,
    stop: function(event, ui) {
        $.post('/setvol', {'volume':ui.value});
    }
});

$('#mpd_clear_playlist').click(function(event) {
    $.post('/clear_playlist', null, playlist_update);
});

$('#mpd_shuffle_playlist').click(function(event) {
    $.post('/shuffle', null, playlist_update);
});

playlist = 0;
search_results = 0;
title = 0;
current_song_id = null;

function load_playlist(list) {
    $.post('/load_playlist', {'playlist':list});
}
function status_update(callback) {
    $.getJSON('/status', null, function(json) {
        $('#mpd_header_playlist').text('Now Playing (' + json.playlistlength + ')');
        $('#mpd_header_volume').slider('value', json.volume);
        
        
        $('#mpd_seek_slider').slider('option', {
            'max': json.duration,
            'value': json.time
        });
        if(callback) {
            callback(json);
        }
    });
}

function now_playing_update() {
    $.getJSON('/now_playing', null, function(json) {
        if(json.title) {
        $('#mpd_np_title').text(json.title);
        $('#mpd_np_artist').text(json.artist);
        document.title = json.title + " - Jive";
        }
        else {    
        $('#mpd_np_title').text('Stopped');
        $('#mpd_np_artist').text('Click play to continue');
        document.title = "Jive - Stopped";
        }
        playing_row = "song_" + json.pos
        $('tr[id!="' + playing_row + '"]').removeClass('row_hilite');
        $('#' + playing_row).addClass('row_hilite');
    });
}

function playlist_update() {
    window.location.reload();
}
