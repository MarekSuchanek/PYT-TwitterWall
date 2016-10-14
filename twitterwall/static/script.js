$(document).ready(function () {
    var timer = null;
    function refreshAjax() {
        alert('yolo');
    }

    $('.details-btn').click(function () {
        var target = $(this).data('target');
        $(target).toggleClass('hide');
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
       alert('a');
       if(timer == null){
           timer = setInterval(refreshAjax, 1000);
           alert('timer setup');
       }else{
           clearInterval(timer);
           timer = null;
       }
    });

});