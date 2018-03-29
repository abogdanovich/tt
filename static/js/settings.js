$(document).ready(function() {
    //alert('i am ready');
});


window.onload = function() {
    
    var theThing = null;
    var replaceThing = function () {
        var priorThing = theThing;
        var unused = function () {
            // 'unused' - ������������ �����, ��� ������������ 'priorThing',
            // �� 'unused' ������� �� ����������
            if (priorThing) {
                console.log("hi");
            }
        };
        theThing = {
            longStr: new Array(1000000).join('*'),  // ������� 1M� ������
            someMethod: function () {
                console.log(someMessage);
            }
        };
    };
    
    
  // TODO: Add info about user to js TO make buttons disabled.

//    $('.mb-add-button').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: "/get_all_user_languages",
    }).done(function(data) {
//        l(data,'COMEBACK data');
        if( typeof data['allUserLanguages'] !== 'undefined') {
            var ul = $('ul.mb-taglist');
            
//            l(ul, 'ul');
            
            for(var i in data['allUserLanguages']) {
                var lang = data['allUserLanguages'][i];
//                l(lang['language_id'], 'lang[language_id]');
                
                var skillsObj = {
                    'language_spoken_skills_value': lang['language_spoken_skills_value'],
                    'language_written_skills_value': lang['language_written_skills_value'],
                };
                
                
//                l(skillsObj, 'skillsObj');
                var li = undefined;
                var divWrapper = 
                        createDivWrapper(
                            lang['language_id'],
                            lang['name'],
                            li, 
                            skillsObj
                        );
                ul.append(divWrapper);
                
                //option_lang_id_53ff06bc019442a2e3e9c2e5
                var option = $('select.mb-input > #option_lang_id_' + lang['language_id']);
                
//                l(option, 'option');
                
//                option.parentNode.removeChild(option);
                
                option.remove();
            }
        }
//        l(data, 'data');
        $('.mb-add-button').removeAttr('disabled');
    });
};










$('.settings_input_skill_description').live('input', function(){
    $(this).addClass('red_color');
});

$('.settings_div_remove_skill').live('click', function(){
    var l = DD('l');
    var id = $(this).attr('id');
    var skillId = id.substr('settings_div_remove_skill'.length);
    l(skillId, 'skillId');
    
    $.ajax({
        type: "POST",
        url: "/remove_skill",
        data: {
            'skillId': skillId
        }
    }).done(function(data) {
//        l(data, 'data');
        if(typeof data['removeResult'] !== 'undefined'
            &&
            typeof data['skillId'] !== 'undefined'
            &&
            typeof data['skillName'] !== 'undefined'
        ) {
        if(data['removeResult'] === true) {
            
            var deletedSkill = $('#settings_div_set_skill_element' + data['skillId']);
            deletedSkill.remove();
            
            
            var deletedOption = $('<option></option>');
            deletedOption.attr('id', 'option_skill_id_' + data['skillId']);
            deletedOption.attr('value', data['skillName']);
            deletedOption.attr('class', 'option_skill_id_');
            deletedOption.html(data['skillName']);
            
            var selectBox = $('#settings_input_skills');
            selectBox.append(deletedOption);
            
            
        }
        }
    });
    
    
});

$('.settings_update_skill').live('click', function(){
    var l = DD('l');
    
    
    var id = $(this).attr('id');
    var skillId = id.substr('settings_update_skill'.length);
//    l(skillId, 'skillId');
    var descriptionElement = $('#settings_input_skill_description' + skillId);
    var description = descriptionElement.attr('value');
    
    $.ajax({
        type: "POST",
        url: "/update_skill_to_user",
        data: {
            'skillId': skillId,
            'description': description
        }
    }).done(function(data) {
//        l(data, 'data');
        if(typeof data['updateResult'] !== 'undefined'
            &&
            typeof data['skillId'] !== 'undefined'
            &&
            typeof data['skillName'] !== 'undefined'
        ) {
        if(data['updateResult'] === true) {
            var textArea = $('#settings_input_skill_description' + data['skillId']);
            
            textArea.removeClass('red_color');
            textArea.addClass('green_color');
            
            setTimeout(function(textArea){
                textArea.removeClass('green_color');
            }, 3000, textArea);
        }
        }
    });
    
    
});

