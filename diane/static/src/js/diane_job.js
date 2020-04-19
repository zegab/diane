$(document).ready(function() {
  if($("#send_job").prop("checked")) {
    $('#send_job_section_div').show();
  } else {
    $('#send_job_section_div').hide();
  }
  $('#submit').hide();
});

$( document ).on("click", "#send_job", function () {
      if($("#send_job").prop("checked")) {
        $('#send_job_section_div').show();
      } else {
        $('#send_job_section_div').hide();
      }
      $('#submit').show();
});

$( document ).on("click", "#send_job_section_div", function () {
    $('#submit').show();
});

