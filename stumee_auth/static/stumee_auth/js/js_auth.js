$(function(){
    $('div.form-group input[name="username"]').addClass('form-control');
    $('div.form-group input[name="user_auth"]').addClass('custom-control-input');
    $('div.form-group input[id="password"]').addClass('form-control');
    $('div.form-group input[id="ta_password"]').addClass('form-control');
    $('div.form-group input[id="teacher_password"]').addClass('form-control');

    var icon_css = {
        visibility:'hidden',
        width:'0',
        height:'0',
    }
    $('div.form-group input[name="original_image"]').css(icon_css);
});

// 権限変更時のイベント
$(function(){
    $( 'input[name="user_auth"]:radio' ).change( function() {
        var radio_value = $(this).val();
        $('div.form-group input[id="ta_password"]').val("");
        $('div.form-group input[id="teacher_password"]').val("");
        if (radio_value == 1){
            $('#modal-TA-Certification-Key-Form').modal();
            $('#modal-Teacher-Certification-Key-Form').modal('hide');
        }else if (radio_value == 2){
            $('#modal-Teacher-Certification-Key-Form').modal();
            $('#modal-TA-Certification-Key-Form').modal('hide');
        }else{
            $('#modal-TA-Certification-Key-Form').modal('hide');
            $('#modal-Teacher-Certification-Key-Form').modal('hide');
        }
    });
});

// 認証キーを入力するモーダルが閉じられたら
$(function(){
    $(".certification-modal-close").on('click', function () {
        $('input[value="0"]:radio').prop('checked', true);
    });
});