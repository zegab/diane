$( document ).on("click", "#sendmessage", function () {
    var p_id = $(this).attr('data-id');
    $("#p_id").val(p_id);
});
