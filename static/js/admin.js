$(document).ready(function() {
    //alert('i am ready');
});

window.onload = function() {

};

$('.admin_li_user_block_language_updating').live('click', function(){
    var l = DD('l');
    var id = $(this).attr('id');
    var userId = id.substr('admin_li_user_block_language_updating'.length);

    $.ajax({
        type: "POST",
        url: "/block_language_updating",
        data: {
            'userId': userId
        }
    }).done(function(data) {

        if(
            typeof data['userId'] !== 'undefined'
            &&  
            typeof data['blockResult'] !== 'undefined'    
        ) {
        if(typeof data['blockResult']['updatedExisting'] !== 'undefined') {
            if(data['blockResult']['updatedExisting'] === true) {
                var userId = data['userId'];
//                l(userId, 'userId')
                var objThis = $('#admin_li_user_block_language_updating' + userId);
                var parent = objThis.parent();
                objThis.remove();
                
                
                var obj = $('<div></div>');
                obj.attr('class', 'admin_li_user_unblock_language_updating')
                obj.attr('id', 'admin_li_user_unblock_language_updating' + userId)
                parent.append(obj);
                
                var li = $('#admin_li_user' + userId);
                li.removeClass('open-updating');
                li.addClass('closed-updating');
            }
        }
        }
    });
});




$('.admin_div_button_unblock_editing_skills').live('click', function(){
    var l = DD('l');
    var id = $(this).attr('id');
    
    var userId = id.substr('admin_div_button_unblock_editing_skills'.length);
    
    $.ajax({
        type: "POST",
        url: "/unblock_editing_skills",
        data: {
            'userId': userId
        }
    }).done(function(data) {

        if(
            typeof data['userId'] !== 'undefined'
            &&  
            typeof data['unblockResult'] !== 'undefined'    
        ) {
            if(data['unblockResult'] === true) {

                l(data['unblockResult'], 'data[unblockResult]');
                
                
                var divUnBlockEditingButton = $('#admin_div_button_unblock_editing_skills' + data['userId']);

                var divBlockEditingButton = $('<div></div>');
                divBlockEditingButton.attr('class',   'admin_div_button_block_editing_skills'                   );
                divBlockEditingButton.attr('id'   ,   'admin_div_button_block_editing_skills' + data['userId']  );

                divUnBlockEditingButton.replaceWith(divBlockEditingButton);
            }
        }
    });

});






$('.admin_div_button_block_editing_skills').live('click', function(){
    var l = DD('l');

    var id = $(this).attr('id');
    
    var userId = id.substr('admin_div_button_block_editing_skills'.length);
    
    $.ajax({
        type: "POST",
        url: "/block_editing_skills",
        data: {
            'userId': userId
        }
    }).done(function(data) {

        if(
            typeof data['userId'] !== 'undefined'
            &&  
            typeof data['blockResult'] !== 'undefined'
        ) {
        if(typeof data['blockResult'] !== 'undefined') {
            if(data['blockResult'] === true) {

                var divBlockEditingButton = $('#admin_div_button_block_editing_skills' + data['userId']);

                var divUnBlockEditingButton = $('<div></div>');
                divUnBlockEditingButton.attr('class',   'admin_div_button_unblock_editing_skills'                   );
                divUnBlockEditingButton.attr('id'   ,   'admin_div_button_unblock_editing_skills' + data['userId']  );
                
                divBlockEditingButton.replaceWith(divUnBlockEditingButton);

            }
        }
        }
    });

});





$('.admin_li_user_unblock_language_updating').live('click', function(){
    var l = DD('l');
    var id = $(this).attr('id');
    var userId = id.substr('admin_li_user_unblock_language_updating'.length);

    $.ajax({
        type: "POST",
        url: "/unblock_language_updating",
        data: {
            'userId': userId
        }
    }).done(function(data, textStatus, jqXHR) {
//
//        l(data, 'data');
//        l(textStatus, 'textStatus');
//        l(jqXHR, 'jqXHR');

        if(
            typeof data['userId'] !== 'undefined'
            &&  
            typeof data['unblockResult'] !== 'undefined'
        ) {
        if( 
            typeof data['unblockResult']['updatedExisting'] !== 'undefined'
        ) {
            if(data['unblockResult']['updatedExisting'] === true) {

                var userId = data['userId'];
                var objThis = $('#admin_li_user_unblock_language_updating' + userId);
                var parent = objThis.parent();
                objThis.remove();
                
                
                var obj = $('<div></div>');
                obj.attr('class', 'admin_li_user_block_language_updating')
                obj.attr('id', 'admin_li_user_block_language_updating' + userId)
                parent.append(obj);
                
                
                var li = $('#admin_li_user' + userId);

                li.removeClass('closed-updating');
                li.addClass('open-updating');
//                li.removeClass('closed-updating')
                
                
            }
        }
        }
    });
});