$('.settings_div_remove_position').live('click', function(){
    var l = DD('l');
//    l('settings_div_remove_position');
    
    var id = $(this).attr('id');
    var positionId = id.substr('settings_div_remove_position'.length);

    l(positionId, 'positionId');

    $.ajax({
        type: "POST",
        url: "/remove_position_from_user",
        data: {
            'positionId': positionId
        }
    }).done(function(data) {
        if(
            typeof data['removeResult'] !== 'undefined'
            &&
            typeof data['positionId'] !== 'undefined'
            &&
            typeof data['positionName'] !== 'undefined'
        ) {
            if( data['removeResult'] === true ) {
                var removedDiv = $('#settings_div_position' + data['positionId'])
                removedDiv.remove();
                
                l(data['positionName'], 'data[positionName]');

                var option = $('<option></option>');
                option.attr('id', 'settings_select_position_option' + data['positionId']);
                option.attr('value', 'settings_select_position_option' + data['positionId']);
                option.html(data['positionName']);

                var selectBox = $('#settings_select_position');
                selectBox.append(option);
                
            }
        }
    });
    
});



$('.checkbox_in_position_in_project').live('click', function(){
    var l = DD('l');
    l('checkbox_in_position_in_project');
    
    var id = $(this).attr('id');
    var positionId = id.substr('checkbox_in_position_in_project'.length);

//    $(this).prop('checked');
    var checkBoxSet = $(this).prop('checked');
    var action = '';
    switch(checkBoxSet) {
        case true: action = 'set'; break;
        case false: action = 'unset'; break;
    }
    if(action !== '') {
        $.ajax({
            type: "POST",
            url: "/show_position_on_main_page",
            data: 
                {
                    'action': action,
                    'positionId':positionId,
                }
        }).done(function(data) {

        });
    }
    
});




$('.settings_add_position').live('click', function(){
    var l = DD('l');
    var selectedOption = $('#settings_select_position :selected');
    var id = selectedOption.val();
    var positionId = id.substr('settings_select_position_option'.length);
//    l(positionId, 'positionId');

    $.ajax({
        type: "POST",
        url: "/add_position_to_user",
        data: {
            'positionId': positionId
        }
    }).done(function(data) {
        if(
            typeof data['addResult'] !== 'undefined'
            &&
            typeof data['positionId'] !== 'undefined'
            &&
            typeof data['positionName'] !== 'undefined'
        ) {
            if( data['addResult'] === true ) {
                
                var container = $('#settings_div_container_positions');
                
                    var div = $('<div></div>');
                    div.addClass('settings_div_position');
                    div.attr('id', 'settings_div_position' + data['positionId']);

                        var divText = $('<div></div>');
                        divText.addClass('settings_div_text_position_name');
                        divText.html(data['positionName']);
                        
                        
                        
//                        <div
//                               class="settings_div_checkbox"
//                        >
//                            <input 
//                                type="checkbox"
//                                class="checkbox_in_position_in_project"
//                                id="checkbox_in_position_in_project541be4324f452d1f3a16b6ac"
//                                checked="checked"
//                            >В проектах
//                        </div>

                        var divCheckBox = $('<div></div>');
                        divCheckBox.addClass('settings_div_checkbox');
                            var inputCheckBox = $('<input></input>');
                            inputCheckBox.attr('id', 'checkbox_in_position_in_project' + data['positionId']);
                            inputCheckBox.attr('type', 'checkbox');
                            inputCheckBox.attr('checked', 'checked');
                            inputCheckBox.addClass('checkbox_in_position_in_project');
                        divCheckBox.append(inputCheckBox);
                        divCheckBox.append('В проектах');
                        
                        
                        
                        
                        

                        var divRemovePosition = $('<div></div>');
                        divRemovePosition.addClass('settings_div_remove_position');
                        divRemovePosition.attr('id', 'settings_div_remove_position' + data['positionId']);
                        

                        var divCl = $('<div></div>');
                        divCl.addClass('cl');

                    div.append(divText);
                    div.append(divCheckBox);
                    div.append(divRemovePosition);
                    div.append(divCl);
                container.append(div);
                
                
                
                

                var idd = '#settings_select_position_option' + data['positionId'];
                
                l(idd, 'idd');
                var deletedOption = $(idd);

                l(deletedOption, 'deletedOption')
                deletedOption.remove();
            }
        }
        
    });
    
    
    
});

