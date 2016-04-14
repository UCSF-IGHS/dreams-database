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

    $('.filter').keyup(function () {
        var targetTable = $(this).data("target_tbody");
        var filterValue = $(this).val();
        filterTable(targetTable, filterValue)
    })

    function filterTable(table_id, filter_value) {
        var rex = new RegExp(filter_value, 'i');
        $(table_id + ' tr').hide();
        $(table_id + ' tr').filter(function () {
            return rex.test($(this).text());
        }).show();
    }

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
                console.log(interventionTypes)
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

    function showSection(show, elementId) {
        if(show)
            $(elementId).removeClass('hidden')
        else
            $(elementId).addClass('hidden')
    }
    
    $('#date-of-completion').change(function () {
        // get the current value
        var selected_date_string = $('#date-of-completion').val();
        if(selected_date_string == null || selected_date_string == "")
            return ""
        var split_date_string_array = selected_date_string.split('/') // MM, DD, YYYY
        var formatted_date_string = split_date_string_array[2] + "-" + split_date_string_array[0] + "-" + split_date_string_array[1]
        $('#date-of-completion-formatted').val(formatted_date_string);
        alert("Formatted and updated " + formatted_date_string)
    })

    $('.validate-intervention-form-field').change(function () {



        // If you are here... No validation errors... Submit form
            
    })

    function validateInterventionEntryForm() {
        // validate form
        var validation_errors_array =  $.merge([], validateInterventionType()) // validate intervention type is selected
        validation_errors_array = $.merge(validation_errors_array, validateDateField())

        // validate required select options
        // hts result
        if(currentInterventionType_Global.fields.has_hts_result == true)
            validation_errors_array = $.merge(validation_errors_array, validateSelectOption('HTS Test Result option ', "#hts-result-select"))

        //  pregnancy test
        if(currentInterventionType_Global.fields.has_pregnancy_result == true)
            validation_errors_array = $.merge(validation_errors_array, validateSelectOption('Pregnancy Test Result option ', "#pregnancy-result-select"))

        // ccc number
        if(currentInterventionType_Global.fields.has_ccc_number == true)
            validation_errors_array = $.merge(validation_errors_array, validateTextInput('CCC Number ', "#ccc-number"))

        // number of sessions
        if(currentInterventionType_Global.fields.has_no_of_sessions == true)
            validation_errors_array = $.merge(validation_errors_array, validateTextInput('Number of Sessions attended ', "#number-of-ss-sessions-attended"))

        // check for errors
        if(validation_errors_array.length > 0){
            // show validation errors
            $('#error-space').html("");
            var textMessage = ""
            $.each(validation_errors_array, function (index, err_messages) {
                textMessage +=  "* " + err_messages + "</br>"
            })
            $('#error-space').html(textMessage);
            // And return
            return false
        }
        return true;
    }

    function validateInterventionType() {
        var current_intervention_id = $('#intervention-type-select').val();
        if(current_intervention_id == null || current_intervention_id == 0)
            return ["Intervention Type is Invalid or NOT Selected"]
        $.each(interventionTypes, function (index, objectVal) {
            if(objectVal.pk == current_intervention_id){
                currentInterventionType_Global = objectVal
                return false
            }
        })

        return []
    }
    
    function validateDateField() {
        var selected_date_string = $('#date-of-completion').val();

        if(selected_date_string == null || selected_date_string == "")
            return ["Intervention Date not Entered"]
        var split_date_string_array = selected_date_string.split('/') // MM, DD, YYYY
        var selected_date_object = new Date(parseInt(split_date_string_array[2]) , parseInt(split_date_string_array[0]) -1 , parseInt(split_date_string_array[1]))
        if(selected_date_object > new Date())
            return ["Intervention Date cannot be later than Today"]

        return []
    }
    
    function validateSelectOption(labelData, selectInputId) {
        var option_val = $(selectInputId).val();
        if (option_val == null || option_val == 0 || option_val == "")
            return [labelData + " is required"]

        return []
    }

    function validateTextInput(labelData, textInputId) {
        var option_val = $(textInputId).val();
        if (option_val == null || option_val == "")
            return [labelData + " is required"]

        return []
    }

    function updateInterventionEntryInView(intervention, code) {
        switch (code){
            case 1001:
                $('#interventions_1001_table').prepend("<tr><td>" + intervention.intervention_type + "</td><td>" + intervention.date_of_completion +  "</td><td> "+ intervention.notes + "</td><td>View/Edit</td></tr>")
                break;
            case 2001:
                break;
            case 3001:
                break;
            case 4001:
                break;
            case 5001:
                break;
        }
    }
    
    $('#intervention-type-select').change(function () {
        // get selected option id
        var currentInterntionId = $('#intervention-type-select').val();
        // search global variable
        $.each(interventionTypes, function (index, type) {
            if(currentInterntionId == type.pk){
                // intervention type // naming
                showSection(true, '#intervention_date_section')
                showSection(type.fields.has_hts_result, '#hts_result_section')
                // hts result
                // ccc number
                showSection(type.fields.has_ccc_number, '#ccc_number_section')
                // pregnancy
                showSection(type.fields.has_pregnancy_result, '#pregnancy_test_section')
                // number of sessions
                showSection(type.fields.has_no_of_sessions, '#no_of_sessions_section')
                // notes
                showSection(true, '#notes_section')

                return false
            }
        })
    })


    $('#btn_save_intervention').click(function (event) {

        event.preventDefault()

        // validate form
        if(!validateInterventionEntryForm())
            return false

        // this is an object returned from the server
        var intervention = {
            'id' : 1,
            'intervention_type': "HTS Test",
            'date_of_completion': '14/04/2016',
            'hts_result' : 'Known Positive',
            'ccc_number':32324,
            'pregnancy_result':'',
            'notes': 'This should get keen followup'
        }

        $('#intervention-modal').modal('hide');
        //updateInterventionEntryInView(intervention);

        // do an ajax post
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : "/ivSave/", // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data:$('#intervention-entry-form').serialize(),
            success : function(data) {
                console.log(data)
                // Close dialog and update view
                //$('#intervention-modal').modal('hide');
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });


    });
});



