// document.addEventListener("DOMContentLoaded", function () {
//   document.querySelector(".submit").addEventListener("click", function (event) {
//     event.preventDefault();
//     customer_editProfile_ConfirmationPopup(); // Show confirmation popup first
//   });
// });

// Show Confirmation Popup
function customer_editProfile_ConfirmationPopup() {
  document.getElementById("customer-editProfile-confirmation-popup").style.display = "flex";
}

// Close Confirmation Popup
function customer_editProfile_close_ConfirmationPopup() {
  document.getElementById("customer-editProfile-confirmation-popup").style.display = "none";
}

// Show Sucessful Popup
function customer_editProfile_show_SucessfulPopup() {
  customer_editProfile_close_ConfirmationPopup();
  document.getElementById("customer-editProfile-sucessful-popup").style.display = "flex";
}

// Submit Form
function customer_editProfile_submitForm() {
  document.getElementById("editProfileForm").submit(); //submit form and validate first before show successful popup
}

// Show Confirmation Popup
function verifyForm() {
  const form = document.getElementById("editProfileForm");
  // console.log("Verifying form...");

  if (form.checkValidity()) {
    customer_editProfile_ConfirmationPopup();
    // console.log("Form is valid, showing confirmation popup.");
  } else {
    form.reportValidity();
    // console.log("Form is invalid, showing validation messages.");
  }
}