$(document).ready(function() {
    var l = DD('l');
    
    var allStartDaysOnProject = $('.my_projects_startDay_roleId');
    var allFinishDaysOnProject = $('.my_projects_finishDay_roleId');

    $.each(allStartDaysOnProject, function(index, obj){
        var id = obj.id;
        $("#" + id).datepicker({
           showOn: "button",
           buttonImage: "/static/css/images/calendar.png",
           dateFormat: "dd/mm/yy",
           showAnim: "drop",
           autoSize: true,
           firstDay: 1,
           buttonImageOnly: true
        });
    });

    $.each(allFinishDaysOnProject, function(index, obj){        
        var id = obj.id;
        $("#" + id).datepicker({
           showOn: "button",
           buttonImage: "/static/css/images/calendar.png",
           dateFormat: "dd/mm/yy",
           showAnim: "drop",
           autoSize: true,
           firstDay: 1,
           buttonImageOnly: true
        });
    });

    $('.my_projects_startDay_roleId').live('change', function(){
        $(this).addClass('unsaved-text-field');
    });

    $('.my_projects_finishDay_roleId').live('change', function(){
        $(this).addClass('unsaved-text-field');
    });


    $('.my_projects_update_work_period_on_project').live('click', function(){
        var l = DD('l');
        var data = {};
        var id = $(this).attr('id');       
        var projectRoleId = id.substr('my_projects_update_work_period_on_project'.length);
        var startDate = $('#my_projects_startDay_roleId' + projectRoleId).val();
        var finishDate = $('#my_projects_finishDay_roleId' + projectRoleId).val();
        
        data['projectRoleId'] = projectRoleId;
        data['startDate'] = startDate;
        data['finishDate'] = finishDate;
        
        $.ajax({
            type: "POST",
            url: "/update_work_period_on_project",
            data: data
        }).done(function(resultData) {
            if(
                typeof resultData['updateResult'] !== 'undefined'
                &&
                typeof resultData['projectRoleId'] !== 'undefined'
                &&
                typeof resultData['finishDate'] !== 'undefined'
                &&
                typeof resultData['startDate'] !== 'undefined'
            ) {
            if(resultData['updateResult'] === true) {
                var startDate = resultData['startDate'];
                var finishDate = resultData['finishDate'];
                
                var projectRoleId = resultData['projectRoleId'];
                var startDayInput = $('#my_projects_startDay_roleId' + projectRoleId)
                
                startDayInput.val(startDate);
                startDayInput.removeClass('unsaved-text-field');
                
                
                var finishDayInput = $('#my_projects_finishDay_roleId' + projectRoleId)
                finishDayInput.val(finishDate);
                finishDayInput.removeClass('unsaved-text-field');
                
            }
            }
        });
        
        
        
    })


    
    
});



