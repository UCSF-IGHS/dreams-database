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

    $('.nav-tabs a[href="#' + "behavioural-interventions" + '"]').tab('show');  // set the default tab on load


    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        //Load tabs
        var target = $(e.target)    // this is the tab anchor.. Get the table
        var panel_id = target.attr('href')
        var intervention_category_code = target.data("intervention_category_code");
        var table_id = $(this).data("tab_intervention_table_id")
        var row_count = $(table_id + '  tbody  tr').length
        if(row_count > 0)
            return  // Loading has been done before...

        // Show loading spinner on tab
        var spinner = $(panel_id + ' .spinner')
        spinner.removeClass('hidden')

        // Do an ajax POST to get elements

        var csrftoken = getCookie('csrftoken');
        $('#intervention_category_code').val(intervention_category_code)

        $.ajax({
            url : "/ivList/", // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data : {
                csrfmiddlewaretoken : csrftoken,
                intervention_category_code : intervention_category_code,
                client_id : $('#client_id').val()
            },
            success : function(data) {
                var ivs = $.parseJSON(data.interventions)
                var ivTypes = $.parseJSON(data.iv_types)
                // populate table
                $.each(ivs, function(index, iv){
                    // Get corresponding iv_type
                    var iv_type = {}
                    $.each(ivTypes, function (index, obj) {

                        if(obj.pk == iv.fields.intervention_type){
                            iv_type = obj
                            return false
                        }
                    })
                    updateInterventionEntryInView(table_id, iv, iv_type, intervention_category_code, false)

                });

                // hide spinner
                $(panel_id + ' .spinner').addClass('hidden')

                // Check for number of rows added
                var new_row_count = $(table_id + '  tbody  tr').length
                if(new_row_count < 1)
                    $(panel_id + ' .message-view').removeClass('hidden')
                else
                    $(panel_id + ' .message-view').addClass('hidden')

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });


    })

    function filterTable(table_id, filter_value) {
        var rex = new RegExp(filter_value, 'i');
        $(table_id + ' tr').hide();
        $(table_id + ' tr').filter(function () {
            return rex.test($(this).text());
        }).show();
    }

    function fetchRelatedInterventions(interventionCategoryCode) {
        currentInterventionCategoryCode_Global = interventionCategoryCode
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
                    combo.append($("<option />").attr("value", this.fields.code).text(this.fields.name));
                    // console.log(this.fields);
                    // console.log(this.fields.code)
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
        var current_intervention_code = $('#intervention-type-select').val();
        if(current_intervention_code == null || current_intervention_code == 0)
            return ["Intervention Type is Invalid or NOT Selected"]
        $.each(interventionTypes, function (index, objectVal) {
            if(objectVal.fields.code == current_intervention_code){
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

    function updateInterventionEntryInView(table_id, iv, iv_type, intervention_category_code, top) { // top is a boolean for either position to insert the record
        switch (intervention_category_code){
            case 1001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                $('#intervention_' + iv.pk).data({"iv": iv, "iv_type": iv_type})
                break;
            case 2001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+  iv.fields.hts_result + iv.fields.client_ccc_number +  "</td><td> "+ "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+  iv.fields.hts_result + iv.fields.client_ccc_number +  "</td><td> "+ "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                $('#intervention_' + iv.pk).data({"iv": iv, "iv_type": iv_type})
                break;
            case 3001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                $('#intervention_' + iv.pk).data({"iv": iv, "iv_type": iv_type})
                break;
            case 4001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                $('#intervention_' + iv.pk).data({"iv": iv, "iv_type": iv_type})
                break;
            case 5001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.no_of_sessions_attended +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td>" + iv_type.fields.name + "</td><td>" + iv.fields.intervention_date +  "</td><td> "+ iv.fields.no_of_sessions_attended +  "</td><td> "+ iv.fields.comment + "</td><td>View/Edit</td></tr>")
                $('#intervention_' + iv.pk).data({"iv": iv, "iv_type": iv_type})
                break;
        }
    }
    
    $('#intervention-type-select').change(function () {
        // get selected option id
        var currentInterntionId = $('#intervention-type-select').val(); // code
        // search global variable
        $.each(interventionTypes, function (index, type) {
            if(currentInterntionId == type.fields.code){
                showSection(true, '#intervention_date_section')
                showSection(type.fields.has_hts_result, '#hts_result_section')
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

        var target = $(event.target)
        var intervention_category_code = currentInterventionCategoryCode_Global
        var table_id = "#interventions_" + intervention_category_code + "_table"

        if (intervention_category_code == null || intervention_category_code == "" || table_id == null || table_id == "")
            return


        event.preventDefault()

        // validate form
        if(!validateInterventionEntryForm())
            return false

        // do an ajax post
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : "/ivSave/", // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data:$('#intervention-entry-form').serialize(),
            success : function(data) {
                var iv = $.parseJSON(data.intervention)
                var iv_type = $.parseJSON(data.i_type)
                updateInterventionEntryInView(table_id, iv[0], iv_type[0], intervention_category_code, true)
                $('#intervention-modal').modal('hide');

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