$('.add_skill_to_user').live('click', function(){
    var l = DD('l');
    var selectedOption = $('#settings_input_skills :selected');
    var id = selectedOption.attr('id');
    var skillId = id.substr('option_skill_id_'.length);


    $.ajax({
        type: "POST",
        url: "/add_skill_to_user",
        data: {
            'skillId': skillId
        }
    }).done(function(data) {
        if(typeof data['addResult'] !== 'undefined'
            &&
            typeof data['skillId'] !== 'undefined'
            &&
            typeof data['skillName'] !== 'undefined'
            &&
            typeof data['skillDescription'] !== 'undefined'
        ) {
        if(data['addResult'].length === '54058ff092e604049cc23123'.length) {
            var skillId = data['skillId'];
            var skillName = data['skillName'];
            var skillDescription = data['skillDescription'];
            
            if(skillName.toString() === '') {
                skillName = '[NONAME SKILL]';
            }

            var selectedOption = $('#option_skill_id_' + skillId);
            if(selectedOption !== undefined) {
                selectedOption.remove();
            }

            var divSkill = $('<div></div>');
            divSkill.attr('class', 'settings_div_set_skill_element');
            divSkill.attr('id', 'settings_div_set_skill_element' + skillId);
                var divSkillName = $('<div></div>');
                divSkillName.attr('class', 'settings_div_skill_name');
                    var headerThree = $('<h3></h3>');
                    headerThree.html(skillName);
                divSkillName.append(headerThree);
                
                
                var divRemoveSkillBlock = $('<div></div>');
                divRemoveSkillBlock.attr('class', 'settings_div_remove_skill');
                divRemoveSkillBlock.attr('id', 'settings_div_remove_skill' + skillId);
                    var imgCross = $('<img></img>');
                    imgCross.attr('src', '/static/images/cross.png');
                divRemoveSkillBlock.append(imgCross);
                
                
                var divSkillDescription = $('<div></div>');
                divSkillDescription.attr('class', 'settings_div_skill_description');
                    var textarea = $('<textarea></textarea>');
                    textarea.attr('class', 'settings_input_skill_description');
                    textarea.attr('id', 'settings_input_skill_description' + skillId);
                    textarea.html(skillDescription);
                divSkillDescription.append(textarea);
                
                
                
                /*
                    <div
                        class="settings_div_checkbox_show_on_main_page" 
                        id="settings_div_checkbox_show_on_main_page54048223d567345ce1f2a70a"
                    >
                        <input 
                            type="checkbox" 
                            class="settings_checkbox_show_on_main_page" 
                            id="settings_checkbox_show_on_main_page54048223d567345ce1f2a70a" 
                            checked=""
                        >
                        <label 
                            for="settings_checkbox_show_on_main_page54048223d567345ce1f2a70a"
                        >
                        �� �������</label>
                    </div>

                */
                var divSkillShowOnMainPage = $('<div></div>');
                divSkillShowOnMainPage.attr('class', 'settings_div_checkbox_show_on_main_page');
                divSkillShowOnMainPage.attr('id', 'settings_div_checkbox_show_on_main_page' + skillId);
                    var checkBox = $('<input></input>');
                    checkBox.attr('type', 'checkBox');
                    checkBox.attr('class', 'settings_checkbox_show_on_main_page');
                    var chBoxId = 'settings_checkbox_show_on_main_page' + skillId;
                    checkBox.attr('id', chBoxId);
                    checkBox.attr('checked', false);
                    
                    var labelForCheckBox = $('<label></label>');
                    labelForCheckBox.attr('for', chBoxId);
                    labelForCheckBox.html('На главной');
                divSkillShowOnMainPage.append(checkBox);
                divSkillShowOnMainPage.append(labelForCheckBox);
                    
                    
               
               
               
                
                var divSkillUpdateSkillBlock = $('<div></div>');
                divSkillUpdateSkillBlock.attr('class', 'settings_update_skill');
                divSkillUpdateSkillBlock.attr('id', 'settings_update_skill' + skillId);
                    var img = $('<img></img>');
                    img.attr('src', '/static/images/kuba_icon_ok_small.png');
                divSkillUpdateSkillBlock.append(img);

            divSkill.append(divSkillName);
            divSkill.append(divRemoveSkillBlock);
            divSkill.append(divSkillDescription);
            divSkill.append(divSkillShowOnMainPage);
            divSkill.append(divSkillUpdateSkillBlock);

            var lastSkillAdded = $('#settings_div_set_skills_elements > .settings_div_set_skill_element :last');
            var lastSkillAddedId = lastSkillAdded.attr('id');
            var lastSkillAddedId = lastSkillAdded.attr('class');
            
            l(lastSkillAddedId, 'lastSkillAddedId');
            
            
            
            if(lastSkillAddedId === undefined) {
                var container = $('#settings_div_set_skills_elements');
                container.append(divSkill);
                var divCl = $('<div></div>');
                divCl.attr('class', 'cl');
                container.append(divCl);
            } else {
                divSkill.insertAfter(lastSkillAdded);
            }
            
            
//            var skillsElement = $('#settings_div_set_skills_elements > .settings_div_set_skill_element :last');
//            skillsElement.append(divSkill);
            
        }
        }
    });
    
    
});


