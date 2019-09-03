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


