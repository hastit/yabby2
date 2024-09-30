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

document.addEventListener('DOMContentLoaded', function () {
  const subjectButtons = document.querySelectorAll('.subject-button');

  subjectButtons.forEach(button => {
    button.addEventListener('click', function (event) {
      event.preventDefault();
      const grade = button.getAttribute('data-grade');
      const subject = button.getAttribute('data-subject');

      // Encode the subject and grade to handle special characters (e.g., spaces, accents)
      const encodedSubject = encodeURIComponent(subject);
      const encodedGrade = encodeURIComponent(grade);

      // Construct the fetch URL
      const fetchUrl = `/app/notes/${encodedGrade}/${encodedSubject}/`;
      console.log('Fetching URL:', fetchUrl); // Debug log for URL

      fetch(fetchUrl)
        .then(response => {
          if (!response.ok) {
            // Log the response status and body for better debugging
            return response.text().then(text => {
              console.error('Error response:', text);
              throw new Error(`Network response was not ok (status: ${response.status})`);
            });
          }
          return response.json();
        })
        .then(data => {
          // Ensure the notes container is selected correctly using `id`
          const notesContainer = document.querySelector(`#${grade}-notes .note-boxes`);
          notesContainer.innerHTML = ''; // Clear previous notes

          if (data.notes && data.notes.length) {
            data.notes.forEach(note => {
              notesContainer.innerHTML += `
                <a href="/notes/${note.pk}" class="note-box">
                  <img src="${note.preview_image ? note.preview_image : '/static/images/default_preview.jpg'}" alt="${note.title}" class="note-image">
                  <div class="note-title">${note.title}</div>
                </a>`;
            });
          } else {
            notesContainer.innerHTML = '<p>No notes available for this subject.</p>';
          }
        })
        .catch(error => {
          // Handle and log errors properly, showing a message in the UI
          console.error('Error fetching notes:', error);
          const notesContainer = document.querySelector(`#${grade}-notes .note-boxes`);
          notesContainer.innerHTML = '<p>There was an error loading the notes. Please try again later.</p>';
        });
    });
  });
});
