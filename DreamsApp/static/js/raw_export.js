$(document).ready(function () {
    $('#btn_download_excel').click(function () {
        var frm = $('#frm_download-excel')
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

// function download_excel() {
//     var i_frame = document.getElementById('download_excel');
//     var csrftoken = getCookie('csrftoken');
//     var ips = $('#i_p').val();
//     var sub_county = $('#id_sub_county').val();
//     var ward = $('#id_ward').val();
//     var sub_grantee = null;
//
//     if ($('#id_sub_grantee')) {
//         sub_grantee = $('#id_sub_grantee').val();
//     }
//
//     $.ajax({
//         url: "/download-excel/", // the endpoint
//         type: "POST", // http method
//         dataType: 'json',
//         data: {
//             csrfmiddlewaretoken: csrftoken,
//             ips: ips,
//             sub_county: sub_county,
//             ward: ward,
//             sub_grantee: sub_grantee
//         },
//         success: function (data) {
//             alert(data);
//         },
//
//         // handle a non-successful response
//         error: function (xhr, errmsg, err) {
//             $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
//                 " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
//             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//         }
//     });
// }
