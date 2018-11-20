$(document).ready(function () {
    $('#btn_download_report').click(function () {
        var frm = $('#frm_download-report')
        var ips = $('#i_p').val();
        if (ips == null || ips.length == 0) {
            $('#ip_selection_alert').removeClass('hidden').addClass('alert-danger')
                .text("Please select Implementing Partner to Export Data")
                .trigger('madeVisible')
            return;
        }
        frm.submit();
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

