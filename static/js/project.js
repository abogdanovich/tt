$(document).ready(function() {

    var msg_error_apply_user_bool = false;

    $('.apply_employee_to_real_project').live('click', function(){
        var l = DD('l');
        l('apply_employee_to_real_project CLICK');


        $('#msg_error_apply_user').html('');
        var selectedEmployee = $("#employee").find(":selected");

        if ( typeof selectedEmployee.attr('id') !== 'undefined' ) {
            var id = selectedEmployee.attr('id').substr('employee_'.length);
            var text = selectedEmployee.html() + '&nbsp;&nbsp;&nbsp;';
            var role_on_project = $("#role_on_project").attr('value');
            
            
            if(role_on_project.length > 5) {            
    //------------------------------------------------------------------------------
    //            var li = document.createElement('li');
                var li = $('<li></li>');
    //            li.className = "li_appended_employee";
                li.attr('class', 'li_appended_employee');
    //            li.id = "li_appended_employee" + id;
                li.attr('id', "li_appended_employee" + id);

                    var divAppliedEmployeeInfo = document.createElement('div');
                    var divAppliedEmployeeInfo = $('<div></div>');
    //                divAppliedEmployeeInfo.className = 'div_applied_employee_info';
                    divAppliedEmployeeInfo.attr('class', 'div_applied_employee_info');

    //                    var divAppliedEmployee = document.createElement('div');
                        var divAppliedEmployee = $('<div></div>');
    //                    divAppliedEmployee.className = 'div_applied_employee_str';
                        divAppliedEmployee.attr('class', 'div_applied_employee_str');
    //                    divAppliedEmployee.innerHTML = text;
                        divAppliedEmployee.html(text);

    //                    var input = document.createElement('input');
                        var input = $('<input></input>');
    //                    input.type = "text";
                        input.attr('type', 'text');
    //                    input.value = role_on_project;
                        input.attr('value', role_on_project);
    //                    input.className = "inp_role_on_project";
                        input.attr('class', 'inp_role_on_project');
    //                    input.id = "inp_role_on_project" + id;
                        input.attr('id', "inp_role_on_project" + id);

    //                divAppliedEmployeeInfo.appendChild(divAppliedEmployee);
                    divAppliedEmployeeInfo.append(divAppliedEmployee);
    //                divAppliedEmployeeInfo.appendChild(input);
                    divAppliedEmployeeInfo.append(input);

                    var divStartDayEmployeeOnProject = $('<div></div>');
                    divStartDayEmployeeOnProject.attr('class', 'div_start_day_employee_on_project');


                        var _idStart = 'start_day_employee_on_project' + id;
                        var inputStartDayEmployeeOnProject = $('<input></input>');
                        inputStartDayEmployeeOnProject.attr('type', 'text');
                        inputStartDayEmployeeOnProject.attr('class', 'start_day_employee_on_project');
                        inputStartDayEmployeeOnProject.attr('readonly', 'readonly');
                        inputStartDayEmployeeOnProject.attr('id', _idStart);
                        inputStartDayEmployeeOnProject.attr('value', '');



                        var divAltTextStartDayEmployeeOnProject = $('<div></div>');
                        divAltTextStartDayEmployeeOnProject.attr('class', 'alt_text_start_day_employee_on_project');
                        divAltTextStartDayEmployeeOnProject.html('Дата старта');

                    divStartDayEmployeeOnProject.append(inputStartDayEmployeeOnProject);
                    divStartDayEmployeeOnProject.append(divAltTextStartDayEmployeeOnProject);


                    var divFinishDayEmployeeOnProject = $('<div></div>');
                    divFinishDayEmployeeOnProject.attr('class', 'div_finish_day_employee_on_project');

                        var _idFinish = 'finish_day_employee_on_project' + id;
                        var inputFinishDayEmployeeOnProject = $('<input></input>');
                        inputFinishDayEmployeeOnProject.attr('type', 'text');
                        inputFinishDayEmployeeOnProject.attr('class', 'finish_day_employee_on_project');
                        inputFinishDayEmployeeOnProject.attr('readonly', 'readonly');
                        inputFinishDayEmployeeOnProject.attr('id', _idFinish);
                        inputFinishDayEmployeeOnProject.attr('value', '');

                        var divAltTextFinishDayEmployeeOnProject = $('<div></div>');
                        divAltTextFinishDayEmployeeOnProject.attr('class', 'alt_text_start_day_employee_on_project');
                        divAltTextFinishDayEmployeeOnProject.html('Дата окончания');

                    divFinishDayEmployeeOnProject.append(inputFinishDayEmployeeOnProject);
                    divFinishDayEmployeeOnProject.append(divAltTextFinishDayEmployeeOnProject);


    //                var divDiv_button_refresh_role_real_project = document.createElement('div');
                    var divDiv_button_refresh_role_real_project = $('<div></div>');
    //                divDiv_button_refresh_role_real_project.className = 'div_button_refresh_role_real_project';
                    divDiv_button_refresh_role_real_project.attr('class', 'div_button_refresh_role_real_project');
    //                divDiv_button_refresh_role_real_project.id = 'div_button_refresh_role_real_project' + id;
                    divDiv_button_refresh_role_real_project.attr('id', 'div_button_refresh_role_real_project' + id);
    //                    var imgRefresh = document.createElement('img');
                        var imgRefresh = $('<img></img>');
                        imgRefresh.src = "/static/images/refresh_small.png";
                        imgRefresh.attr('src', "/static/images/refresh_small.png");
    //                divDiv_button_refresh_role_real_project.appendChild(imgRefresh);
                    divDiv_button_refresh_role_real_project.append(imgRefresh);

    //                var divDiv_remove_from_real_project_from_appended = document.createElement('div');
                    var divDiv_remove_from_real_project_from_appended = $('<div></div>');
    //                divDiv_remove_from_real_project_from_appended.className = 'div_remove_from_real_project_from_appended';
                    divDiv_remove_from_real_project_from_appended.attr('class', 'div_remove_from_real_project_from_appended');
    //                divDiv_remove_from_real_project_from_appended.id = 'div_remove_from_real_project_from_appended' + id;
                    divDiv_remove_from_real_project_from_appended.attr('id', 'div_remove_from_real_project_from_appended' + id);
    //                    var imgRemove = document.createElement('img');
                        var imgRemove = $('<img></img>');
    //                    imgRemove.src = '/static/images/cross.png';
                        imgRemove.attr('src', '/static/images/cross.png');
    //                divDiv_remove_from_real_project_from_appended.appendChild(imgRemove);
                    divDiv_remove_from_real_project_from_appended.append(imgRemove);

    //                var divCl = document.createElement('div');
                    var divCl = $('<div></div>');
                    divCl.className = 'cl';
                    divCl.attr('class', 'cl');

    //            li.appendChild(divAppliedEmployeeInfo);
                li.append(divAppliedEmployeeInfo);


    //            li.appendChild(divStartDayEmployeeOnProject);
                li.append(divStartDayEmployeeOnProject);
    //            li.appendChild(divFinishDayEmployeeOnProject);
                li.append(divFinishDayEmployeeOnProject);

    //            li.appendChild(divDiv_button_refresh_role_real_project);
                li.append(divDiv_button_refresh_role_real_project);
    //            li.appendChild(divDiv_remove_from_real_project_from_appended);
                li.append(divDiv_remove_from_real_project_from_appended);
    //            li.appendChild(divCl);
                li.append(divCl);
        //------------------------------------------------------------------------------
    //            var applied_employees = document.getElementById('applied_employees');
                var applied_employees = $('#applied_employees');
        //        applied_employees.appendChild(li);
                var project_appended_employee = $("#project_appended_employee").attr('value');
                var l = DD('l');

                project_appended_employee += id + ",";

                $("#project_appended_employee").attr('value', project_appended_employee);
                
                var idd = $(this).attr('id');
                var projectId = idd.substr('apply_employee_to_real_project'.length);
                
                var data = 
                {
                    "userId": id,
                    "projectId": projectId,
                    "roleOnProject": role_on_project
                };

                $.ajax({
                    type: "POST",
                    url: "/add_employee_to_real_project_project",
                    data: data
                }).done(function(data) {
                    if(
                        typeof data.status !== 'undefined'
                        &&
                        data.status.length === '54194b3f4f452d29551f21cf'.length
                    ) {
                        $("#role_on_project").attr('value', '');
                        selectedEmployee.remove();
    //                    applied_employees.appendChild(li);
                        applied_employees.append(li);


                        $("#" + _idStart).datepicker({
                            showOn: "button",
                            buttonImage: "/static/css/images/calendar.png",
                            dateFormat: "dd/mm/yy",
                            showAnim: "drop",
                            autoSize: true,
                            firstDay: 1,
                            buttonImageOnly: true
                        });

                        $("#" + _idFinish).datepicker({
                            showOn: "button",
                            buttonImage: "/static/css/images/calendar.png",
                            dateFormat: "dd/mm/yy",
                            showAnim: "drop",
                            autoSize: true,
                            firstDay: 1,
                            buttonImageOnly: true
                        });






                    } else {
                        $('#msg_area_project_error').html('Сотрудник не добавлен на проект');
                    }
                });
            } else {
                $('#msg_error_apply_user').html('Заполните роль сотрудника на проекте [больше 5 символов]');
                msg_error_apply_user_bool = true;
            }
        }
    
    
    
    
    
    
    
        
        
        
    });


    $('.div_button_refresh_role_real_project').live('click', function(){
        var l = DD('l');
        l('div_button_refresh_role_real_project CLICK', '');
        var self = this;
        if(typeof $(this).attr('id') !== 'undefined') {
            var id = $(this).attr('id');
            var userId = id.substr('div_button_refresh_role_real_project'.length);
            
            l(userId, 'userId');
            
            var roleOnProject = $('#inp_role_on_project' + userId).attr('value');
                                        
            var startDayOnproject = $('#start_day_employee_on_project' + userId).attr('value');
            var finishDayOnproject = $('#finish_day_employee_on_project' + userId).attr('value');

            l(startDayOnproject, 'startDayOnproject');
            l(finishDayOnproject, 'finishDayOnproject');

            
            
            var id = $('.apply_employee_to_real_project').attr('id');
            var projectId = id.substr('apply_employee_to_real_project'.length);

            $.ajax({
                type: "POST",
                url: "/update_employee_role_on_real_project",
                data: 
                    {
                        'userId': userId,
                        'projectId': projectId,
                        'roleOnProject': roleOnProject,
                        'startDayOnProject': startDayOnproject,
                        'finishDayOnProject': finishDayOnproject,
                    }
            }).done(function(data) {
                if(
                    typeof data['appenderId'] !== 'undefined'
                    &&    
                    typeof data['employeeId'] !== 'undefined'
                    &&    
                    typeof data['roleOnProject'] !== 'undefined'
                    &&    
                    typeof data['finishDayOnProject'] !== 'undefined'
                    &&    
                    typeof data['startDayOnProject'] !== 'undefined'
                    &&    
                    typeof data['status'] !== 'undefined'
                    &&    
                    data['status'] === true
                ) {
                    var employeeId = data['employeeId'];
                    var roleOnProject = data['roleOnProject'];
                    if(typeof $('#inp_role_on_project' + userId) !== 'undefined'
                        && 
                        typeof $('#finish_day_employee_on_project' + userId) !== 'undefined'
                        && 
                        typeof $('#start_day_employee_on_project' + userId) !== 'undefined'
                    ) {

                        var startDayInput = $('#start_day_employee_on_project' + userId);
                        startDayInput.removeClass('unsaved-text-field');
                        startDayInput.addClass('saved-text-field');
                        var finishDayInput = $('#finish_day_employee_on_project' + userId);
                        finishDayInput.removeClass('unsaved-text-field');
                        finishDayInput.addClass('saved-text-field');

                        var inputRoleProject = $('#inp_role_on_project' + userId);
                        inputRoleProject.attr('value', roleOnProject);
                        inputRoleProject.removeClass('unsaved-text-field');
                        inputRoleProject.addClass('saved-text-field');
                        
                        
                        
                        setTimeout(function(self){
                            var id = self.id;
                            var userId = id.substr('div_button_refresh_role_real_project'.length);
                            var inputRoleProject = $('#inp_role_on_project' + userId);
                            inputRoleProject.removeClass('saved-text-field');

                            var startDayInput = $('#start_day_employee_on_project' + userId);
                            startDayInput.removeClass('saved-text-field');
                            var finishDayInput = $('#finish_day_employee_on_project' + userId);
                            finishDayInput.removeClass('saved-text-field');


                        }, 2000, self);
                    }
                }
            });
        }
    });
    
    
    
    setInterval(__, 2000);
    var func = hasNewFilesUploadedFunc();
    function __() {
        func();
    }

    function hasNewFilesUploadedFunc() {
        var ulId = '_ul_uploaded_files_real_project';
        
        var filesNumber = $("#" + ulId).children().length;
    //    l(filesNumber, 'INIT :: filesNumber');
        return function () {
            var _return = $("#" + ulId).children().length === filesNumber;
            filesNumber = $("#" + ulId).children().length;
            var id__ = $('.apply_employee_to_real_project').attr('id');
            
//            l(id__, 'id__');
            
            var projectId = id__.substr('apply_employee_to_real_project'.length);
            
//            l(projectId, 'projectId');

            var data = {
                projectId: projectId
            };

            if(_return === false) {
                l('Ajax');
                 $.ajax({
                    type: "POST",
                    url: "/get_all_uploaded_files_objectids_real_project",
                    data: data
                }).done(function(data) {
                    if(typeof data !== 'undefined'){
                    for(var i in data) {
                        if( window.allUploadedFiles.indexOf(data[i]) >= 0 ) {}
                        else {

                    //        #uploaded_descriptions > ul
                            var objectId = data[i];
                            var ul = $('#uploaded_descriptions > ul');
                            if(typeof ul !== 'undefined') {
                                    var li = $('<li></li>');
                                    li.attr('class', 'li_uploaded_description');
                                    li.attr('id', 'li_uploaded_description_' + objectId);

                                        var div = $('<div></div>');
                                        div.html('Описание файла');
                                        var input = $('<input></input>');
                                        input.attr('class', 'input_uploaded_description');
                                        input.attr('id', 'input_uploaded_description_' + objectId);
                                        input.attr('type', 'text');
                                        input.attr('value', '');

                                        var divButton = $('<div></div>');
                                        divButton.attr('class', 'div_button_update_file_desc_real_project');
                                        divButton.attr('id', 'div_button_update_file_desc_real_project_' + objectId);

                                            var img = $('<img></img>');
                                            img.attr('src', '/static/images/kuba_icon_ok_small.png');

                                        divButton.append(img);

                                    li.append(div);
                                    li.append(input);
                                    li.append(divButton);
                                ul.append(li);
                            }
                        }
                    }
                    }


                });
            }
            return _return;
        };
    }
    
    $('.input_uploaded_description').live('input', function(){
        $(this).addClass('unsaved-text-field');
    });
    
    
    
    

    $('.div_remove_from_real_project_from_appended').live('click', function(){
        l('div_remove_from_real_project_from_appended CLICK', '');
        
        
    });
    
    
    
    
    
    $('.div_button_update_file_desc_real_project').live('click', function(){
        var self = this;
        var id = $(this).attr('id');
        if ( typeof id !== 'undefined' ) {
            var fileId = id.substr('div_button_update_file_desc_real_project_'.length);
            var descrEl = $('#input_uploaded_description_' + fileId);
            if ( typeof descrEl !== 'undefined' ) {
                var description = descrEl.attr('value');
                
                var id = $('.apply_employee_to_real_project').attr('id');
                var projectId = id.substr('apply_employee_to_real_project'.length);
                
                
                $.ajax({
                    type: "POST",
                    url: "/update_file_description_for_real_project",
                    data: 
                        {
                            'projectId': projectId,
                            'fileId': fileId,
                            'description': description,
                        }
                }).done(function(data) { 
                    
                    l(data, 'data');
                    
                    
                    if(
                        typeof data['status'] !== 'undefined'
                        &&
                        typeof data['userId'] !== 'undefined'
                        &&
                        typeof data['fileId'] !== 'undefined'
                        &&
                        typeof data['description'] !== 'undefined'
                    ) {
                        if( data['status'] === true ) { 
                            $('#input_uploaded_description_' + data['fileId']).removeClass('unsaved-text-field');
                            $('#input_uploaded_description_' + data['fileId']).addClass('saved-text-field');
                            
                            
                            setTimeout(function(self){
                                    var id = self.id;
                                    
                                    l(id, 'id');
                                    
                                    var fileId = id.substr('div_button_update_file_desc_real_project_'.length);
                                    
                                    l(fileId, 'fileId')
                                    
                                    var inputRoleProject = $('#input_uploaded_description_' + fileId);
                                    inputRoleProject.removeClass('saved-text-field');
                                }, 2000, self);
                        }
                    }
                    
                    l(data, 'data');
                });
            }
        }
    });


    $('#project_close_div_message').live('click', function(){
        var l = DD('l');
        var id = $('.apply_employee_to_real_project').attr('id');
        var projectId = id.substr('apply_employee_to_real_project'.length);
        
        l(projectId, 'projectId');
        
        var data = {};
        data['projectId'] = projectId;
        $.ajax({
            type: "POST",
            url: "/close_project",
            data: data
        }).done(function(data) {
//            l(data, 'data9076');

        if(typeof data['err'] !== 'undefined') {
            $('#msg_area_project_error').html(data['err']);
            setInterval(function(){
                $('#msg_area_project_error').html('');
            }, 8000);
        }
            if(
                typeof data['closeResult'] !== 'undefined'
            ) {
                if( data['closeResult'] === true ) { 
                    
                    if(
                        typeof data['msg'] !== 'undefined'
                    ) {
                        var msgArea = $('#project_update_div_message');
                        msgArea.html(data['msg']);
                        setTimeout(function(msgArea){
                            msgArea.html('');
                        }, 5000, msgArea);
                    }
                }
            }
    });
    });
    
    
    
    $('#projects_update_project').live('click', function(){
        
        var data = {};

        data['project_name'] = $('#project_name').val();
        data['project_desc'] = $('#project_desc').val();
        data['project_desc_for_customer'] = $('#project_desc_for_customer').val();
        data['customer'] = $('#customer').val();
        data['customer_feedback'] = $('#customer_feedback').val();
        data['service'] = $('#service').val();
        data['industry'] = $('#industry').val();
        data['solution_highlight'] = $('#solution_highlight').val();
        data['development_tools_and_technologies'] = $('#development_tools_and_technologies').val();
        data['development_time'] = $('#development_time').val();
        data['start_date'] = $('#start_date').val();
        data['finish_date'] = $('#finish_date').val();
        data['project_is_in_pause'] = $('#project_is_in_pause').prop('checked');
        
        var id = $('.apply_employee_to_real_project').attr('id');
        var projectId = id.substr('apply_employee_to_real_project'.length);
        data['projectId'] = projectId;
        

        $.ajax({
            type: "POST",
            url: "/update_project",
            data: data
        }).done(function(data) {
//            l(data, 'data9076');

        if(typeof data['err'] !== 'undefined') {
            $('#msg_area_project_error').html(data['err']);
            setInterval(function(){
                $('#msg_area_project_error').html('');
            }, 8000);
        }
            
            if(
                typeof data['updateResult'] !== 'undefined'
            ) {
                if( data['updateResult'] === true ) { 
                    
                    if(
                        typeof data['msg'] !== 'undefined'
                    ) {
                        var msgArea = $('#project_update_div_message');
                        msgArea.html(data['msg']);
                        msgArea.addClass('saved-text-field');

                        setTimeout(function(msgArea){
                            msgArea.removeClass('saved-text-field');

                            setTimeout(function(msgArea){
                                msgArea.html('');
                            }, 2000, msgArea);
                            
                        }, 2000, msgArea);
                    }
                }
            }
        });
    });

    
    
    
});
