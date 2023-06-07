$(".hover-profile").hover(function(){
  let position = $(this).position();
  let obj = $("#tooltip");
  let obj_cont = $(".con-tooltip");
  obj_cont.show();
  console.log(($(window).height() - position.top - 35), position.top-5);
  if (($(window).height() - position.top - 35) < 350) {
    obj_cont.css("top", position.top+15-385);
    obj_cont.css("left", position.left);
  }
  else {
    obj_cont.css("top", position.top+15);
    obj_cont.css("left", position.left);
  }
  obj.removeClass("tooltip");
  obj.addClass("tooltip-hover");
  $(".profile_hover_body").scrollTop(0);
}, function(){
  if ($(".con-tooltip:hover").length !== 0) {

  }
  else {
    let obj = $("#tooltip");
    let obj_cont = $(".con-tooltip");
    obj_cont.hide();
    obj.removeClass("tooltip-hover");
    obj.addClass("tooltip");
  }
});

$(".con-tooltip").hover(function(){

}, function () {
  let obj = $("#tooltip");
  let obj_cont = $(".con-tooltip");
  obj_cont.hide();
  obj.removeClass("tooltip-hover");
  obj.addClass("tooltip");
});

