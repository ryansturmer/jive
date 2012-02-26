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
        document.title = "Jive - Stopped";
        }
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
    $.getJSON('/playlist', null, function(json) {
        $('.mpd_playlist_item').remove();
        playlist = json;
        if(json) {
            for(song in json) {
                song = json[song]
                new_row = $('#mpd_playlist_row_template').clone()
                new_row.addClass('mpd_playlist_item')
                $('.mpd_title', new_row).text(song.title)
                $('.mpd_artist', new_row).text(song.artist)
                $('.mpd_duration', new_row).text(duration(song.time))
                new_row.show()
                $('#mpd_playlist').append(new_row);
            }
        }
    });
}
setInterval(status_update, 1000);
