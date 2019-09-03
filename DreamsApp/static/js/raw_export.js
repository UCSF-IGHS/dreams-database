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

//
// $(document).ready(function () {
//     $('#btn_download_report').click(function () {
//         var frm = $('#frm_download-report')
//         validateIps()
//         var fromDate = $('#from_date').val()
//         var toDate = $('#toDate').val()
//         if (!validateDates(fromDate, toDate)) {
//             return
//         }
//         // if (!validateIps()) {
//         //     return
//         // }
//         console.log(frm)
//         frm.submit();
//     });
//
//     // $('#from-date').change(function () {
//     //     console.log('dates')
//     //     // console.log(fromDate)
//     //     // console.log(toDate)
//     //     //
//     //     // validateDates(fromDate, toDate)
//     // });
//
//     function validateDates(fromDate, toDate) {
//         dateIsValid = false
//         if (fromDate && toDate){
//             if (fromDate > toDate) {
//                 $('#date_selection_alert').removeClass('hidden').addClass('alert-danger')
//                 .text("From date cannot be come after the to date. Please correct")
//                 .trigger('madeVisible')
//             }
//             else if (fromDate > new Date() || toDate > new Date()) {
//                 $('#date_selection_alert').removeClass('hidden').addClass('alert-danger')
//                 .text("From date cannot be come after the to date. Please correct")
//                 .trigger('madeVisible')
//             }
//             else {
//                 $('#date_selection_alert').removeClass('alert-danger').addClass('hidden')
//                 dateIsValid = true
//             }
//             return dateIsValid
//         }
//     }
//
//
//
//     function validateIps() {
//         var validIps = false
//         var ips = $('#i_p').val();
//         console.log(ips)
//         if (ips == null || ips.length == 0) {
//             $('#ip_selection_alert').removeClass('hidden').addClass('alert-danger')
//                 .text("Please select Implementing Partner to Export Data")
//                 .trigger('madeVisible')
//             return false;
//         }
//         else {
//             return true
//         }
//     }
// });
//
//


