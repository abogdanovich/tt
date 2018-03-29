
var lastSentEmployes = '';
$(document).ready(function() {
var msg_error_apply_user_bool = false;
var msg_area_project_error_bool = false;
var l = DD('l');


$('.div_button_update_file_desc').live('click', function(){
    var id = $(this).attr('id');
    if ( typeof id !== 'undefined' ) {
        var fileId = id.substr('div_button_update_file_desc_'.length);
        var descrEl = $('#input_uploaded_description_' + fileId);
        if ( typeof descrEl !== 'undefined' ) {
            var description = descrEl.attr('value');
            $.ajax({
                type: "POST",
                url: "/update_file_description_for_empty_project",
                data: 
                    {
                        'fileId': fileId,
                        'description': description,
                    }
            }).done(function(data) {
                
                /*
                    description: "фываывав"
                    fileId: "541993d14f452d58f69cf082"
                    n: 1
                    nModified: 1
                    ok: 1
                    updatedExisting: true
                    userId: 283
                 */
                
                l(data, 'data')
                if (
                    typeof data['description'] !== 'undefined'
                    &&
                    typeof data['fileId'] !== 'undefined'
                    &&
                    typeof data['updatedExisting'] !== 'undefined'
                ) {
            
                    
                    // input_uploaded_description_541993d14f452d58f69cf082
                    var input = $('#input_uploaded_description_' + data['fileId']);
                    
                    l(input, 'input');
                    
                    input.html(data['description']);
                    input.removeClass('unsaved-text-field');
                    input.addClass('saved-text-field');
                    
                    
                    
                    setTimeout(function(input){
                            input.removeClass('saved-text-field');
                        }, 2000, input);
                    
                    
                
                    l(data, 'data');
                }
            });
        }
    }
    
    
});
    
    




$("#start_date").datepicker({
	showOn: "button",
	buttonImage: "/static/css/images/calendar.png",
	dateFormat: "dd/mm/yy",
	showAnim: "drop",
	autoSize: true,
	firstDay: 1,
	buttonImageOnly: true
});


$("#finish_date").datepicker({
	showOn: "button",
	buttonImage: "/static/css/images/calendar.png",
	dateFormat: "dd/mm/yy",
	showAnim: "drop",
	autoSize: true,
	firstDay: 1,
	buttonImageOnly: true
});






$('.div_remove_from_appended').live('click', function(){
    console.log('div_remove_from_appended()');
    if(typeof $(this).attr('id') !== 'undefined') {
        var id = $(this).attr('id');
        var userId = id.substr('div_remove_from_appended'.length);

        if(typeof allUsers !== 'undefined') {
            if(typeof allUsers[userId] !== 'undefined') {
                $.ajax({
                    type: "POST",
                    url: "/remove_employee_from_empty_project",
                    data: 
                        {
                            'userId': userId, 
                        }
                }).done(function(data) {
                    if(typeof data['removeStatus'] !== 'undefined') {
                        if(data['removeStatus'] == true && false    ) {
                            var user = allUsers[userId];
                            var ord = user.order - 1;
                            var upUser = null;
                            while(ord >= 0) {
                                if(typeof allUsersByOrder[ord] !== 'undefined' ) {
                                    var _ = allUsersByOrder[ord];

                                    for(ip in notAppliedOnProjectEmployee) {
                                        if(notAppliedOnProjectEmployee[ip].userId === _.id) {
                                            upUser = notAppliedOnProjectEmployee[ip];
                                            ord = -1;
                                            break;
                                        }
                                    }
                                    notAppliedOnProjectEmployee[ord];
                                }
                                ord--;
                            }
                                var newOption = $('<option></option>');
                                newOption.attr('value', user.id);
                                newOption.attr('id', "employee_" + user.id);
                                newOption.html(user.name + '&nbsp;' + user.surname);
                            if(upUser !== null) {
                                var option = $('select#employee > option#employee_' + upUser.userId);
                                newOption.insertAfter(option);
            //                    option.insertAfter(newOption);
                            } else {
                                $("select#employee").prepend(newOption);
                            }
                            $('li#li_appended_employee' + userId).remove();
                        }
                    }
                });
            }
        }
    }
});

$('.div_button_refresh_role').live('click', function(){
    var self = this;
    if(typeof $(this).attr('id') !== 'undefined') {
        var id = $(this).attr('id');
        var userId = id.substr('div_button_refresh_role'.length);
        var roleOnProject = $('#inp_role_on_project' + userId).attr('value');
        var startDayOnproject = $('#start_day_employee_on_project' + userId).attr('value');
        var finishDayOnproject = $('#finish_day_employee_on_project' + userId).attr('value');
        
        var l = DD('l');
        
        $.ajax({
            type: "POST",
            url: "/update_employee_role_on_empty_project",
            data: 
                {
                    'userId': userId, 
                    'roleOnProject': roleOnProject,
                    'startDayOnProject': startDayOnproject,
                    'finishDayOnProject': finishDayOnproject,
                }
        }).done(function(data) {
            if(typeof data !== 'undefined') {
                if(typeof data !== 'undefined') {
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
                    ) {
                        if(data['status'] == true) {
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
                                    var userId = id.substr('div_button_refresh_role'.length);
                                    var inputRoleProject = $('#inp_role_on_project' + userId);
                                    inputRoleProject.removeClass('saved-text-field');

                                    var startDayInput = $('#start_day_employee_on_project' + userId);
                                    startDayInput.removeClass('saved-text-field');
                                    var finishDayInput = $('#finish_day_employee_on_project' + userId);
                                    finishDayInput.removeClass('saved-text-field');


                                }, 2000, self);
                            }
                        }
                    }
                }
            }
        });
    }
});

