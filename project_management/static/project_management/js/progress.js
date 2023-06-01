// $(function(){
//   var $ppc = $('.progress-pie-chart'),
//     percent = parseInt($ppc.data('percent')),
//     deg = 360*percent/100;
//   if (percent > 50) {
//     $ppc.addClass('gt-50');
//   }
//   $('.ppc-progress-fill').css('transform','rotate('+ deg +'deg)');
//   $('.ppc-percents span').html(percent+'%');
// });

function progress_set(proj_id, percent) {
  var ppc = $(`#progress_${proj_id}`),
    deg = 360*percent/100;
  percent = parseInt(percent);
  if (percent > 50) {
    ppc.addClass('gt-50');
  }
  else {
    ppc.removeClass('gt-50');
  }
  $(`#progres_fill_${proj_id}`).css('transform','rotate('+ deg +'deg)');
  $(`#progress_percent_${proj_id} span`).html(percent+'%');
}