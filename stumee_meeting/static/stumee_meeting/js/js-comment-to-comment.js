window.onload = function () {
    const addCommentButtons = document.querySelectorAll('.add-comment-to-comment');
    const cancelCommentButton = document.getElementById('comment-cancel-btn');

    addCommentButtons.forEach(addCommentBtn => {
        addCommentBtn.addEventListener('click', SetUpCommentForm, false);
    })

    cancelCommentButton.addEventListener('click', HideCommentForm, false);

    document.getElementById('id_comment_to_comment').addEventListener('keydown', function(e){
        if(e.ctrlKey){
			if(e.keyCode == 13 && this.value){
				document.getElementById('comment-submit-btn').click();
      	    }
      	}
    },false);
};

function SetUpCommentForm(e){
    const clickedButton = e.target;
    const commentFormsTitle = document.getElementById('comment-forms-title');
    const commentSelectForm = document.getElementById('id_parent_comment_select');
    OperateDisplayAnswerForm(false);
    OperateDisplayCommentForm(true);

    commentFormsTitle.innerText = `@${clickedButton.dataset.commentUsername} にコメント`;
    console.log(commentSelectForm);
    commentSelectForm.value = clickedButton.dataset.commentPk;

    document.getElementById('id_comment_to_comment').focus();
}

function OperateDisplayAnswerForm(isShow) {
    const commentFormsTitle = document.getElementById('comment-forms-title');
    const answerForm = document.getElementById('answer-comment-form');
    if (isShow){
        commentFormsTitle.innerText = "この質問に回答する";
        answerForm.style.display = "block";
    }else{
        answerForm.style.display = "none";
    }
}

function OperateDisplayCommentForm(isShow) {
    const commentForm = document.getElementById('comment-to-comment-form');
    if (isShow){
        commentForm.style.display = "block";
    }else{
        commentForm.style.display = "none";
    }
}

function HideCommentForm(){
    OperateDisplayCommentForm(false);
    OperateDisplayAnswerForm(true);
}