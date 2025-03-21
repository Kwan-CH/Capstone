document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".update-btn");

  buttons.forEach(button => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");
      const status = row.querySelector(".status").innerText.trim();

      if (status === "Pending") {
        showConfirmationPopup();
      } else if (status === "Approved") {
        window.location.href = "assign-driver.html";
      }
    });
  });
});

//document.addEventListener("DOMContentLoaded", function () {
//    document.querySelector(".submit").addEventListener("click", function (event) {
//        event.preventDefault();
//        showConfirmationPopup(); // Show confirmation popup first
//    });
//  });

// Show Confirmation Popup
function showConfirmationPopup() {
  document.getElementById("confirmation-popup").style.display = "flex";
}

// Close Confirmation Popup
function closeConfirmationPopup() {
  document.getElementById("confirmation-popup").style.display = "none";
}

// Show Sucessful Popup
function showSuccessfulPopup() {
  closeConfirmationPopup();
  document.getElementById("sucessful-popup").style.display = "flex";
}

// Close Sucessful Popup
function closeTrackingPopup() {
  document.getElementById("sucessful-popup").style.display = "none";
}

//Show Reject Request Popup
function showRejectReqPopup() {
  closeConfirmationPopup();
  document.getElementById("rejectReq-popup").style.display = "flex";
}

//Close Reject Request Popup
function closeRejectReqPopup() {
  document.getElementById("rejectReq-popup").style.display = "none";
}

//Show Confirmation Popup2
function showConfirmationPopup2() {
  closeRejectReqPopup();
  document.getElementById("confirmation-popup").style.display = "flex";
}

function closeConfirmationPopup2() {
  closeRejectReqPopup();
  document.getElementById("confirmation-popup").style.display = "none";
}

//Rejected Popup
function rejectedPopup() {
  closeRejectReqPopup();
  document.getElementById("rejected-popup").style.display = "flex";
}

//Close Rejected Popup
function closeRejectedPopup() {
  document.getElementById("rejected-popup").style.display = "none";
}