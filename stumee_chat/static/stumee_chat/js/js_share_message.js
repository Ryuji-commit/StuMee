window.addEventListener('load', function() {
    handleDisplayShareButton();
})

function handleDisplayShareButton() {
    const chatContents = document.querySelectorAll(".talk-content");
    chatContents.forEach(function (element) {
        element.addEventListener("mouseenter", addMessageShareButton, false);
        element.addEventListener("mouseleave", removeMessageShareButton, false);
    });
}

function addMessageShareButton(e) {
    const element = e.currentTarget;
    let shareButton = document.createElement("span");
    shareButton.innerHTML = '<i class="fas fa-share-square fa-xs"></i>';
    shareButton.classList.add("share-message-btn");
    element.appendChild(shareButton);
}

function removeMessageShareButton(e) {
    const element = e.currentTarget;
    const shareButton = element.lastElementChild;
    if (e.relatedTarget != shareButton) {
        element.removeChild(shareButton);
    }
}
