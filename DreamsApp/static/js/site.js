$(document).ready(function () {
    $('#i_types').change(function () {
        fetchRelatedInterventions();
    });

    //For getting CSRF token
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

     $('#intervention-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var interventionCategoryCode = button.data('whatever')
        fetchRelatedInterventions(interventionCategoryCode)
    })

    function fetchRelatedInterventions(interventionCategoryCode) {
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : "/ivgetTypes/", // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data : {
                csrfmiddlewaretoken : csrftoken,
                category_code : interventionCategoryCode//$('#i_types').val()
            },
            success : function(data) {
                interventionTypes = $.parseJSON(data.itypes); // Gloabal variable

                var combo = $('#intervention-type-select');
                combo.empty();
                combo.append($("<option />").attr("value", '').text('Select Intervention').addClass('selected disabled hidden').css({display:'none'}));
                $.each(interventionTypes, function(){
                    combo.append($("<option />").attr("value", this.pk).text(this.fields.name));
                    console.log(this.fields);
                });

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    function hideSection(hide, elementId) {
        if(hide)
            $(elementId).removeClass('hidden')
        else
            $(elementId).addClass('hidden')
    }

    $('#intervention-type-select').change(function () {
        // get selected option id
        var currentInterntionId = $('#intervention-type-select').val();
        // search global variable
        $.each(interventionTypes, function (index, type) {
            if(currentInterntionId == type.pk){
                hideSection(type.fields.has_hts_result || type.fields.has_pregnancy_result, '#date_of_completion_section')
                hideSection(type.fields.has_hts_result, '#hts_test_section')
                hideSection(type.fields.has_hts_result, '#linkage_date_section')
                hideSection(type.fields.has_hts_result, '#ccc_number_section')
                hideSection(type.fields.has_pregnancy_result, '#pregnancy_test_section')
                //hideSection(type.fields.has_pregnancy_result, '#sessions_attended_section') // Modification from this point to take care of other sections

            }
        })
    })
});



