document.addEventListener("DOMContentLoaded", function () {
  const dropdownBalance = document.getElementById("dropdownBalance");
  const dropdownMenu = dropdownBalance.nextElementSibling; // The ul element

  dropdownBalance.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default link behavior
    dropdownMenu.classList.toggle("show"); // Toggle visibility of the dropdown menu
  });

  // Close dropdown when clicking outside
  document.addEventListener("click", function (event) {
    if (
      !dropdownBalance.contains(event.target) &&
      !dropdownMenu.contains(event.target)
    ) {
      dropdownMenu.classList.remove("show");
    }
  });

  // Dropdown functionality for notifications
  const nBtn = document.getElementById("nBtn");
  const nMenu = document.getElementById("nMenu");

  nBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default button behavior
    nMenu.classList.toggle("show"); // Toggle visibility
  });

  // Close notifications dropdown when clicking outside
  document.addEventListener("click", function (event) {
    if (!nBtn.contains(event.target) && !nMenu.contains(event.target)) {
      nMenu.classList.remove("show"); // Hide the menu
    }
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const dropdownTrigger = document.querySelector("#smallDeviceDropdown");
  dropdownTrigger.addEventListener("click", () => {
    const dropdownMenu = document.querySelector(".dropdown-menu");
    if (dropdownMenu.classList.contains("show")) {
      dropdownMenu.classList.remove("show");
    } else {
      dropdownMenu.classList.add("show");
    }
  });
});
