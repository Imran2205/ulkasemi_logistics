function get_online_stat(){
  let pp_objs = $('.pp_st');
  pp_objs.each(function(idx, li) {
    let ofc_id = $(li).attr('ofc_id');
    if (ofc_id.length >= 6) {
      $.ajax({
        url: "ajax/ajax_get_active_time/",
        method: 'GET',
        data: {
          "id": ofc_id,
        },
        headers: {'X-CSRFToken': csrf_token},
        success: function (response) {
          let l_time = new Date(response['time']);
          let c_time = new Date();
          l_time = l_time.getTime();
          c_time = c_time.getTime();
          let time_dif = (c_time - l_time)/1000;
          if (time_dif > 60){
            $(li).addClass('inactive');
          }
          else {
            $(li).removeClass('inactive');
          }
        },
        error: function (error) {
          console.log(error);
          console.log("error");
        }
      });
    }
  });
}