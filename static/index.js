// Function to load HTML content into an element
function loadHTML(elementId, filePath) {
  fetch(filePath)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.text();
    })
    .then((data) => {
      document.getElementById(elementId).innerHTML = data;

      // Call an initialization function based on the element loaded
      if (elementId === "header") {
        initNavbar(); // Initialize navbar functionality
      } else if (elementId === "sidebar") {
        initSidebar(); // Initialize sidebar functionality
        setActiveLink(); // Set active link in the sidebar
      }
    })
    .catch((error) => {
      console.error("Error loading HTML:", error);
    });
}

// Determine the base path and file paths dynamically based on the location of the page
let basePath = "../../";
let navbarFile = "navbar.html";
let sidebarFile = "sidebar.html";

// Update paths based on the new folder structure in `Templates`
if (window.location.pathname.includes("/Templates/User/")) {
  basePath = "../../";
  navbarFile = "navbar.html";
  sidebarFile = "sidebar.html";
} else if (window.location.pathname.includes("/Templates/Admin/")) {
  basePath = "../../";
  navbarFile = "navbarAdmin.html";
  sidebarFile = "sidebarAdmin.html";
} else if (window.location.pathname.includes("/admin.html")) {
  basePath = "";
  navbarFile = "navbarAdmin.html";
  sidebarFile = "sidebarAdmin.html";
} else if (window.location.pathname.includes("/user.html")) {
  basePath = "";
  navbarFile = "navbar.html";
  sidebarFile = "sidebar.html";
}

// Load the appropriate header and sidebar based on the detected paths
loadHTML("header", `${basePath}${navbarFile}`);
loadHTML("sidebar", `${basePath}${sidebarFile}`);

// Function to initialize navbar functionality
function initNavbar() {
  // Toggle Customize Menu
  const customizeBtn = document.getElementById("customizeBtn");
  const customizeMenu = document.getElementById("customizeMenu");

  if (customizeBtn && customizeMenu) {
    customizeBtn.addEventListener("click", function (event) {
      event.stopPropagation(); // Prevent the event from bubbling to other elements
      const isVisible = customizeMenu.style.display === "block";
      customizeMenu.style.display = isVisible ? "none" : "block";
    });

    // Hide customize menu when clicking outside
    document.addEventListener("click", function (event) {
      if (
        !customizeBtn.contains(event.target) &&
        !customizeMenu.contains(event.target)
      ) {
        customizeMenu.style.display = "none";
      }
    });
  }

  // Toggle Notifications Menu
  const nBtn = document.getElementById("nBtn");
  const nMenu = document.getElementById("nMenu");

  if (nBtn && nMenu) {
    nBtn.addEventListener("click", function (event) {
      event.stopPropagation();
      const isVisible = nMenu.style.display === "block";
      nMenu.style.display = isVisible ? "none" : "block";
    });

    // Hide notifications menu when clicking outside
    document.addEventListener("click", function (event) {
      if (!nBtn.contains(event.target) && !nMenu.contains(event.target)) {
        nMenu.style.display = "none";
      }
    });
  }

  // Small device dropdown (Mobile view)
  const smallDeviceDropdownBtn = document.getElementById("smallDeviceDropdown");
  const smallDeviceDropdownMenu = smallDeviceDropdownBtn?.nextElementSibling;

  if (smallDeviceDropdownBtn && smallDeviceDropdownMenu) {
    smallDeviceDropdownBtn.addEventListener("click", function (event) {
      event.stopPropagation();
      const isVisible = smallDeviceDropdownMenu.classList.contains("show");
      if (isVisible) {
        smallDeviceDropdownMenu.classList.remove("show");
      } else {
        smallDeviceDropdownMenu.classList.add("show");
      }
    });

    // Hide small device dropdown when clicking outside
    document.addEventListener("click", function (event) {
      if (
        !smallDeviceDropdownBtn.contains(event.target) &&
        !smallDeviceDropdownMenu.contains(event.target)
      ) {
        smallDeviceDropdownMenu.classList.remove("show");
      }
    });
  }

  // Navbar toggler for mobile view
  const navbarToggler = document.querySelector(".navbar-toggler");
  const sidebar = document.getElementById("snavbarTogglerDemo03");

  if (navbarToggler && sidebar) {
    navbarToggler.addEventListener("click", function () {
      sidebar.classList.toggle("open");
    });
  }
}

// Function to initialize sidebar functionality
function initSidebar() {
  const sidebar = document.getElementById("snavbarTogglerDemo03");
  const sidebarToggleBtn = document.getElementById("sidebarToggleBtn");
  const closeNav = document.getElementById("closeNav");

  // Check if the sidebar and toggle button exist
  if (!sidebar || !sidebarToggleBtn) {
    console.error("Sidebar or toggle button not found.");
    return;
  }

  // Initially hide the sidebar
  sidebar.classList.remove("open");

  // Toggle sidebar visibility when the toggle button is clicked
  sidebarToggleBtn.addEventListener("click", function () {
    sidebar.classList.toggle("open"); // Toggle 'open' class
  });

  // Close sidebar when the close button is clicked
  closeNav.addEventListener("click", function () {
    sidebar.classList.remove("open");
  });
}

// Function to set the active link in the sidebar
function setActiveLink() {
  const links = document.querySelectorAll("a[href]"); // Select all anchor tags with href attribute
  const currentPath = window.location.pathname; // Get the current path

  links.forEach((link) => {
    const linkPath = link.getAttribute("href");

    // Debugging log
    console.log("Current Path:", currentPath);
    console.log("Checking link:", linkPath);

    // Check if the current path includes the link path and set the active class on the div inside
    if (currentPath.includes(linkPath)) {
      const udashDiv = link.querySelector(".Udash");
      if (udashDiv) {
        udashDiv.classList.add("active");
      }
    }
  });
}
