// Toggle content based on button click
function toggleContent(sectionId) {
  // Get all content sections
  const sections = document.querySelectorAll('.content-section');
  
  // Hide all sections
  sections.forEach(section => {
      section.style.display = 'none';
  });

  // Show the selected section
  const selectedSection = document.getElementById(sectionId);
  if (selectedSection) {
      selectedSection.style.display = 'block';
  }
}

// Document ready event for filtering logic
document.addEventListener('DOMContentLoaded', function() {
  const filterButtons = document.querySelectorAll('.filter-button');
  const subjectButtons = document.querySelectorAll('.subject-button');
  const contentSections = document.querySelectorAll('.content-section');

  filterButtons.forEach(button => {
      button.addEventListener('click', function() {
          const target = this.getAttribute('data-target');
          contentSections.forEach(section => {
              if (section.id === target) {
                  section.style.display = 'block';
              } else {
                  section.style.display = 'none';
              }
          });
      });
  });

  subjectButtons.forEach(button => {
      button.addEventListener('click', function() {
          const filter = this.getAttribute('data-filter');
          // Add your filtering logic here to update the content inside filtered-content
          // For example, you can dynamically load content via Ajax or manipulate DOM based on the filter.
      });
  });
});
