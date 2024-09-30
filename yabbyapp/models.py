from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image
import fitz  # PyMuPDF
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    # Grade level choices
    GRADE_CHOICES = [
        ('seconde', 'Seconde'),
        ('bac_general', 'Bac Général'),
        ('bac_tech', 'Bac Technologique'),
    ]
    SUBJECT_CHOICES = [
        ('Mathématiques', 'Mathématiques'),
        ('Physique-chimie', 'Physique-chimie'),
        ('Histoire', 'Histoire'),
        ('Géographie', 'Géographie'),
        ('SES', 'SES'),
        ('Sciences numériques et technologie', 'Sciences numériques et technologie'),
        ('Français', 'Français'),
        ('SVT', 'SVT'),
        ('Anglais', 'Anglais'),
    ]

    
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    description = models.TextField()
    pdf = models.FileField(upload_to='notes_pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='images/notes/', blank=True, null=True)
    preview_image = models.ImageField(upload_to='images/previews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade_level = models.CharField(max_length=20, choices=GRADE_CHOICES, default='seconde')  # New field

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if the object is being created for the first time or updated
        is_new_instance = self._state.adding

        # Call the parent class's save method to save the object first
        super().save(*args, **kwargs)

        # If it's a new instance and there is a PDF, generate the preview image
        if is_new_instance and self.pdf and not self.preview_image:
            self.generate_preview_image()
            # Save again to store the preview image
            super().save(*args, **kwargs)

    def generate_preview_image(self):
        if self.pdf:
            pdf_path = self.pdf.path
            # Create a new image file path
            preview_image_name = f'{self.title}_preview.jpg'
            preview_image_path = default_storage.path(f'images/previews/{preview_image_name}')
            
            # Open PDF file and get the first page
            pdf_document = fitz.open(pdf_path)
            first_page = pdf_document.load_page(0)
            
            # Increase the resolution of the rendered page
            zoom_x = 3.0  # Horizontal zoom (scale factor)
            zoom_y = 3.0  # Vertical zoom (scale factor)
            mat = fitz.Matrix(zoom_x, zoom_y)
            pix = first_page.get_pixmap(matrix=mat)  # Apply the zoom matrix

            # Convert the pixmap to an Image object
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Define crop dimensions (focus on the center of the page)
            width, height = img.size
            crop_area = (
                width // 4,  # Start 25% from the left
                height // 4,  # Start 25% from the top
                width * 3 // 4,  # End 25% from the right
                height * 3 // 4  # End 25% from the bottom
            )
            cropped_img = img.crop(crop_area)

            # Save the cropped image to a BytesIO object
            img_io = BytesIO()
            cropped_img.save(img_io, format='JPEG')
            img_io.seek(0)

            # Save the image file to storage
            if default_storage.exists(preview_image_path):
                default_storage.delete(preview_image_path)
            
            # Save the image to the model
            self.preview_image.save(preview_image_name, ContentFile(img_io.read()), save=False)

            pdf_document.close()

class User(AbstractUser):
    library = models.ManyToManyField('Note', related_name='users_library', blank=True)
    
    # Add unique related_name to resolve conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Unique related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
