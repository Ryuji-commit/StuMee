const threadGoodMark = document.querySelector('#thread-good-mark');
const commentGoodMarks = document.querySelectorAll('.comment-good-mark');

threadGoodMark.addEventListener('click', function(e){
    const threadGoodCount = document.querySelector('.thread-good-count');
    const threadURL = threadGoodMark.getAttribute('data-href');
    fetch(threadURL)
        .then((response) => {
            if (response.status == 502) {
                console.log("status 502");
            }
            if (response.status != 200) {
                console.log("status" + response.status);
            }
            return response.json();
        })
        .then((data) => {
            threadGoodCount.innerText = data.count;
        })
        .catch((error) => {
            console.log(error);
        })
},false);

commentGoodMarks.forEach(element => {
    element.addEventListener('click', function(e){
        clickedMark = e.target;
        const commentURL = clickedMark.getAttribute('data-href');
        fetch(commentURL)
            .then((response) => response.json())
            .then((data) => {
                const CommentGoodCountDomID = 'comment-good-count-' + data.id;
                const CommentGoodCount = document.getElementById(CommentGoodCountDomID);
                CommentGoodCount.innerText = data.count;
            })
    })
},false);