$('.start_day_employee_on_project').live('change', function(){
    $(this).addClass('unsaved-text-field');
});

$('.finish_day_employee_on_project').live('change', function(){
    $(this).addClass('unsaved-text-field');
});

$('.inp_role_on_project').live('input', function(){
    $(this).addClass('unsaved-text-field');
});

$('.input_uploaded_description').live('input', function(){
    $(this).addClass('unsaved-text-field');
});

$('#projects_add_project').click(function(){//send_main_form
//    $('#add_new_project').click();
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
    
    $.ajax({
        type: "POST",
        url: "/add_project",
        data: data
    }).done(function(resultData) {

        if(typeof resultData['err'] !== 'undefined') {
            $('#msg_area_project_error').html(resultData['err']);
            setInterval(function(){
                $('#msg_area_project_error').html('');
            }, 8000);
        }

        if(typeof resultData['addResult'] !== 'undefined') {
        if(resultData['addResult'] === true) {
            
            if(typeof resultData['msg'] !== 'undefined') {
                var msg = resultData['msg'];
                
                $('#msg_area_project').html(msg);
                
                setInterval(function(){
                    var l = DD('l');
                    $('#msg_area_project').html('');
                    l('clearing');
                }, 8000);

                
                //msg_area_project_error
                //msg_area_project
                //msg_hidden_project_create
            }
        }
        }
    });

});



var last_message_area_project = '';
function  refreshForm() {
    var html = $('#msg_area_project').html();
    if(html !== '' && last_message_area_project !== html) {
        l = DD('l');

        last_message_area_project = html;
        
        
        $('#uploaded_descriptions > ul').empty();
        $('#applied_employees').empty();
        $('#___ul_uploaded_files').empty();
        $('#project_name').attr('value', '');
        $('#project_desc').attr('value', '');
        $('#project_desc_for_customer').attr('value', '');
        $('#customer_feedback').attr('value', '');
        $('#service').attr('value', '');
        $('#industry').attr('value', '');
        $('#solution_highlight').attr('value', '');
        $('#development_tools_and_technologies').attr('value', '');
        $('#development_time').attr('value', '');
        $('#start_date').attr('value', '');
        $('#finish_date').attr('value', '');
//        $('#project_is_in_pause').attr('value', '');



        var notAppliedOnProjectEmployee = window.notAppliedOnProjectEmployee;
        var allUsers = window.allUsers;

        notAppliedOnProjectEmployee = [];

        for(var i in allUsers) {
            notAppliedOnProjectEmployee[allUsers[i].order] = {
                'userId': allUsers[i].id,
                'order': allUsers[i].order,
                'name': allUsers[i].name,
                'surname': allUsers[i].surname,
            };
        }
        
        //<option value="148" id="employee_148">пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ&nbsp;пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ</option>
        var newOptions = [];
        for(i in notAppliedOnProjectEmployee) {
            var option = $('<option></option>');
            option.attr('value', notAppliedOnProjectEmployee[i].userId);
            option.attr('id', "employee_" + notAppliedOnProjectEmployee[i].userId);
            option.html(notAppliedOnProjectEmployee[i].name + "&nbsp;" + notAppliedOnProjectEmployee[i].surname);
            newOptions[i] = option;
        }
        
        var selectBox = $('#employee');
        selectBox.empty();

        for(i in newOptions) {
            selectBox.append(newOptions[i]);
        }
    }

}


