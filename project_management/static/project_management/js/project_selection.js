function project_selection(target, proj_id, req_url, token) {
  let proj_s = document.getElementsByClassName('msg');
  for (let i = 0; i < proj_s.length; i++) {
    let item = proj_s[i];
    if (item === target) {
      item.classList.add("selected-bg")
    } else {
      item.classList.remove("selected-bg")
    }
  }
  $('.mail-detail').show();
  var b = $('.submit-button');
  b.attr('p_id', proj_id);
  b.attr('p_req_url', req_url);

  setup_timeline(proj_id, req_url, token);
}

function setup_timeline(proj_id, req_url, token) {
  $.ajax({
    url: req_url.replace('0', proj_id),
    method: 'GET',
    headers: {'X-CSRFToken': token},
    success: function (response) {
      let timeline_data = ``
      for (var j=0; j<response["updates_this_week"].length; j++){
        let this_week_html = `
          <li class="timeline-item">
            <div class="timeline-info">
              <span style="padding-top: 20px;">${response["updates_this_week"][j]['created_at'].split("T")[0]}</span>
              <i id="update_edit" class="fa fa-pencil-square-o fa-lg" aria-hidden="true" onclick="show_update_form()" style="display: none; cursor: pointer"></i>
            </div>
            <div class="timeline-marker">
              <span style="left: 6px; top: 7px; position: relative">${response["updates_this_week"][j]['week']}</span>
            </div>
            <div class="timeline-content">
              <!--                      <h3 class="timeline-title">Event Title</h3>-->
              <p class="justify-align-text" style="font-size: 17px;">
                ${response["updates_this_week"][j]['description_summary']}
              </p>

              <ul class="timeline-member">
                <li class="timeline-item-member">
                  <div class="timeline-info-member"></div>
                  <div class="timeline-marker-member">
                    <div class="circle-image pp_st" ofc_id="${response["updates_this_week"][j]['creator_ofc_id']}">
                      <img src="${response["updates_this_week"][j]['creator_pp_url']}"
                         alt="" class="members_team">
                    </div>
                  </div>
                  <div style="text-align: justify">
                    <p class="justify-align-text" style="font-size: 15px;">
                        <b>This Week:</b> ${response["updates_this_week"][j]['description_this_week']}
                    </p>
                    <p style="font-size: 15px;">
                        <b>Next Week:</b> ${response["updates_this_week"][j]['description_next_week']}
                    </p>
                    <p style="font-size: 15px; color: gray">
                      <i>
                        <b>Comment:</b> ${response["updates_this_week"][j]['description_comment']}
                      </i>
                    </p>

                  </div>
                </li>
              </ul>
            </div>
          </li>
        `
        timeline_data = timeline_data + '\n' + this_week_html;
      }
      for (var k=0; k<response["updates_others"].length; k++){
        let other_week_html = `
          <li class="timeline-item">
            <div class="timeline-info">
              <span style="padding-top: 20px;">${response["updates_others"][k]['created_at'].split("T")[0]}</span>
            </div>
            <div class="timeline-marker">
              <span style="left: 6px; top: 7px; position: relative">${response["updates_others"][k]['week']}</span>
            </div>
            <div class="timeline-content">
              <!--                      <h3 class="timeline-title">Event Title</h3>-->
              <p class="justify-align-text" style="font-size: 17px;">${response["updates_others"][k]['description_summary']}</p>

              <ul class="timeline-member">
                <li class="timeline-item-member">
                  <div class="timeline-info-member"></div>
                  <div class="timeline-marker-member">
                    <div class="circle-image pp_st" ofc_id="${response["updates_others"][k]['creator_ofc_id']}">
                      <img src="${response["updates_others"][k]['creator_pp_url']}"
                         alt="" class="members_team">
                    </div>
                  </div>
                  <div style="text-align: justify">
                    <p class="justify-align-text" style="font-size: 15px;">
                        <b>This Week:</b> ${response["updates_others"][k]['description_this_week']}
                    </p>
                    <p style="font-size: 15px;">
                        <b>Next Week:</b> ${response["updates_others"][k]['description_next_week']}
                    </p>
                    <p style="font-size: 15px; color: gray">
                      <i>
                        <b>Comment:</b> ${response["updates_others"][k]['description_comment']}
                      </i>
                    </p>

                  </div>
                </li>
              </ul>
            </div>
          </li>
        `
        timeline_data = timeline_data + '\n' + other_week_html;
      }
      $('#timeline_ul').html(timeline_data);
      if (response["updates_this_week"].length > 0) {
        var currentDate = new Date();
        var year = new Date(currentDate.getFullYear(), 0, 1);
        var days = Math.floor((currentDate - year) / (24 * 60 * 60 * 1000));
        var week = Math.trunc((currentDate.getDay() + 1 + days) / 7);

        if (response["updates_this_week"][0]['week'] === week) {
          for (var i = 0; i < response["updates_this_week"].length; i++) {
            document.getElementById('editorContent').innerHTML = response["updates_this_week"][i]['description_this_week'];
            document.getElementById('editorContent2').innerHTML = response["updates_this_week"][i]['description_next_week'];
            document.getElementById('editorContent3').innerHTML = response["updates_this_week"][i]['description_comment'];
          }
          $('.editor').hide();
          $('#update_edit').show();
          $('#update_form_hide').show();
        } else {
          $('.editor').show();
          $('#update_edit').hide();
          $('#update_form_hide').hide();
          document.getElementById('editorContent').innerHTML = "";
          document.getElementById('editorContent2').innerHTML = "";
          document.getElementById('editorContent3').innerHTML = "";
        }
      }
      else {
        $('.editor').show();
        $('#update_edit').hide();
        $('#update_form_hide').hide();
        document.getElementById('editorContent').innerHTML = "";
        document.getElementById('editorContent2').innerHTML = "";
        document.getElementById('editorContent3').innerHTML = "";
      }
      $(".btn_st").each(function( index ) {
        if ($(this).text() === response['proj_status']) {
          $(this).removeClass('defult-btn');
          $(this).addClass('defult-green');
        }
        else {
          $(this).removeClass('defult-green');
          $(this).addClass('defult-btn');
        }
      });
      $("#project_progress").val(response['proj_progress']);
      $("#project_progress_value").val(response['proj_progress']);
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
}

function save_comment(e, req_url, token) {
  var proj_id = e.getAttribute('p_id');
  var proj_req_url = e.getAttribute('p_req_url');

  var this_week = document.getElementById('editorContent').innerHTML;
  var next_week = document.getElementById('editorContent2').innerHTML;
  var comment = document.getElementById('editorContent3').innerHTML;

  if (this_week !== '' || next_week !== '' || comment !== '') {
    $.ajax({
      url: req_url.replace('0', proj_id),
      method: 'POST',
      data: {
        "this_week": this_week,
        "next_week": next_week,
        "comment": comment
      },
      headers: {'X-CSRFToken': token},
      success: function (response) {
        // console.log(response);
        alert("Your response is stored successfully!!!");
        setup_timeline(proj_id, proj_req_url, token);
      },
      error: function (error) {
        console.log(error);
        console.log("error");
      }
    });
  }
}

function show_update_form(){
  $('.editor').show()
}

function hide_update_form(){
  $('.editor').hide()
}

function set_project_progress(e, token) {
  let proj_id = document.getElementById('submit-button').getAttribute('p_id');
  var proj_req_url = document.getElementById('submit-button').getAttribute('p_req_url');

  $.ajax({
    url: "ajax/set_project_progress/",
    method: 'POST',
    data: {
      "proj_id": proj_id,
      "progress": e.value
    },
    headers: {'X-CSRFToken': token},
    success: function (response) {
      // console.log(response);
      // setup_timeline(proj_id, proj_req_url, token);
      // console.log(e.value);
      progress_set(proj_id, e.value);
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
}

function set_project_status(status, token){
  let proj_id = document.getElementById('submit-button').getAttribute('p_id');
  var proj_req_url = document.getElementById('submit-button').getAttribute('p_req_url');

  $.ajax({
    url: "ajax/set_project_status/",
    method: 'POST',
    data: {
      "proj_id": proj_id,
      "status": status
    },
    headers: {'X-CSRFToken': token},
    success: function (response) {
      console.log(response);
      setup_timeline(proj_id, proj_req_url, token);
      let status_show = $(`#status_${proj_id}`);
      status_show.html(status);
      let current_classes = status_show.attr('class').split(/\s+/);
      let keep_class = ['tag', 'chatStatus']
      $.each(current_classes, function(index, item) {
        if (! keep_class.includes(item)) {
          console.log("removing..", item);
          status_show.removeClass(item);
        }
      });
      let css_class = status.replaceAll(' ', '').toLowerCase();
      console.log("adding..", css_class);
      status_show.addClass(css_class);
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
}