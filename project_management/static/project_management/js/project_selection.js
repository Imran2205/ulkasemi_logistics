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

  $.ajax({
    url: req_url.replace('0', proj_id),
    method: 'GET',
    headers: {'X-CSRFToken': token},
    success: function (response) {
      if (response["updates_this_week"].length > 0) {
        var currentDate = new Date();
        var year = new Date(currentDate.getFullYear(), 0, 1);
        var days = Math.floor((currentDate - year) / (24 * 60 * 60 * 1000));
        var week = Math.trunc((currentDate.getDay() + 1 + days) / 7);

        if (response["updates_this_week"][0]['week'] === week) {
          for (var i = 0; i < response["updates_this_week"].length; i++) {
            if (response["updates_this_week"][i]['type'] === 'this_week') {
              document.getElementById('editorContent').innerHTML = response["updates_this_week"][i]['description'];
            }
            else if (response["updates_this_week"][i]['type'] === 'next_week') {
              document.getElementById('editorContent2').innerHTML = response["updates_this_week"][i]['description'];
            }
            else if (response["updates_this_week"][i]['type'] === 'comment') {
              document.getElementById('editorContent3').innerHTML = response["updates_this_week"][i]['description'];
            }
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
      } else {
        $('.editor').show();
        $('#update_edit').hide();
        $('#update_form_hide').hide();
        document.getElementById('editorContent').innerHTML = "";
        document.getElementById('editorContent2').innerHTML = "";
        document.getElementById('editorContent3').innerHTML = "";
      }

      // for (var j=0; j<response["updates_this_week"].length; j++){
      //   var main_html = `
      //     <li class="timeline-item">
      //       <div class="timeline-info">
      //         <span style="padding-top: 20px;">
      //   ` + `</span>
      //     <i id="update_edit" class="fa fa-pencil-square-o fa-lg" aria-hidden="true" onclick="show_update_form()" style="display: none; cursor: pointer"></i>
      //       </div>
      //       <div class="timeline-marker">
      //       </div>
      //       <div class="timeline-content">
      //   `
      // }
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
}

function save_comment(e, req_url, token) {
  var proj_id = e.getAttribute('p_id');

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
        console.log(response);
        alert("Your response is stored successfully!!!")
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