$(document).ready(function () {
    var timer = null;

    function refreshAjax() {
        var btn = $('#autorefresh');
        var lid = encodeURIComponent(btn.data('lid'));
        var query = encodeURIComponent(btn.data('query'));
        var lang = encodeURIComponent(btn.data('lang'));
        var url = 'http://' + window.location.host + '/api/' + lid + '/' + query;
        if (lang) {
            url += '/' + lang;
        }
        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                if (data.lid > lid) {
                    btn.data('lid', data.lid);
                    btn.toggleClass('hide');
                    var interval = btn.data('interval') * 1000;
                    clearInterval(timer);
                    timer = null;

                    $('#tweet-cnt').text(parseInt($('#tweet-cnt').text()) + data.tweets.length);

                    data.tweets.forEach(function (tweet) {
                        $('#wall').prepend(tweet);
                    });
                    bind_details_btn();

                    timer = setInterval(refreshAjax, interval);
                    btn.toggleClass('hide');
                }
            },
            error: function (request, status, error) {
                //alert(request.responseText);
            }
        });
    }

    function bind_details_btn() {
        var btns = $('.details-btn');
        btns.unbind('click');
        btns.click(function () {
            var target = $(this).data('target');
            $(target).toggleClass('hide');
            var gl = $(this).find('.glyphicon');
            gl.toggleClass('glyphicon-chevron-down');
            gl.toggleClass('glyphicon-chevron-up');
        });
    }

    bind_details_btn();

    $('#query-btn').click(function () {
        var query = encodeURIComponent($('#query').val());
        var lang = encodeURIComponent($('#lang').val());
        var url = 'http://' + window.location.host + '/q/' + query;
        if (lang) {
            url += '/' + lang;
        }
        window.location.assign(url);
    });

    $('#autorefresh').click(function () {
        $(this).toggleClass('btn-refresh-off');
        $(this).toggleClass('btn-refresh-on');
        var interval = $(this).data('interval') * 1000;
        if (timer == null) {
            timer = setInterval(refreshAjax, interval);
        } else {
            clearInterval(timer);
            timer = null;
        }
    });

    $('#cleanup').click(function () {
        $('#wall').empty();
        $('#tweet-cnt').text(0);
    });
});