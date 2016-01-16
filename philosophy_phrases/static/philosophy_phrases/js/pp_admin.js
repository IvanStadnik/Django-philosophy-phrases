django.jQuery(document).ready(function($){
    $('#import_default_phrases').on('click', function(){
        $('#pp_import_action').after('<span id="pp_loading"></span>');
        $.post($('#pp_import_action').val(), { csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()}, function(data){
            console.log(data);
            $('.pp_custom_submite_row #pp_loading').remove();
            $('#pp_import_action').after('<span id="pp_loading_result" class="'+data.class+'">'+data.message+'<span class="pp_mes_close"></span></span>');
        })
    })

    $('.pp_custom_submite_row').on('click', '.pp_mes_close', function(){
        $(this).parent('span').fadeOut('fast', function(){
            $(this).remove();
        })
    })
    $('.pp_custom_submite_row').on('click', '#pp_loading_result', function(){
        $(this).fadeOut('fast', function(){
            $(this).remove();
        })
    })
})