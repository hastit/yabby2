from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Note

User = get_user_model()

class UserAdmin(DefaultUserAdmin):
    model = User

    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('library',)}),
    )
    add_fieldsets = DefaultUserAdmin.add_fieldsets + (
        (None, {'fields': ('library',)}),
    )
    list_display = DefaultUserAdmin.list_display + ('library_count',)
    search_fields = DefaultUserAdmin.search_fields + ('library',)

    def library_count(self, obj):
        return obj.library.count()
    library_count.short_description = 'Library Count'

admin.site.register(User, UserAdmin)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'description', 'image', 'preview_image', 'created_at', 'updated_at')
    search_fields = ('title', 'subject')
    list_filter = ('created_at', 'updated_at')
