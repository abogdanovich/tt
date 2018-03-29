/*
#########################################################################
# TimeCard ajax requests
# author Alex Bogdanovich
# 2012 
#########################################################################
*/

//any useful functions are here...

var previous_logo = "";

//-----------------------------------------------------------------------------
function LoadLogotype() {
  var card_logo = $("#card_logo").val();

  if ((card_logo != "") && (previous_logo != card_logo)) {
    previous_logo = card_logo;
    $("#uploadphoto").submit();
  }
}

$(document).ready(function() {

var static_url_param = $("#static_url_param").attr('title');

//-----------------------------------------------------------------------------
setInterval("LoadLogotype()", 1000);

$("#datepicker").datepicker({
	showOn: "button",
	buttonImage: static_url_param+"css/images/calendar.png",
	dateFormat: "mm/dd",
	showAnim: "drop",
	autoSize: true,
	firstDay: 1,
	buttonImageOnly: true
});
$("#datepicker_report").datepicker({
	showOn: "button",
	buttonImage: static_url_param+"css/images/calendar.png",
	dateFormat: "yy-mm",
	showAnim: "drop",
	width: "30px",
	autoSize: true,
	changeYear: true,
	firstDay: 1,
	buttonImageOnly: true
});

$("#datepicker_dayoff").datepicker({
    dateFormat: "yy-mm-dd",
    autoSize: true,
    changeYear: true,
    firstDay: 1
});

$("#project_start_date").datepicker({
    dateFormat: "yy-mm-dd"
});


$("#save_u_set_button").button({
	icons: {
	    primary: "ui-icon-clipboard"
	}
});

$("#tabs").tabs({
    event: "mouseover"
});

$("#group_list_users").click(function(){
    if ($('#gomel_users').css('display') == "none") {
	$("#minsk_users").hide();
	$("#group_list_users").text("Гомель online");
	$("#gomel_users").show();
	
    }
    else {
	$("#gomel_users").hide();
	$("#group_list_users").text("Минск online");
	$("#minsk_users").show();
    }
    
    
});


$("div[id*=user_dep_selector_]").click(function(){
    var id = $(this).attr("id2");
    $("#user_dep_"+[id]).show();
    $(this).hide();
});

$("div[id*=user_group_selector_]").click(function(){
    var id = $(this).attr("id2");
    $("#user_group_"+[id]).show();
    $(this).hide();
});    


$("input[id*=xim_projects_]").click(function(){
    var project = $(this).attr("title");
    //$("#user_dep_"+[id]).show();
    $("#selected_project").text(project);
    
});    


$("img[id*=expand_]").click(function(){
      var id = $(this).attr("id2");
      var sr = $(this).attr("src");
      
      if (sr != static_url_param+"css/images/exp0.png") {
            $(this).attr("src",static_url_param+"css/images/exp0.png");
	    $(this).attr("width","60px");
            $("#expanddiv_"+[id]).slideDown();
      }
      else {
            $(this).attr("src",static_url_param+"css/images/exp1.png");
	    $(this).attr("width","60px");
            $("#expanddiv_"+[id]).hide();
      }
      
});


$("img[id^='user_hour_image_']").hover(function(){
        $(this).attr("src", static_url_param+"css/images/del15_hover.png");
        }, function(){
        $(this).attr("src", static_url_param+"css/images/del15.png");
});

     
});

