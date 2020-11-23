$(function(){
    $("textarea#id_comment").on("keydown", function(e){
        if(e.ctrlKey){
			if(e.keyCode === 13 && $(this).val()){
				$('button#comment-submit-btn').click();
      	    }
      	}
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