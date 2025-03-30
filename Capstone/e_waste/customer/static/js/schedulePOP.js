document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".submit").addEventListener("click", function (event) {
        event.preventDefault();
        if (validateForm()) {
            showConfirmationPopup(); // Show confirmation popup only if validation passes
        }
    });

    document.querySelector(".proceed").addEventListener("click", function () {
        document.getElementById("schedule-pickup-form").submit(); // Submit form after confirmation
    });
});

// Show Confirmation Popup
function showConfirmationPopup() {
    document.getElementById("confirmation-popup").style.display = "flex";
}

// Close Confirmation Popup
function closeConfirmationPopup() {
    document.getElementById("confirmation-popup").style.display = "none";
}

// Show Tracking Number Popup After Confirmation
function showTrackingPopup() {
    closeConfirmationPopup();
    document.getElementById("tracking-popup").style.display = "flex";
}

// Close Tracking Popup
function closeTrackingPopup() {
    document.getElementById("tracking-popup").style.display = "none";
}
