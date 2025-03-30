document.addEventListener("DOMContentLoaded", function () {
    // Attach event listeners to all "Completed" buttons
    document.querySelectorAll(".completed-button").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default form submission (if any)
            showConfirmationPopup(); // Show confirmation popup instead
        });
    });
});

// Show Confirmation Popup
function showConfirmationPopup() {
    document.getElementById("proceed-popup").style.display = "flex";
}

// Close Confirmation Popup
function closeConfirmationPopup() {
    document.getElementById("proceed-popup").style.display = "none";
}

// Show Tracking Number Popup After Confirmation
function showTrackingPopup() {
    closeConfirmationPopup();
    document.getElementById("greatjob-popup").style.display = "flex";
}

// Close Tracking Popup
function closeTrackingPopup() {
    document.getElementById("greatjob-popup").style.display = "none";
}