$('.mb_input').live('change', function(){
//    $(this).children(':selected').addClass('red_color');
    $(this).addClass('red_color');
})


$('.mb_tag_remove').live('click', function(){
//    var arr = [ "one", "two", "three", "four", "five" ];
//    $.each(arr, function(index, value) {
//       l(index, 'index');
//       l(value, 'value');
//   });

    var li = $(this).parent().parent();
    var divWrapper = li.parent();

    var _ = li.attr('id');
    var language_id = _.substr('li-language-'.length);

    $.ajax({
        type: "POST",
        url: "/remove_user_language",
        data: {
            'language_id': language_id
        }
    }).done(function(data) {
        if(typeof data['removeResult'] !== 'undefined'
            &&
            typeof data['language_id'] !== 'undefined'
            &&
            typeof data['language_name'] !== 'undefined'
        ) {
        if(data['removeResult'] === 1) {
            var language_id = data['language_id'];
            var divWrapper = $('#li-language-' + language_id).parent();
            divWrapper.remove();

            var optionLang = $('<option></option>');
            optionLang.attr('id', 'option_lang_id_' + language_id);
            optionLang.attr('value', data['language_name']);
            optionLang.html(data['language_name']);

            var select = $('select.mb-input');
            select.append(optionLang);
        }
        }
    });
});


$('.settings_checkbox_show_on_main_page').live('change', function(){
    
    var id = $(this).attr('id');
    var skillId = id.substr('settings_checkbox_show_on_main_page'.length);

//    $(this).prop('checked');
    var checkBoxSet = $(this).prop('checked');
    var action = '';
    switch(checkBoxSet) {
        case true: action = 'set'; break;
        case false: action = 'unset'; break;
    }
    $.ajax({
        type: "POST",
        url: "/showing_skill_on_main_page",
        data: 
            {
                'action': action,
                'skillId':skillId,
            }
    }).done(function(data) {
        if(
            typeof data['action'] !== 'undefined'
            &&
            typeof data['actionResult'] !== 'undefined'
            &&
            typeof data['skillId'] !== 'undefined'
        ) {
        if(data['actionResult'] === false) {
            var chBox = $('#settings_checkbox_show_on_main_page' + data['skillId']);
            switch(data['action']) {
                case 'set':
                    chBox.prop('checked', false);
                    break;
                case 'unset':
                    chBox.prop('checked', true);
                    break;
            }
        }
        }
    });
});


