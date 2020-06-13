$(function(){
    $('div.form-group input[name="username"]').addClass('form-control');
    $('div.form-group input[name="user_auth"]').addClass('custom-control-input');
    $('div.form-group [id="password"]').addClass('form-control');

    var icon_css = {
        visibility:'hidden',
        width:'0',
        height:'0',
    }
    $('div.form-group input[name="original_image"]').css(icon_css);
});