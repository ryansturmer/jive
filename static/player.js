jQuery.extend({
       postJSON: function( url, data, callback) {
          return jQuery.post(url, data, callback, "json");
       }
});

// Play COntrols in the header
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
function duration(s) {
    a = Math.floor(s/60);
    b = s % 60;
    if(isNaN(a) || isNaN(b)) {
        return "";
    }
    else {
        return a + ":" + b;
    }
}
function playlist_update() {
    window.location.reload();
}
setInterval(status_update, 1000);
