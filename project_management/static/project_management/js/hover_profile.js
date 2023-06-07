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
  $.ajax({
    url: "ajax/get_user_pop_up_info/",
    method: 'GET',
    data: {
      "id": $(this).attr('uid'),
    },
    headers: {'X-CSRFToken': $(this).attr('token')},
    success: function (response) {
      $('#popup_name').html(response['name']);
      if (response['profile_picture'] === 'na' || response['profile_picture'] === ''){
        $('#popup_pp').html(`
          <img src="/static/project_management/images/avatar.png" width="100px" height="100px" class="icon">
        `);
      }
      else{
        $('#popup_pp').html(`
          <img src="${response['profile_picture']}" width="100px" height="100px" class="icon">
        `);
      }

      $('#popup_designation').html(response['designation']);
      $('#popup_department').html(response['department']);
      $('#popip_ulka_email').html(response['ulka_email']);
      $('#popup_phone').html(response['ulka_email']);
      $('#popup_gf_email').html(response['ulka_email']);
      let team_html = ``;
      for (let i=0; i<response['teams'].length; i++) {
        team_html += `
          <div class="team" style="background-color: ${response['teams'][i]['color']}">${response['teams'][i]['name']}</div>
        `;
      }
      $('#popup_teams').html(team_html);
      let proj_c1_html = ``;
      let proj_c2_html = ``;
      for (const [key, value] of Object.entries(response['project_counts_c1'])) {
        proj_c1_html += `
          <div class="task-stat">
            <div class="task-number color_${key.replaceAll(' ', '').toLowerCase()}" style="opacity: 0.7;">${value}</div>
            <div class="task-condition color_${key.replaceAll(' ', '').toLowerCase()}">${key}</div>
            <div class="task-tasks color_${key.replaceAll(' ', '').toLowerCase()}" style="opacity: 0.5;">Projects</div>
          </div>
        `
      }
      for (const [key, value] of Object.entries(response['project_counts_c2'])) {
        proj_c2_html += `
          <div class="task-stat">
            <div class="task-number color_${key.replaceAll(' ', '').toLowerCase()}" style="opacity: 0.7;">${value}</div>
            <div class="task-condition color_${key.replaceAll(' ', '').toLowerCase()}">${key}</div>
            <div class="task-tasks color_${key.replaceAll(' ', '').toLowerCase()}" style="opacity: 0.5;">Projects</div>
          </div>
        `
      }
      $('#popup_proj_c1').html(proj_c1_html);
      $('#popup_proj_c2').html(proj_c2_html);
      console.log(response);
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
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

