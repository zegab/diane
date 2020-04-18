$(document).ready(function() {
  if($("#send_job").prop("checked")) {
    $('#send_job_section_div').show();
    $('#submit').show();
  } else {
    $('#send_job_section_div').hide();
    $('#submit').hide();
  }
});

