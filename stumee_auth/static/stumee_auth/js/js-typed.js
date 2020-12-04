window.onload = function() {
    const username = JSON.parse(document.getElementById('username').textContent);
    const typeChar = `こんにちは${username}さん。まだユーザ名の変更をしていない場合は設定ページで変更してください。
    また、各ページのグローバルナビ右部にそれぞれのページの利用方法のツールチップを用意しています。`
    typing('typing-space', typeChar);
};

const typing = (elementId, sentence) => {
    [...sentence].forEach((character, index) => {
        setTimeout(() => {
            document.getElementById(elementId).textContent += character;
        }, 100 * ++index);
    });
}