$(function(){
    // Ajaxによるいいねボタンの処理
    $(document).ready(function () {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            crossDomain: false,
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    });

    $("#thread-good-mark").on("click", function() {
        event.preventDefault();
        var thread_good = $(this);
        $.ajax({
            url: thread_good.attr('data-href'),
            method: 'POST',
            timeout: 10000,
            dataType: "json",
        })
        .done(function (data) {
            $('.thread-good-count').text(data.count)
        })
        .fail(function (data) {
            alert("fail");
        })
    });

    $(".comment-good-mark").on("click", function() {
        event.preventDefault();
        var comment_good = $(this);
        $.ajax({
            url: comment_good.attr('data-href'),
            method: 'POST',
            timeout: 10000,
            dataType: "json",
        })
        .done(function (data) {
            var id = '#comment-good-count-' + data.id;
            $('.comment-good').addClass('on')
            $(id).text(data.count)
        })
        .fail(function (data) {
            alert('error')
        })
    });
});



// 一般に使用するjs
// form-control要素を追加
$(function(){
    $('div.form-group [id^=id_]').addClass('form-control');
});

// post_thread.htmlに使用するjs
// 日本語の入力を禁止
$(function(){
   $('div.form-group input[id=id_tag]').attr({
    'pattern': '^[0-9A-Za-z, ]+$',
    'aria-describedby' : 'tagHelpBlock'
    });
    $('div.form-group input[id=id_tag]').after(
        '<small id="tagHelpBlock" class="form-text text-muted">タグ名は半角英数字で、カンマ区切りで入力してください。</small>'
    );
});