$('.div-button-save-language').live('click', function(){
   var id = $(this).attr('id');
   var selectedLanguageId = id.substr('div-button-save-language-'.length);
   
   var writtenSkillsOption = $('#choosen_language_written_' + selectedLanguageId + ' option:selected');
   var writtenSkillsValue = writtenSkillsOption.attr('value');
   
   var spokenSkillsOption = $('#choosen_language_spoken_' + selectedLanguageId + ' option:selected');
   var spokenSkillsValue = spokenSkillsOption.attr('value');

    $.ajax({
        type: "POST",
        url: "/update_user_language",
        data: 
            {
                'languageId':selectedLanguageId,
                'writtenSkillsValue':writtenSkillsValue,
                'spokenSkillsValue':spokenSkillsValue,
            }
    }).done(function(data) {
        if(
            typeof data['updateResult'] !== 'undefined'
            &&
            typeof data['language_id'] !== 'undefined'
        ) {
        if(data['updateResult'] === 1) {
//            l(data['updateResult'], 'data[updateResult]');
            var language_id = data['language_id'];
            var select = $('#choosen_language_spoken_' + language_id);
            select.removeClass('red_color');
            var select = $('#choosen_language_written_' + language_id);
            select.removeClass('red_color');
        }
        }
//        l(data, 'data');
    });
});

$( "#settings_input_languages" ).masterblaster( {
    animate: true
} );


function createDivWrapper(selectedLanguageId, nameSelectedLanguage, li, skillsObj) {

//    l(nameSelectedLanguage, 'nameSelectedLanguage');
    if (nameSelectedLanguage === undefined){
        if( li !== undefined ) {
            li.remove();
        }
    } else {
        if(typeof nameSelectedLanguage === 'string') {
            li = $('<li></li>');
            li.css('opacity', 1);
            li.attr('data-tag', nameSelectedLanguage.toString());
            li.attr('class', "mb-tag");
            li.attr('id', 'li-language-' + selectedLanguageId);
                var divMbTagContent = $('<div></div>');
                divMbTagContent.attr('class', "mb-tag-content");

                    var spanTagText = $('<span></span>');
                    spanTagText.attr('class', 'mb-tag-text');
                    spanTagText.html(nameSelectedLanguage);

                    var aTagRemove = $('<a></a>');
                    aTagRemove.attr('class', 'mb_tag_remove');

                divMbTagContent.append(spanTagText);
                divMbTagContent.append(aTagRemove);

            li.append(divMbTagContent);
        } else {}
    }
    
    
            var divCl = $('<div></div>');
                divCl.attr('class', 'cl');

               var divWrapper = $('<div></div>');
               divWrapper.attr('class', 'div_li_wrapper');
                   var divWrittenLangSkills = $('<div></div>');
                   divWrittenLangSkills.attr('class', 'settings_div_select_lang_skills');
                   divWrittenLangSkills.html('Written');

                   var selectWritten =  $('<select></select>');
                   selectWritten.attr('class', 'mb_input');
                   selectWritten.attr('id', 'choosen_language_written_' + selectedLanguageId);

                       var optionWrittenNone = $('<option></option>');
                       optionWrittenNone.attr('value', '0');
                       optionWrittenNone.addClass('color_black');
                       optionWrittenNone.html('None');

                       var optionWrittenBasic = $('<option></option>');
                       optionWrittenBasic.addClass('color_black');
                       optionWrittenBasic.attr('value', '1');
                       optionWrittenBasic.html('Basic');

                       var optionWrittenAdvanced = $('<option></option>');
                       optionWrittenAdvanced.addClass('color_black');
                       optionWrittenAdvanced.attr('value', '2');
                       optionWrittenAdvanced.html('Advanced');

                       var optionWrittenFluent = $('<option></option>');
                       optionWrittenFluent.addClass('color_black');
                       optionWrittenFluent.attr('value', '3');
                       optionWrittenFluent.html('Fluent');

           //            l(optionWrittenFluent.attr('value'), 'optionWrittenFluent.attr(\'value\')');

                   selectWritten.append(optionWrittenNone);
                   selectWritten.append(optionWrittenBasic);
                   selectWritten.append(optionWrittenAdvanced);
                   selectWritten.append(optionWrittenFluent);
                   
                   if(typeof skillsObj !== 'undefined') {
                       selectWritten.val(skillsObj['language_written_skills_value']);
                   }

//                   l(selectWritten, 'selectWritten');

           //        var divCl = $('<div></div>');
           //        divCl.attr('class', 'cl');

                   var divSpokenLangSkills = $('<div></div>');
                   divSpokenLangSkills.attr('class', 'settings_div_select_lang_skills');
                   divSpokenLangSkills.html('Spoken');

                   var selectSpoken =  $('<select></select>');
                   selectSpoken.attr('class', 'mb_input');
                   selectSpoken.attr('id', 'choosen_language_spoken_' + selectedLanguageId);

                       var optionSpokenNone = $('<option></option>');
                       optionSpokenNone.addClass('color_black');
                       optionSpokenNone.attr('value', '0');
                       optionSpokenNone.html('None');

                       var optionSpokenBasic = $('<option></option>');
                       optionSpokenBasic.addClass('color_black');
                       optionSpokenBasic.attr('value', '1');
                       optionSpokenBasic.html('Basic');

                       var optionSpokenAdvanced = $('<option></option>');
                       optionSpokenAdvanced.addClass('color_black');
                       optionSpokenAdvanced.attr('value', '2');
                       optionSpokenAdvanced.html('Advanced');

                       var optionSpokenFluent = $('<option></option>');
                       optionSpokenFluent.addClass('color_black');
                       optionSpokenFluent.attr('value', '3');
                       optionSpokenFluent.html('Fluent');

                   selectSpoken.append(optionSpokenNone);
                   selectSpoken.append(optionSpokenBasic);
                   selectSpoken.append(optionSpokenAdvanced);
                   selectSpoken.append(optionSpokenFluent);

                   if(typeof skillsObj !== 'undefined') {
                       selectSpoken.val(skillsObj['language_spoken_skills_value']);
                   }



                   var divButtonSave = $('<div></div>');
                   divButtonSave.attr('class', 'div-button-save-language');
                   divButtonSave.attr('id', 'div-button-save-language-' + selectedLanguageId);
                       var imgButtonSave = $('<img></img>');
                       imgButtonSave.attr('src', '/static/images/save_small.png');
                   divButtonSave.append(imgButtonSave);


               divWrapper.append(li);// Wrap LI

               divWrapper.append(divWrittenLangSkills);
               divWrapper.append(selectWritten);

               divWrapper.append(divCl);

               divWrapper.append(divSpokenLangSkills);
               divWrapper.append(selectSpoken);

               divWrapper.append(divButtonSave);

               return divWrapper;
}

