document.addEventListener("DOMContentLoaded", function () {
    let cards = document.querySelectorAll('.card');
    let maxHeight = 0;

    cards.forEach(card => {
        maxHeight = Math.max(maxHeight, card.offsetHeight);
    });

    cards.forEach(card => {
        card.style.height = maxHeight + "px";
    });
});
