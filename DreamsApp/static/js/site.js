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
         // check the mode... Can be new or edit
        var button = $(event.relatedTarget) // Button that triggered the modal
        var interventionCategoryCode = button.data('whatever')

         // Check if this is null.
         if (interventionCategoryCode != null && interventionCategoryCode != "edit") { // This is a new mode
             fetchRelatedInterventions(interventionCategoryCode)
             modalMode = "new";
         }
         else{
             modalMode = "edit"
             // this is an edit mode.. adjsut the view accordingly
             // set intervention type and disable field
             // This does not happen here! It is handled elsewhere!
         }
    })

    $('#intervention-modal').on('shown.bs.modal', function (event) {
         if(modalMode == null || modalMode == "new"){
             // Do nothing
         }
        else if (modalMode == "edit"){
             $('#intervention_id').val(intervention.pk) // This is the intervention id
         }
    })

    $('#intervention-modal').on('hide.bs.modal', function (event) {
        $('#intervention-type-select').removeAttr('disabled')
        // reset the form

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
                setInterventionTypesSelect(interventionTypes)
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    function setInterventionTypesSelect(interventionTypes) {
        var combo = $('#intervention-type-select');
        combo.empty();
        combo.append($("<option />").attr("value", '').text('Select Intervention').addClass('selected disabled hidden').css({display:'none'}));
        $.each(interventionTypes, function(){
            combo.append($("<option />").attr("value", this.fields.code).text(this.fields.name));
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

    function setDateField(dateVal) {
        // set the original value
        $('#date-of-completion-formatted').val(dateVal);
        var split_date_string_array = dateVal.split('-')
        $('#date-of-completion').val(split_date_string_array[1] + "/" + parseInt(split_date_string_array[2]) + "/" +  parseInt(split_date_string_array[0]))
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
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                break;
            case 2001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='hts_result'> "+  iv.fields.hts_result +  "</td><td class='client_ccc_number'> " + iv.fields.client_ccc_number + "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='hts_result'> "+  iv.fields.hts_result +  "</td><td class='client_ccc_number'> " + iv.fields.client_ccc_number+ "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                break;
            case 3001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                break;
            case 4001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                break;
            case 5001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='no_of_sessions_attended'> "+ iv.fields.no_of_sessions_attended +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='no_of_sessions_attended'> "+ iv.fields.no_of_sessions_attended +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td class='edit_intervention_click'><span class='glyphicon glyphicon-pencil' arial-label='Arial-Hidden'></span> Edit</td></tr>")
                break;

        }

        setInterventionAction(iv, iv_type, intervention_category_code);

    }

    function setInterventionAction(iv, iv_type, intervention_category_code) {
        $('#intervention_' + iv.pk + ' .edit_intervention_click').click(function (event) {
            $('#intervention-modal').modal('show'); // this is to show the modal
            currentInterventionCategoryCode_Global = intervention_category_code // this will be needed during update!
            interventionTypes = [iv_type]
            intervention = iv
            setInterventionTypesSelect(interventionTypes)
            // set the current intevention type to be the same
            $('#intervention-type-select').val(iv_type.fields.code).change() // this should change the current selected option and trigger the modal fields to be rendered appropriately
            // set disabled fields and ad values as required
            prePopulateInterventionModal(iv, iv_type)
        })
    }

    $('#intervention-type-select').change(function () {
        // get selected option id
        var currentInterventionTypeCode = $('#intervention-type-select').val(); // code
        // search global variable
        $.each(interventionTypes, function (index, type) {
            if(currentInterventionTypeCode == type.fields.code){
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

    function prePopulateInterventionModal(iv, iv_type) {
        $('#intervention-type-select').attr('disabled','disabled')

        // Populate values

        setDateField(iv.fields.intervention_date) // done

        // check for the rest of the fields
        if(iv_type.fields.has_hts_result)
            $('#hts-result-select').val(iv.fields.hts_result)
        // ccc number
        if(iv_type.fields.has_ccc_number)
            $('#ccc_number').val(iv.fields.client_ccc_number)
        // pregnancy
        if(iv_type.fields.has_pregnancy_result)
            $('#pregnancy-result-select').val(iv.fields.pregnancy_test_result)
        // number of sessions
        if(iv_type.fields.has_no_of_sessions)
            $('#number-of-ss-sessions-attended').val(iv.fields.no_of_sessions_attended)
        // notes
        $('#comments-text').val(iv.fields.comment)

    }


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

        var postUrl = "/ivSave/" // by default
        if(modalMode == "edit")
            postUrl = "/ivUpdate/"

        // do an ajax post
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : postUrl, // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data:$('#intervention-entry-form').serialize(),
            success : function(data) {
                var iv = $.parseJSON(data.intervention)[0]
                var iv_type = $.parseJSON(data.i_type)[0]
                if(modalMode != "edit"){
                    updateInterventionEntryInView(table_id, iv, iv_type, intervention_category_code, true)
                    alert("Record Added Successfully!")
                }
                else{
                    // Update existing record on the view
                    // get table name and row id
                    var row_id = 'intervention_' + iv.pk
                    $('#' + row_id + ' .intervention_date').text(iv.fields.intervention_date)

                    // check for the rest of the fields
                    if(iv_type.fields.has_hts_result)
                        $('#' + row_id + ' .hts_result').text(iv.fields.hts_result)
                    // ccc number
                    if(iv_type.fields.has_ccc_number)
                        $('#' + row_id + ' .client_ccc_number').text(iv.fields.client_ccc_number)
                    // pregnancy
                    if(iv_type.fields.has_pregnancy_result)
                        $('#' + row_id + ' .pregnancy_test_result').text(iv.fields.pregnancy_test_result)
                    // number of sessions
                    if(iv_type.fields.has_no_of_sessions)
                        $('#' + row_id + ' .no_of_sessions_attended').text(iv.fields.no_of_sessions_attended)
                    // notes
                    $('#' + row_id + ' .comment').text(iv.fields.comment)

                    setInterventionAction(iv, iv_type, intervention_category_code)

                    alert("Record updated Successfully")
                }
                $("#intervention-modal").each( function() { this.reset; });
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

    $('.edit_intervention_click').click(function (event) {
        var target = $(event.target)
    })

});



