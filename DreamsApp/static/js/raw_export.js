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
        var from_date = $('#from_date').val()
        var to_date = $('#to_date').val()
        if (from_date > new Date()) {
            $('#ip_selection_alert').removeClass('hidden').addClass('alert-danger')
                .text("From date cannot be in the future")
                .trigger('madeVisible')
            return;
        }
        if (to_date > new Date()) {
            $('#ip_selection_alert').removeClass('hidden').addClass('alert-danger')
                .text("To date cannot be in the future")
                .trigger('madeVisible')
            return;
        }
        if(from_date > to_date) {
            $('#ip_selection_alert').removeClass('hidden').addClass('alert-danger')
                .text("From date cannot be after the to date")
                .trigger('madeVisible')
            return;
        }
        frm.submit();
    });
});
