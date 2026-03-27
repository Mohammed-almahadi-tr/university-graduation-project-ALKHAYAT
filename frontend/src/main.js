// Interaction Logic
document.addEventListener("DOMContentLoaded", () => {
  console.log("SUTRA Multi-Page Application Initialized");

  // Sidebar management or dark mode toggles could go here
  // For now, let's add a simple smooth scroll and basic interactions
  const dropdownButtons = document.querySelectorAll("[data-dropdown-toggle]");
  dropdownButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-dropdown-toggle");
      const target = document.getElementById(targetId);
      if (target) {
        target.classList.toggle("hidden");
      }
    });
  });

  // Dark mode toggle (if applicable)
  const toggleDarkMode = () => {
    document.documentElement.classList.toggle("dark");
  };

  // Attach to window for easy access from HTML if needed
  window.toggleDarkMode = toggleDarkMode;
});
