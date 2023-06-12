function search(e) {
  $.ajax({
    url: "ajax/ajax_search_project/",
    method: 'GET',
    data: {
      "proj_id": ""
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