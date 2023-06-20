const days = (date_1, date_2) =>{
    let difference = date_1.getTime() - date_2.getTime();
    let TotalDays = Math.ceil(difference / (1000 * 3600 * 24));
    return TotalDays;
}

function  getFormalDate(convertDate) {
  let date = new Date(convertDate);
  if (date.toString() === "Invalid Date")
    return "N/A";

  let dateString = date.toLocaleDateString("en-US", {month: 'long', day: 'numeric', year: 'numeric'});
  return dateString
}

function search(e) {
  $('.mail-detail').hide();
  $.ajax({
    url: "ajax/ajax_search_project/",
    method: 'GET',
    data: {
      "search_parameter": e.value
    },
    headers: {'X-CSRFToken': csrf_token},
    success: function (response) {
      // console.log(response);
      // setup_timeline(proj_id, proj_req_url, token);
      // console.log(e.value);
      // console.log(response);
      let projects_html = ``;
      let projects = response['projects'];
      for (let i = 0; i < projects.length; i++) {
        let proj = projects[i];
        let deadline = new Date(proj['ends']);
        let today = new Date();
        let day_rem = days(deadline, today);
        if (day_rem < 0) {
          day_rem = 0;
        }
        let last_mod = new Date(proj['last_modified']);
        let status_l = proj['status'].replaceAll(' ', '').toLowerCase();
        let html_proj = `
          <div class="msg anim-y" onclick="project_selection(this, ${proj['id']}, 'ajax/get_project/${proj['id']}', '${csrf_token}')">
            <!-- <input type="checkbox" name="msg" id="mail1" class="mail-choice" checked> -->
            <!--                        <label for="mail1"></label>-->
            <div class="msg-content">
              <div class="msg-title">${proj['name']}</div>
              <div>
                place_tags_here
              </div>
  
              <div class="msg-date">
                <span style="color: rgb(93, 93, 93);">Started: </span>
                <span style="margin-right:5px">${getFormalDate(proj['started'])}</span>
  
                <span style="color: rgb(93, 93, 93);">Last modified: </span>
                <span>${getFormalDate(proj['last_modified'])}</span>
  
                <span style="color: rgb(93, 93, 93);">Ends: </span>
                <span>${getFormalDate(proj['ends'])}</span>
  
                <span style="color: rgb(93, 93, 93); margin-left: 16px;">Remaining: </span>
                <span>${day_rem} days</span>
              </div>
  
  
              <!--            <div class="">-->
              <!--              <div class="progress">-->
              <!--                <div class="progress-bar"></div>-->
              <!--              </div>-->
  
              <!--              <div class="progress-status">100/100</div>-->
              <!--            </div>-->
              <!--            -->
  
              <!-- <div class="side-wrapper"> -->
              <!-- <div class="project-title">Team</div> -->
              <div class="team-member">
                place_members_here
              </div>
              <!-- </div> -->
            </div>
            <!---Project Status-->
            <div class="mail-members">
              <div class="tag ${status_l} chatStatus" id="status_${proj['id']}">${proj['status']}</div>
  
              <div class="progress-pie-chart" data-percent="${proj['progress']}" id="progress_${proj['id']}">
                <div class="ppc-progress">
                  <div class="ppc-progress-fill" id="progres_fill_${proj['id']}"></div>
                </div>
                <div class="ppc-percents" id="progress_percent_${proj['id']}">
                  <div class="pcc-percents-wrapper">
                    <span></span>
                  </div>
                </div>
                <script type="text/javascript">
                    progress_set('${proj['id']}', '${proj['progress']}');
                </script>
              </div>
            </div>
          </div>
        `
        let html_tags = ``;
        for (let j = 0; j < proj['tags'].length; j++){
          let tag_html = `
           <span class="price-tag">
             <span>${proj['tags'][j]}</span>
           </span>
          `
          html_tags = html_tags + tag_html + '\n';
        }
        let html_members = ``;
        for (let k = 0; k < proj['members'].length; k++){
          let member_html = `
           <div class="circle-image pp_st" ofc_id="${proj['members'][k]['id']}">
              <img
                src="${proj['members'][k]["pp"]}"
                alt="PP" class="members_team">
            </div>
          `
          html_members = html_members + member_html + '\n'
        }
        html_proj = html_proj.replace(`place_tags_here`, html_tags);
        html_proj = html_proj.replace(`place_members_here`, html_members);
        projects_html = projects_html + html_proj + '\n';
      }
      $('.inbox').html(projects_html);
    },
    error: function (error) {
      console.log(error);
      console.log("error");
    }
  });
}