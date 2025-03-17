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

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".submit").addEventListener("click", function (event) {
        event.preventDefault();
        showConfirmationPopup(); // Show confirmation popup first
    });
  });
  
  // Show Confirmation Popup
  function showConfirmationPopup() {
    document.getElementById("confirmation-popup").style.display = "flex";
  }
  
  // Close Confirmation Popup
  function closeConfirmationPopup() {
    console.log("show confirmation")
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

  // Show Rejected Popup
  function showRejectReqPopup(){
    console.log("show rejected popup") 
    document.getElementById("rejectReq-popup").style.display = "flex";
  }
  

  
// document.addEventListener("DOMContentLoaded", function () {
//   const updateButtons = document.querySelectorAll(".update-btn");
//   const popup = document.getElementById("confirmation-popup");

//   // Modal input fields
//   const modalName = document.getElementById("modal-name");
//   const modalCategory = document.getElementById("modal-category");
//   const modalAddress = document.getElementById("modal-address");

//   let selectedRequestID = null; // Store request ID



//   // Handle "Update" button click
//   updateButtons.forEach(button => {
//       button.addEventListener("click", function () {
//           selectedRequestID = this.dataset.requestId;  // Get request ID

//           // Set modal values dynamically
//           modalName.value = this.dataset.name;
//           modalCategory.value = this.dataset.category;
//           modalAddress.value = this.dataset.address;

//           // Show the popup
//           popup.style.display = "block";


//       });
//   });
// });
