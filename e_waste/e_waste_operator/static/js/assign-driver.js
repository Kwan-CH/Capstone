document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".assign-btn");

  buttons.forEach(button => {
      button.addEventListener("click", function () {
        showConfirmationPopup();
      });
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

// Show Sucessful Popup 
function showSucessfulPopup() {
  closeConfirmationPopup(); 
  document.getElementById("sucessful-popup").style.display = "flex";
}

// Close Sucessful Popup
function closeTrackingPopup() {
  document.getElementById("sucessful-popup").style.display = "none";
}

