from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'description', 'image', 'created_at', 'updated_at')  # Adjust based on your model fields
    search_fields = ('title', 'subject')  # Adjust based on your model fields
