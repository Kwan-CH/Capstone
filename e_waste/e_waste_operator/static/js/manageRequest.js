document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".update-btn");

  buttons.forEach(button => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");
      const status = row.querySelector(".status").innerText.trim();

      if (status === "Pending") {
        showConfirmationPopup();
      }
    });
  });
});

let requestID = null;
<<<<<<< Updated upstream
function storeRequestID(button){
=======
function storeRequestID(button) {
>>>>>>> Stashed changes
  requestID = button.dataset.id;
}

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
function rejectRequest() {
  const resonDropdown = document.getElementById('reason');
  const selectedReason = resonDropdown.value;
  console.log(selectedReason)

  fetch("reject_request/", {
    method: "POST",
    headers: {
<<<<<<< Updated upstream
    "Content-Type": "application/json",
  "X-CSRFToken": getCookie("csrftoken"),  // CSRF token for security
  },
  body: JSON.stringify({ selectedRequest: requestID, selectedReason:selectedReason}),
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
            document.getElementById("successful-popup").style.display = "flex"; // Show success popup
          } else {
            alert("⚠️ " + data.message);
          }
    })
  .catch(error => console.error("Error:", error));
=======
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),  // CSRF token for security
    },
    body: JSON.stringify({ selectedRequest: requestID, selectedReason: selectedReason }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        document.getElementById("successful-popup").style.display = "flex"; // Show success popup
      } else {
        alert("⚠️ " + data.message);
      }
    })
    .catch(error => console.error("Error:", error));
>>>>>>> Stashed changes

  closeRejectReqPopup();
  document.getElementById("rejected-popup").style.display = "flex";
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
<<<<<<< Updated upstream
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.startsWith(name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
                }
            }
        }
=======
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
>>>>>>> Stashed changes
  return cookieValue;
}

//Close Rejected Popup
function closeRejectedPopup() {
  document.getElementById("rejected-popup").style.display = "none";
  window.location.reload();
}


<<<<<<< Updated upstream

function assignDriverPage(){
  if (!requestID){
    alert("Something went wrong")
  }else{
=======
function assignDriverPage() {
  if (!requestID) {
    alert("Something went wrong")
  } else {
>>>>>>> Stashed changes
    const url = `assign_driver_page?requestID=${requestID}`;
    console.log(url)
    window.location.href = url;
  }
}