$( "#settings_input_languages" ).on( "mb:add", function( e, tagName ) {

    var ul = $('ul.mb-taglist');
    var li = $('ul.mb-taglist > li');
    li.remove();
//    var nameSelectedLanguage = li.attr('data-tag');
//    l(nameSelectedLanguage, 'nameSelectedLanguage');

    var selectedOption = $('select.mb-input option:selected');
    var selectedLanguageId = selectedOption.attr('id');
    selectedLanguageId = selectedLanguageId.substr('option_lang_id_'.length);
//    l(selectedLanguageId, 'selectedLanguageId');
    $.ajax({
        type: "POST",
        url: "/add_language_to_user",
        data: 
            {
                'languageId':selectedLanguageId,
            }
    }).done(function(response) { 
        if(typeof response['insertResult'] !== 'undefined'){
            if('53ff11fd92e60419383fd536'.length === response['insertResult'].toString().length){

                var selectedOption = $('select.mb-input option:selected');
                selectedOption.remove();
                
                var undefinedLi = undefined;
                var divWrapper = createDivWrapper(selectedLanguageId, response['language_name'], undefinedLi);

                ul.append(divWrapper);
            }
        }
    });
    console.info( "Added: ", tagName );
} );

$( "#settings_input_languages" ).on( "mb:remove", function( e, tagName ) {
    console.info( "Removed: ", tagName );
} );
