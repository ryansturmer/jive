since = '';

function refresh() {
    $.getJSON('/_posts', {since: since}, function(data) {
        if (data.count > 0) {
            since = data.since;
            $('#posts').prepend(data.html);
        }
    });
}

$('#textForm').submit(function(event) {
    event.preventDefault();
    $.post('/_add_post', $('#textForm').serialize(), function(data) {
        refresh();
    });
    $('#textForm').find('input[name=text]')[0].value = '';
});

setInterval(function() {
    refresh();
}, 1000);

refresh();
