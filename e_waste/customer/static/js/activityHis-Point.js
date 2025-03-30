function switchPage(page) {
    window.location.href = page;
}

<<<<<<< Updated upstream
document.getElementById('show-qr').addEventListener('click', function (event) {
    event.preventDefault();
    showQrPopup();
=======
// document.getElementById('show-qr').addEventListener('click', function (event) {
//     event.preventDefault();
//     showQrPopup();
// });

document.querySelectorAll('.show-qr').forEach(function (button) {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        showQrPopup();
    });
>>>>>>> Stashed changes
});

function showQrPopup() {
    document.getElementById('qr-popup').style.display = 'flex';
}

function closeSuccessfulPopup() {
    document.getElementById('qr-popup').style.display = 'none';
}