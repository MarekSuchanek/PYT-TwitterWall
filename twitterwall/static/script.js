$(document).ready(function () {
    var timer = null;
    function refreshAjax() {
        var btn = $('#autorefresh');
        var lid = encodeURIComponent(btn.data('lid'));
        var query = encodeURIComponent(btn.data('query'));
        var lang = encodeURIComponent(btn.data('lang'));
        var url = 'http://'+window.location.host+'/api/'+lid+'/'+query;
        if(lang) {
            url += '/'+lang;
        }
        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                if(data.lid > lid) {
                    btn.data('lid', data.lid);
                    $('#wall').prepend(data.html);
                }
            },
            error: function (request, status, error) {
                //alert(request.responseText);
            }
        });
    }

    $('.details-btn').click(function () {
        var target = $(this).data('target');
        $(target).toggleClass('hide');
        var gl = $(this).find('.glyphicon');
        gl.toggleClass('glyphicon-chevron-down');
        gl.toggleClass('glyphicon-chevron-up');
    });
    $('#query-btn').click(function () {
        var query = encodeURIComponent($('#query').val());
        var lang = encodeURIComponent($('#lang').val());
        var url = 'http://'+window.location.host+'/q/'+query;
        if(lang) {
            url += '/'+lang;
        }
        window.location.assign(url);
    });
    $('#autorefresh').click(function () {
        $(this).toggleClass('btn-refresh-off');
        $(this).toggleClass('btn-refresh-on');
        var interval = $(this).data('interval')*1000;
        alert(interval);
        if(timer == null){
            timer = setInterval(refreshAjax, interval);
        }else{
            clearInterval(timer);
            timer = null;
        }
    });
    $('#cleanup').click(function () {
        $('#wall').empty();
        $('#tweet-cnt').val(0);
    });

});