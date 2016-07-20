$(document).ready(function () {

    $('#alert_modal').on('shown.bs.modal', function (e) {
        // Start counter to close this modal
        setTimeout(function(){
            // hide alert_modal after 2 seconds
            $('#alert_modal').modal('hide');
        }, 5000);
    })

    $('#alert_enrollment_modal').on('shown.bs.modal', function (e) {
        // Start counter to close this modal
        setTimeout(function(){
            // hide alert_modal after 2 seconds
            $('#alert_enrollment_modal').modal('hide');
        }, 5000);
    })

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

    /* Login form submission */

    $('#dp-login-form').submit(function (event) {
        event.preventDefault();
        // Do ajax for login
        var csrftoken = getCookie('csrftoken');
        console.log(csrftoken);
        $.ajax({
            url : '/', // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data:$('#dp-login-form').serialize(),
            success : function(data) {
                result = $.parseJSON(data);
                if(result.status == 'success'){
                    window.location.href = "/clients";
                }
                else{
                    // Indicate error
                    $('.invalid-password-span').removeClass('hidden');
                    $('.invalid-password-span').html(result.message);
                }

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    })

    /* End Login form submission */

    function insertClientTableRow(clients_tbody, pk, dreams_id, first_name, last_name, middle_name, date_of_enrollment, append, is_superuser) {
        var is_superuser = $('#is_superuser').val();
        var row_string = "<tr id='clients_row_" + pk +"' style='cursor: pointer;'>"
                        + "<td>" + dreams_id + "</td>"
                        + "<td>" + first_name + " " + last_name + " " + middle_name +  "</td>"
                        + "<td>" + date_of_enrollment + "</td>"
                        + "<td id='client_' + " + pk + "'>"
                            + "<div class='btn-group'>"
                              + "<button type='button' class='btn btn-sm btn-default' onclick=\"window.location='/client?client_id=" + pk + "'\" style='cursor: pointer;'> Interventions </button>"
                              + "<button type='button' class='btn btn-sm btn-default dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>"
                                + "<span class='caret'></span>"
                                + "<span class='sr-only'>Toggle Dropdown</span>"
                              + "</button>"
                              + "<ul class='dropdown-menu'>"
                                + "<li><a href='#' class='edit_intervention_click edit_client' data-view_mode='view' data-toggle='modal' data-target='#enrollment-modal' data-client_id='" + pk + "' style='cursor: pointer;word-spacing: 0px !important;'> View Enrollment </a></li>"
                                if(is_superuser){
                                row_string += "<li><a href='#' class='edit_intervention_click edit_client' data-toggle='modal' data-target='#enrollment-modal' data-client_id='" + pk +"' style='cursor: pointer;word-spacing: 0px !important;'> Edit Enrollment </a></li>"
                                + "<li><a href='#' class='delete_intervention_click ' data-client_id='" + pk +"' id='delete_client_a_" + pk +"' data-confirm-client-delete='Are you sure you want to delete?'> Delete Enrollment &nbsp;&nbsp;&nbsp;</a></li>"
                                }
                              row_string += "</ul>"
                            + "</div>"
                        + "</td>"
                    + "</tr>"

        if(append)
            clients_tbody.append(row_string);
        else
            clients_tbody.prepend(row_string);
        $('#delete_client_a_' + pk).click(function (event) {
        var clientId = $(this).data('client_id');
        $('#confirmationModal #frm_title').html('Confirm Client Delete Action');
        $('#confirmationModal #frm_body > h4').html('Are you sure you want to delete this client? Changes cannot be undone');
        $('#confirmationModal').modal({show:true});
        // Add delete event listener on confirmation
        $('#confirmationModal #dataConfirmOK').click(function (event) {
            console.log(clientId);
            deleteClient(clientId);
        })
    })
    }

    $('#clients_search_form').submit(function (event) {
        event.preventDefault();
        // do ajax

        // work on reset
        // do an ajax post
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : '/clients', // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data:$('#clients_search_form').serialize(),
            success : function(data) {
                var clients = $.parseJSON(data)
                var clients_tbody = $('#dp-patient-list-body')

                clients_tbody.empty();
                if(clients.length > 0){
                    $.each(clients, function (index, client) {
                        insertClientTableRow(clients_tbody, client.pk,client.fields.dreams_id, client.fields.first_name, client.fields.last_name, client.fields.middle_name, client.fields.date_of_enrollment, true, client.fields.is_superuser);
                    })
                }
                else
                    clients_tbody.append("<tr><td colspan='4' style='text-align: center;font-weight: normal; color: #bbb;'>No clients found matching your search.</td></tr>")
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

    })
    
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
        $('#error-space').text("");
        $('#comments-text').val("")
        // reset the form

    })

    $('.filter').keyup(function () {
        var targetTable = $(this).data("target_tbody");
        var filterValue = $(this).val();
        filterTable(targetTable, filterValue)
    })

    $('.filter-enrollment').keyup(function (event) {
        return
        /*
            This function filters clients table on typing
            It has been disabled for enrollment

        // check which key is pressed
        var rex = new RegExp($(this).val(), 'i');
        $('#dp-patient-list-body tr').hide();
        $('#dp-patient-list-body tr').filter(function () {
            return rex.test($(this).text());
        }).show();

        if($('#dp-patient-list-body tr:visible').length < 1 || $('#dp-patient-list-body tr').length < 1)
            $('#client_actions_alert').removeClass('hidden').addClass('alert-danger')
                        .text("0 Clients found")
                        .trigger('madeVisible')
        */
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
            url : "/ivList", // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data : {
                csrfmiddlewaretoken : csrftoken,
                intervention_category_code : intervention_category_code,
                client_id : $('#current_client_id').val()
            },
            success : function(data) {
                var ivs = $.parseJSON(data.interventions)
                var ivTypes = $.parseJSON(data.iv_types)
                // Clear table
                $(table_id + '  tbody').empty();
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
                    insertInterventionEntryInView(table_id, iv, iv_type, intervention_category_code, false)

                });

                // hide spinner
                $(panel_id + ' .spinner').addClass('hidden')

                // Check for number of rows added
                var new_row_count = $(table_id + '  tbody  tr').length
                // check if no records and insert empty table message
                if(new_row_count < 1){
                    var cols = $(table_id).data('cols');
                    $(table_id + '  tbody').append("<tr><td  colspan='"+ cols +"' class='table-message'> No interventions found</td></tr>")
                }


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
            url : "/ivgetTypes", // the endpoint
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

    function insertInterventionEntryInView(table_id, iv, iv_type, intervention_category_code, top) { // top is a boolean for either position to insert the record
        var tabpanel_id = '#behavioural-interventions'
        switch (intervention_category_code){
            case 1001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                break;
            case 2001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='hts_result'> "+  iv.fields.hts_result +  "</td><td class='client_ccc_number'> " + iv.fields.client_ccc_number + "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='hts_result'> "+  iv.fields.hts_result +  "</td><td class='client_ccc_number'> " + iv.fields.client_ccc_number+ "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                tabpanel_id = '#biomedical-interventions';
                break;
            case 3001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                tabpanel_id = '#post-gbv-care';
                break;
            case 4001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                tabpanel_id = '#social-protection';
                break;
            case 5001:
                if(!top)
                    $(table_id).append("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='no_of_sessions_attended'> "+ iv.fields.no_of_sessions_attended +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                else
                    $(table_id).prepend("<tr id='intervention_"+ iv.pk +"'><td class='name'>" + iv_type.fields.name + "</td><td class='intervention_date'>" + iv.fields.intervention_date +  "</td><td class='no_of_sessions_attended'> "+ iv.fields.no_of_sessions_attended +  "</td><td class='comment'> "+ iv.fields.comment + "</td><td> <span class='glyphicon glyphicon-pencil edit_intervention_click' arial-label='Arial-Hidden'> Edit</span> &nbsp;&nbsp; <span class='glyphicon glyphicon-trash delete_intervention_click' arial-label='Arial-Hidden'> Delete</span> </td></tr>")
                tabpanel_id = '#other-interventions';
                break;

        }
        // check for the number of rows in the table
        if($(table_id + '  tbody  tr').length > 0)
            $(tabpanel_id +  ' .message-view').addClass('hidden')
        setInterventionActionHandler(iv, iv_type, intervention_category_code);
    }

    function setInterventionActionHandler(iv, iv_type, intervention_category_code) {
        $('#intervention_' + iv.pk + ' .edit_intervention_click').click(function (event) {
            $('#intervention-modal').modal('show'); // this is to show the modal
            currentInterventionCategoryCode_Global = intervention_category_code // this will be needed during update!
            interventionTypes = [iv_type]
            intervention = iv
            setInterventionTypesSelect(interventionTypes)
            $('#intervention-type-select').val(iv_type.fields.code).change() // this should change the current selected option and trigger the modal fields to be rendered appropriately
            // set disabled fields and ad values as required
            prePopulateInterventionModal(iv, iv_type)
        })

        $('#intervention_' + iv.pk + ' .delete_intervention_click').click(function (event) {
            // Show a confirm delete dialog
            $('#confirm-delete-mordal').modal('show')
            currentInterventionCategoryCode_Global = intervention_category_code // this will be needed during update!
            interventionTypes = [iv_type]
            intervention = iv
            $('#intervention_delete_id').val(intervention.pk);
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

        var postUrl = "/ivSave" // by default
        if(modalMode == "edit")
            postUrl = "/ivUpdate"

        // do an ajax post
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : postUrl, // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data:$('#intervention-entry-form').serialize(),
            success : function(data) {
                var status = data.status
                var message = data.message
                var alert_id = '#action_alert_' + currentInterventionCategoryCode_Global
                if(status == 'failed'){
                    $(alert_id).removeClass('hidden').addClass('alert-danger')
                        .text(message)
                        .trigger('madeVisible')
                    $("#intervention-modal").each( function() { this.reset; });
                    $('#intervention-modal').modal('hide');
                }
                else{
                    var iv = $.parseJSON(data.intervention)[0]
                    var iv_type = $.parseJSON(data.i_type)[0]
                    if(modalMode != "edit"){
                        insertInterventionEntryInView(table_id, iv, iv_type, intervention_category_code, true)
                        $(alert_id).removeClass('hidden').addClass('alert-success')
                            .text('Intervention has been Saved successfully!')
                            .trigger('madeVisible')
                    }
                    else{
                        // Add existing record on the view
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

                        setInterventionActionHandler(iv, iv_type, intervention_category_code)
                        $(alert_id).removeClass('hidden').addClass('alert-success').text('Intervention has been Updated successfully!')
                    }
                    $("#intervention-modal").each( function() { this.reset; });
                    $('#intervention-modal').modal('hide');
                }
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $(alert_id).removeClass('hidden').addClass('alert-danger').text('An error occurred. Please try again')
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });


    });

    $('.dp-action-alert').on('madeVisible', function (event) {
        setTimeout(function(){
            var alert_space = $(event.target)
            alert_space.removeClass('alert-success').removeClass('alert-danger')
                .addClass('hidden')
                .text("")
        }, 5000);
    })

    $('tr').on('rowChangeMade', function (event) {
        var tr = $(this).addClass('success');
        //tr.css('background-color', '#5bc0de');

        setTimeout(function(){
            tr.removeClass('success');
        }, 5000);
    })

    $('#user_credentials_alert').on('madeVisible_logout', function (event) {
        setTimeout(function(){
            var alert_space = $(event.target)
            alert_space.removeClass('alert-success').removeClass('alert-danger')
                .addClass('hidden')
                .text("")
            window.location.href = "/logout";
        }, 1000);
    })

    $('#btn_delete_intervention_confirmation').click(function (event) {
        var btn = $(event.target);
        // do an ajax post delete

        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : '/ivDelete', // the endpoint
            type : "POST", // http method
            dataType: 'json',
            data:$('#intervention_delete_form').serialize(),
            success : function(data) {
                var result = $.parseJSON(data)
                // remove row from table

                var alert_id = '#action_alert_' + currentInterventionCategoryCode_Global;
                if(result.result == "success"){
                    $('#intervention_' + result.intervention_id).remove();
                    $(alert_id).removeClass('hidden').addClass('alert-success')
                        .text('Intervention has been deleted successfully!')
                        .trigger('madeVisible')
                    // check the number of remaining rows
                    var tbody_id = '#interventions_' + currentInterventionCategoryCode_Global + '_tbody'
                    if($(tbody_id + ' tr').length < 1){
                        // No more record in the table
                        var col_span = $('#interventions_' + currentInterventionCategoryCode_Global + '_table' + ' thead tr')[0].cells.length
                        $(tbody_id).append("<tr><td colspan='" + col_span + "' style='text-align: center'>0 Interventions</td></tr>")
                    }
                }
                else
                    $(alert_id).removeClass('hidden').addClass('alert-danger').text('You do not have the rights to ' +
                        'delete this intervention because it was created by a ' +
                        'different Implementing Partner').
                    trigger('madeVisible')

                $('#confirm-delete-mordal').modal('hide');

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                //$(alert_id).removeClass('hidden').addClass('alert-danger').text('An error occurred. Please try again')
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

            }
        });

        //console.log(intervention)
    })

    function validateClientForm(clientForm) {
        var errors = 0;

        // reset all validate fields
        clientForm.find('.validate_field').each(function (index, field) {
            $('#spn_' + $(field).attr('id')).addClass('hidden');
        })

        // validate required fields
        clientForm.find('.required_field').each(function (index, field) {
            if($(field).val() == null || $(field).val() == ''){
                var spanId = '#spn_' + $(field).attr('id');
                $(spanId).html('&nbsp; &#42; Required')
                    .css('color', 'red')
                    .removeClass('hidden');
                errors++;
            }

        })

        clientForm.find('.phone_number_field').each(function (index, field) {
            var phone_number = $(field).val();
            if(phone_number != null && phone_number != ''){
                var filter = /^((\+[1-9]{1,4}[ \-]*)|(\([0-9]{2,3}\)[ \-]*)|([0-9]{2,4})[ \-]*)*?[0-9]{3,4}?[ \-]*[0-9]{3,4}?$/;
                if (!filter.test(phone_number)) {
                    var spanId = '#spn_' + $(field).attr('id');
                    $(spanId).html('&nbsp; &#42; Invalid Phone Number')
                        .css('color', 'red')
                        .removeClass('hidden');
                    errors++;
                }
            }
        })

        return errors < 1;
    }
    
    $('.format_date_event').change(function (event) {
        var target = $(event.target);
        var target_id = '#' + target.attr('id')
        var formatted_target_id = target_id + '_formatted'

        var selected_date_string = $(target_id).val();
        if(selected_date_string == null || selected_date_string == "")
            return;
        var split_date_string_array = selected_date_string.split('/') // MM, DD, YYYY
        var formatted_date_string = split_date_string_array[2] + "-" + split_date_string_array[0] + "-" + split_date_string_array[1]
        $(formatted_target_id).val(formatted_date_string);
    })

    function deleteClient(client_id) {
        var client_id = client_id;
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : '/clientDelete',
            type : "GET",
            dataType: 'json',
            data:{'client_id':client_id},
            success : function(data) {
                var result = $.parseJSON(data)
                if(result.status == "success"){
                    // show
                    $('#clients_row_' + client_id).remove();
                    $('#client_actions_alert').removeClass('hidden').addClass('alert-success')
                        .text(result.message)
                        .trigger('madeVisible')
                    // check number of rows in table
                    if($('#dp-patient-list-body tr').length < 1){
                        // No more record in the table
                        $('#dp-patient-list-body').append("<tr><td colspan='4' style='text-align: center'>0 Clients</td></tr>")
                    }

                }
                else{
                    $('#client_actions_alert').removeClass('hidden').addClass('alert-danger')
                        .text(result.message)
                        .trigger('madeVisible')
                }
                $('#confirmationModal').modal('hide');
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#confirmationModal').modal('hide');
                $('#alert_enrollment').removeClass('hidden').addClass('alert-danger')
                        .text('An error occurred while deleting client. Contact system administratior if this persists')
                        .trigger('madeVisible')
            }
        });
    }

    $('#enrollment-modal').on('shown.bs.modal', function (e) {
        var button = $(e.relatedTarget);
        var client_id = button.data('client_id');
        var view_mode = button.data('view_mode');
        if(client_id != null && client_id != 0){
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                url : '/clientEdit', // the endpoint
                type : "GET", // http method
                dataType: 'json',
                data:{'client_id':client_id},
                success : function(response_data) {
                    var response = JSON.parse(response_data.client);
                    var client = response[0];

                    if(view_mode == 'view')
                        $('#enrollment-form :input').attr('disabled', true);
                    else
                        $('#enrollment-form :input').attr('disabled', false);
                    $('#enrollment-form #btn_hide_enrollment').attr('disabled', false);
                    $('#enrollment-form #close__enrollment_modal').attr('disabled', false);
                    // set client_id-- this is not named the same way in the model as in the form
                    $('#enrollment-form #client_id').val(client.pk)
                    $.each(client.fields, function (index, field) {
                        $('#enrollment-form #' + index).val(field);
                    })

                    // set IP values
                    $('#implementing_partner option').each(function() {
                        if($(this).data('ip_id') ==  client.fields.implementing_partner) {
                            $(this).prop("selected", true);
                        }
                    });

                    // Set Verification document values
                    $('#verification_document option').each(function() {
                        if($(this).data('verification_document_id') ==  client.fields.verification_document) {
                            $(this).prop("selected", true);
                        }
                    });

                    // Set Marital status values
                    $('#marital_status option').each(function() {
                        if($(this).data('marital_status_id') ==  client.fields.marital_status) {
                            $(this).prop("selected", true);
                        }
                    });

                    // Set County values
                    $('#county_of_residence option').each(function() {
                        if($(this).data('county_of_residence_id') ==  client.fields.county_of_residence) {
                            $(this).prop("selected", true);
                        }
                    });

                    getSubCounties(true, $('#county_of_residence').val(), client.fields.sub_county, client.fields.ward)   // bool, code and id
                },

                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    //$(alert_id).removeClass('hidden').addClass('alert-danger').text('An error occurred. Please try again')
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

                }
            });
        }
        else {
            return;
        }
    })

    $('#enrollment-modal').on('hide.bs.modal', function (e) {
        $('#enrollment-form .clear_value').val('');
        $('#enrollment-form .clear_span').html('');
        $('#enrollment-form .clear_true').prop('checked', false);
    })

    $('#enrollment-form').submit(function (event) {
        event.preventDefault();
        var enrollment_form_submit_mode = 'new';
        var post_url = '/clientSave';
        var clientForm = $(event.target);
        if(!validateClientForm(clientForm))
            return;
        var client_id = $('#enrollment-form #client_id').val();
        if(client_id != null && client_id != ''){
            enrollment_form_submit_mode = 'edit';
            post_url = '/clientEdit';
        }
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : post_url,
            type : "POST",
            dataType: 'json',
            data:$('#enrollment-form').serialize(),
            success : function(data) {
                var result = $.parseJSON(data)
                if(result.status == "success"){
                    var clients_tbody = $('#dp-patient-list-body')
                    var date_of_enrollment = new Date($('#enrollment-form #date_of_enrollment').val());
                    date_of_enrollment = $.datepicker.formatDate('MM d, yy', date_of_enrollment)
                    if(enrollment_form_submit_mode == 'new'){
                        // Prepend new line into the clients' table
                        insertClientTableRow(clients_tbody, result.client_id,$('#enrollment-form #dreams_id').val(), $('#enrollment-form #first_name').val(), $('#enrollment-form #last_name').val(), $('#enrollment-form #middle_name').val(), date_of_enrollment, false, true)
                    }
                    else{
                        // Update relevant table line without reloading the page
                        console.log(result)
                        $('#clients_row_' + result.client_id).remove(); // remove row
                        // Insert updated value
                        insertClientTableRow($('#dp-patient-list-body'), result.client_id,$('#enrollment-form #dreams_id').val(), $('#enrollment-form #first_name').val(), $('#enrollment-form #last_name').val(), $('#enrollment-form #middle_name').val(), date_of_enrollment, false, $('#is_superuser').val());
                    }
                    $('#client_actions_alert').removeClass('hidden').addClass('alert-success')
                        .text(result.message)
                        .trigger('madeVisible')

                    // Close enrollment modal when done
                    $("#enrollment-modal").modal('hide');
                }
                else{
                    $("#enrollment-modal").modal('hide');
                    $('#client_actions_alert').removeClass('hidden').addClass('alert-danger')
                        .text(result.message)
                        .trigger('madeVisible')
                }
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#alert_enrollment').removeClass('hidden').addClass('alert-danger')
                        .text('An error occurred while processing client details. Contact system administratior if this persists')
                        .trigger('madeVisible')
            }
        });
    })

    $('#btn_hide_enrollment').click(function (event) {
        $('#enrollment-modal').modal('toggle');
    })

    $('#county_of_residence').change(function (event) {
        getSubCounties(false, null, null, null);
    })

    function getSubCounties(setSelected, c_code, sub_county_id, ward_id) {
        var county_code = setSelected == true ? c_code : $('#county_of_residence').val();
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : "/getSubCounties", // the endpoint
            type : "GET", // http method
            dataType: 'json',
            data : {
                county_code : county_code,
            },
            success : function(data) {
                var sub_counties = $.parseJSON(data.sub_counties);
                $("#sub_county option").remove();
                $("#sub_county").append("<option value=''>Select Sub-County</option>");
                $.each(sub_counties, function (index, field) {
                    $("#sub_county").append("<option data-sub_county_id='" + field.pk + "' value='" + field.fields.code + "'>" + field.fields.name + "</option>");
                })

                // setting sub-county when necessary
                if(setSelected){    // set selected sub county
                    $('#sub_county option').each(function() {
                        if(sub_county_id != null && $(this).data('sub_county_id') ==  sub_county_id ) {
                            $(this).prop("selected", true);
                            // Load wards since a subcounty has been selected
                            getWards(true, $(this).val(), ward_id)
                        }
                    });
                }
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    function getWards(setSelected, sc_code, ward_id) {
        var sc_code = setSelected ? sc_code : $('#sub_county').val();
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url : "/getWards", // the endpoint
            type : "GET", // http method
            dataType: 'json',
            data : {
                sub_county_code : sc_code,
            },
            success : function(data) {
                var wards = $.parseJSON(data.wards);
                $("#ward option").remove();
                $("#ward").append("<option value=''>Select Ward</option>");
                $.each(wards, function (index, field) {
                    $("#ward").append("<option data-ward_id='" + field.pk + "' value='" + field.fields.code + "'>" + field.fields.name + "</option>");
                })

                if(setSelected){
                    $('#ward option').each(function() {
                        if(ward_id != null && $(this).data('ward_id') ==  ward_id ) {
                            $(this).prop("selected", true);
                        }
                    });
                }
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
    
    $('#sub_county').change(function (event) {
        getWards(false, null, null);
    })

    /*
    $('#filter-log-date').change(function (event) {
        // do a get with the new parameters
        window.location.href = "/logs/?page=1&date=" + $('#filter-log-date').val();
    })
    */

    /* Confirmation modal*/
    $('a[data-confirm-client-delete]').click(function (event) {
        var clientId = $(this).data('client_id');
        $('#confirmationModal #frm_title').html('Confirm Client Delete Action');
        $('#confirmationModal #frm_body > h4').html('Are you sure you want to delete this client? Changes cannot be undone');
        $('#confirmationModal').modal({show:true});
        // Add delete event listener on confirmation
        $('#confirmationModal #dataConfirmOK').click(function (event) {
            deleteClient(clientId);
        })
    })
    /* End of Confirmation modal*/

    $('#filter-log-form').submit(function (event) {
        // this is going as expected!
    })

    $('#audit-log-clear-filtes').click(function (event) {
        $('#filter-log-text').val('');
        $('#filter-log-date').val('');
        window.location.href = "/logs";
    })

    /* users section */

    $('.user_action').click(function (event) {
        var btn = event.target;
        var u_action = $(btn).data('user_action');
        var ip_user_id = $(btn).data('ip_user_id');

        var confirm_title = "";
        var confirm_message = "";
        var active = false
        var callback_func = null;
        switch (u_action){
            case "deactivate_user":
                confirm_title = 'Confirm User Deactivation Action'
                confirm_message = 'Are you sure you want to Deactivate User?'
                callback_func = toggleUserStatus
                active = false;
                break;
            case "activate_user":
                confirm_title = 'Confirm User Activation Action'
                confirm_message = 'Are you sure you want to Activate User?'
                callback_func = toggleUserStatus
                active = true;
                break;
            case "delete_user":
                confirm_title = 'Confirm User Delete Action'
                confirm_message = 'Are you sure you want to Delete User? This action cannot be undone.'
                callback_func = deleteUser
                break;
            default:
                break;
        }

        $('#confirmationModal #frm_title').html(confirm_title);
        $('#confirmationModal #frm_body > h4').html(confirm_message);
        $('#confirmationModal').modal({show:true});
        // Add delete event listener on confirmation
        $('#confirmationModal #dataConfirmOK').click(function (event) {
            callback_func(ip_user_id, active, btn);
            $(event.target).off('click'); // Works like a charm
        })
    })

    function toggleUserStatus(ip_user_id, activate, target) {
        // deactivate using ajax
            // No form, just a normal get
        $.ajax({
            url : '/admin/users/toggle_status',
            type : "GET",
            dataType: 'json',
            data:{
                'ip_user_id': ip_user_id,
                'toggle': activate
            },
            success : function(data) {
                if(data.status == "success"){
                    // Show message
                    $('#user_actions_alert').removeClass('hidden').addClass('alert-success')
                        .text(data.message)
                        .trigger('madeVisible')
                    // Change view
                    $(target).addClass('hidden')// Hide current
                    $(target).siblings('.hidden').removeClass('hidden') // Show sibling
                    // change status text
                    var tblData = $(target).parent().parent() // <td>
                    tblData.siblings().eq(4).html(activate ? "Active" : "Disabled");
                    tblRow = tblData.parent()  // <tr>
                    tblRow.trigger('rowChangeMade')
                }
                else{
                    // We wil also know what to do here
                    $('#user_actions_alert').removeClass('hidden').addClass('alert-danger')
                        .text(data.message)
                        .trigger('madeVisible')
                }
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#user_actions_alert').removeClass('hidden').addClass('alert-danger')
                        .text('An error occurred while processing client details. Contact system administratior if this persists')
                        .trigger('madeVisible')
            }
        });

        // hide modal
        $("#confirmationModal").modal('hide');
    }

    function deleteUser(ip_user_id, active, target) {
        //alert("Deleting: " + ip_user_id)
    }

    $("#user-entry-form").validate({
        rules: {
            reg_role: "required",
            reg_firstname: {
                required: true,
                minlength: 2
            },
            reg_lastname: {
                required: true,
                minlength: 2
            },
            reg_username: {
                required: true,
                minlength: 2
            },
            reg_email: {
                required: true,
                email: true
            }
        },
        messages: {
            reg_firstname: "* Please enter your First Name",
            reg_lastname: "* Please enter your Last Name",
            reg_username: {
                required: "* Please enter a username",
                minlength: "* Your username must consist of at least 2 characters"
            },
            reg_email: "* Please enter a valid email address"
        },
        highlight: function (element) {
            //$(element).parent().addClass('text-danger')
            //console.log();
            $(element).parent().find('label.error').addClass('text-danger')
        },
        unhighlight: function (element) {
            $(element).parent().find('label.error').removeClass('text-danger')
        }
    });

    $('#reg_emailaddress').on('input', function (e) {
        $('#reg_username').val($(e.target).val().split('@')[0])
    })

    $("#user-entry-form").submit(function (e) {
        e.preventDefault();
        if(!$(e.target).valid())
            return false;

        /* Form is valid. You can proceed to submit and register user. We are using an ajax call */
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url : '/admin/users/save',
            type : "POST",
            dataType: 'json',
            data:$('#user-entry-form').serialize(),
            success : function(data) {
                console.log(data.status + " " + data.message);
                if(data.status == "success"){
                    alert(data.message);
                    $("#user-modal").modal('hide');
                    window.location.href = "/admin/users";
                }
                else{
                    $('#user_actions_alert').removeClass('hidden').addClass('alert-danger')
                        .text(data.message)
                        .trigger('madeVisible')
                    $("#user-modal").modal('hide');
                }
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#user_actions_alert').removeClass('hidden').addClass('alert-danger')
                        .text('An error occurred while processing client details. Contact system administratior if this persists')
                        .trigger('madeVisible')
            }
        });
    })
    
    $('#user-clear-filters').click(function (e) {
        window.location.href = "/admin/users";
    })

    $("#user_change_password_form").validate({
        rules: {
            ch_username: {
                required: true,
                minlength: 2
            },
            ch_current_password: {
                required: true,
                minlength: 2
            },
            ch_new_password: {
                required: true,
                minlength: 2
            },
            ch_confirm_new_password: {
                required: true,
                minlength: 2,
                equalTo: "#ch_new_password"
            }
        },
        messages: {
            ch_username: {
                required: "* Please enter your Username",
                minlength: "* Your username must be at least 2 characters long"
            },
            ch_current_password: {
               required:  "* Please enter your current password",
                minlength: "Your current password must be at least 2 characters long"
            },
            ch_new_password: {
                required: "* Please enter your new password",
                minlength: "Your new password must be at least 2 characters long"
            },
            ch_confirm_new_password: {
                required: "* Please confirm your new password",
                equalTo: "Please enter matching new and confirmation passwords"
            }
        },
        highlight: function (element) {
            $(element).parent().addClass('text-danger')
        },
        unhighlight: function (element) {
            $(element).parent().removeClass('text-danger')
        }
    });

    $("#user_change_password_form").submit(function (event) {
        event.preventDefault()
        if(!$(event.target).valid()) // Check if form is valid
            return false;   // return, form is not valid

        // Form is valid, do an ajax call
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url : '/admin/users/change_cred',
            type : "POST",
            dataType: 'json',
            data:$('#user_change_password_form').serialize(),
            success : function(data) {
                console.log(data.status + " " + data.message);
                if(data.status == "success"){
                    $('#user_credentials_alert').removeClass('hidden').addClass('alert-success')
                        .text(data.message)
                        .trigger('madeVisible_logout')
                }
                else{
                    $('#user_credentials_alert').removeClass('hidden').addClass('alert-danger')
                        .text(data.message)
                        .trigger('madeVisible_logout')
                    $("#user-modal").modal('hide');
                }
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#user_credentials_alert').removeClass('hidden').addClass('alert-danger')
                        .text('An error occurred while processing client details. Contact system administratior if this persists')
                        .trigger('madeVisible')
            }
        });
    })
    /* end of users section */

    /* Custom error pages */

    /* End Custom error pages */

});