setInterval(refreshForm, 2000);
setInterval(_clearProccess, 3000);




setInterval(__, 2000);
var func = hasNewFilesUploadedFunc();
function __() {
    func();
}

function hasNewFilesUploadedFunc() {
    var filesNumber = $("#___ul_uploaded_files").children().length;
//    l(filesNumber, 'INIT :: filesNumber');
    return function () { 
        var _return = $("#___ul_uploaded_files").children().length === filesNumber;
        filesNumber = $("#___ul_uploaded_files").children().length;
        
        if(_return === false) {
             $.ajax({
                type: "POST",
                url: "/get_all_uploaded_files_objectids",
                data: _
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
                                    divButton.attr('class', 'div_button_update_file_desc');
                                    divButton.attr('id', 'div_button_update_file_desc_' + objectId);

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

function _clearProccess() {
   
    if(msg_error_apply_user_bool === true) {
        msg_error_apply_user_bool = false;
    } else {
        $('#msg_error_apply_user').html('');
        msg_error_apply_user_bool = true;
    }
}

$("#apply_employee_to_project").click(function(){
    l = DD('l');
    l('apply_employee_to_project()');
    
    
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
               

//                var divDiv_button_refresh_role = document.createElement('div');
                var divDiv_button_refresh_role = $('<div></div>');
//                divDiv_button_refresh_role.className = 'div_button_refresh_role';
                divDiv_button_refresh_role.attr('class', 'div_button_refresh_role');
//                divDiv_button_refresh_role.id = 'div_button_refresh_role' + id;
                divDiv_button_refresh_role.attr('id', 'div_button_refresh_role' + id);
//                    var imgRefresh = document.createElement('img');
                    var imgRefresh = $('<img></img>');
                    imgRefresh.src = "/static/images/refresh_small.png";
                    imgRefresh.attr('src', "/static/images/refresh_small.png");
//                divDiv_button_refresh_role.appendChild(imgRefresh);
                divDiv_button_refresh_role.append(imgRefresh);

//                var divDiv_remove_from_appended = document.createElement('div');
                var divDiv_remove_from_appended = $('<div></div>');
//                divDiv_remove_from_appended.className = 'div_remove_from_appended';
                divDiv_remove_from_appended.attr('class', 'div_remove_from_appended');
//                divDiv_remove_from_appended.id = 'div_remove_from_appended' + id;
                divDiv_remove_from_appended.attr('id', 'div_remove_from_appended' + id);
//                    var imgRemove = document.createElement('img');
                    var imgRemove = $('<img></img>');
//                    imgRemove.src = '/static/images/cross.png';
                    imgRemove.attr('src', '/static/images/cross.png');
//                divDiv_remove_from_appended.appendChild(imgRemove);
                divDiv_remove_from_appended.append(imgRemove);

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
            
//            li.appendChild(divDiv_button_refresh_role);
            li.append(divDiv_button_refresh_role);
//            li.appendChild(divDiv_remove_from_appended);
            li.append(divDiv_remove_from_appended);
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

            var _ = {"userId": id, "roleOnProject": role_on_project};

            $.ajax({
                type: "POST",
                url: "/add_employee_to_project",
                data: _
            }).done(function(data) {
                if(data[0].status !== 'None') {
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
                     setInterval(function(){
                        $('#msg_area_project_error').html('');
                    }, 3000);
                }
            });
        } else {
            $('#msg_error_apply_user').html('Заполните роль сотрудника на проекте [больше 5 символов]');
            msg_error_apply_user_bool = true;
        }
    }
});
//update_employee_role_on_empty_project
});
