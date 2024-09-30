from django.urls import path
from . import views
from .views import load_notes

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('backpack/', views.backpack, name='backpack'),
    path('practice/', views.practice, name='practice'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('quicklinks/', views.quicklinks, name='quicklinks'),
    path('settings/', views.settings, name='settings'),
    path('manuals/', views.manuals, name='manuals'),
    path('books/', views.books, name='books'),
    path('teacherslounge/', views.teacherslounge, name='teacherslounge'),
    path('add_to_library/<int:note_id>/', views.add_to_library, name='add_to_library'),
    path('notes_list/', views.notes_list, name='notes_list'),
    path('notes/<str:grade>/<str:subject>/', views.load_notes, name='load_notes'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('create_note/', views.create_note, name='create_note'),
    path('notes/<str:grade_level>/<str:subject>/', views.notes_list, name='notes_list'),
]
