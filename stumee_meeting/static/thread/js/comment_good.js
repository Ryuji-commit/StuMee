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