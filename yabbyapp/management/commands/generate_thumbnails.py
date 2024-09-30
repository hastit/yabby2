import fitz  # PyMuPDF
from django.core.management.base import BaseCommand
from django.conf import settings
from yabbyapp.models import Note
from PIL import Image
import os

class Command(BaseCommand):
    help = 'Generate preview images for PDF files'

    def handle(self, *args, **kwargs):
        notes = Note.objects.all()
        for note in notes:
            if note.pdf and not note.image:
                self.generate_thumbnail(note)

    def generate_thumbnail(self, note):
        pdf_path = note.pdf.path
        image_path = os.path.join(settings.MEDIA_ROOT, 'images/notes', f'{note.id}_thumbnail.png')
        
        # Open PDF file
        pdf_document = fitz.open(pdf_path)
        
        # Get the first page
        page = pdf_document.load_page(0)
        
        # Render page to an image
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save the image
        img.save(image_path)
        
        # Update the note with the image path
        note.image = os.path.relpath(image_path, settings.MEDIA_ROOT)
        note.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created thumbnail for Note ID {note.id}'))
