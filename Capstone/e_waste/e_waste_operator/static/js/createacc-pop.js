document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".btn submit").addEventListener("click", function (event) {
      event.preventDefault();
      verifyForm(); // Show confirmation popup first
  });
});

// Show Confirmation Popup
function verifyForm() {
    const form = document.getElementById("driverForm");

    if (form.checkValidity()){
        showConfirmationPopUp();
    }else{
        form.reportValidity();
    }
  }

function showConfirmationPopUp(){
    document.getElementById("confirmation-popup").style.display = "flex";
}

// Proceed button in the confirmation pop up
function proceedAction(){
    console.log("Entering driver saving action");
    document.getElementById("hidden-submit").click();
}

// Close Confirmation Popup
function closeConfirmationPopup() {
    document.getElementById("confirmation-popup").style.display = "none";
}

// Show Successful Popup
function showSuccessfulPopup() {
    closeConfirmationPopup();
    document.getElementById("successful-popup").style.display = "flex";
}

// Close Successful Popup
function closeSuccessfulPopup() {
    document.getElementById("successful-popup").style.display = "none";
}

