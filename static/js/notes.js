// Toggle content based on button click
function toggleContent(sectionId) {
  const sections = document.querySelectorAll('.content-section');
  sections.forEach(section => {
      section.style.display = 'none';
  });

  const selectedSection = document.getElementById(sectionId);
  if (selectedSection) {
      selectedSection.style.display = 'block';
  }
}

// Document ready event for filtering logic
document.addEventListener('DOMContentLoaded', function () {
  const subjectButtons = document.querySelectorAll('.subject-button');

  subjectButtons.forEach(button => {
    button.addEventListener('click', function (event) {
      event.preventDefault();
      const grade = button.getAttribute('data-grade');
      const subject = button.getAttribute('data-subject');

      // Encode the subject and grade to handle special characters
      const encodedSubject = encodeURIComponent(subject);
      const encodedGrade = encodeURIComponent(grade);

      const fetchUrl = `/notes/${encodedGrade}/${encodedSubject}/`;
      console.log('Fetching URL:', fetchUrl); // Debug log for URL

      fetch(fetchUrl)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          const notesContainer = document.querySelector(`#${grade}-notes .note-boxes`);
          notesContainer.innerHTML = ''; // Clear previous notes
          if (data.notes.length) {
            data.notes.forEach(note => {
              notesContainer.innerHTML += `
                <a href="/notes/${note.pk}" class="note-box">
                  <img src="${note.preview_image ? note.preview_image : '/static/images/default_preview.jpg'}" alt="${note.title}" class="note-image">
                  <div class="note-title">${note.title}</div>
                </a>
              `;
            });
          } else {
            notesContainer.innerHTML = '<p>No notes available for this subject.</p>';
          }
        })
        .catch(error => console.error('Error fetching notes:', error));
    });
  });
});
