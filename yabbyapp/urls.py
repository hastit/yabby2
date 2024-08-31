from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('practice/', views.practice, name='practice'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('quicklinks/', views.quicklinks, name='quicklinks'),
    path('settings/', views.settings, name='settings'),
    path('manuals/', views.manuals, name='manuals'),
    path('books/', views.books, name='books'),
    path('notes/', views.notes_list, name='notes_list'),  # Updated to use notes_list
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('create_note/', views.create_note, name='create_note'),
    path('teacherslounge/', views.teacherslounge, name='teacherslounge'),
]
