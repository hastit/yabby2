// JavaScript for dropdown menu behavior if needed
document.addEventListener('DOMContentLoaded', (event) => {
  // Example code for dropdown menu handling
  const dropdowns = document.querySelectorAll('.dropdown');
  dropdowns.forEach(dropdown => {
      dropdown.addEventListener('click', () => {
          const content = dropdown.querySelector('.dropdown-content');
          content.classList.toggle('show');
      });
  });
});
