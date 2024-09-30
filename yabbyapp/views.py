from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm, SignUpForm
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                auth_login(request, user)
                return redirect(reverse('home'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    recent_notes = request.user.library.order_by('-created_at')[:5]
    context = {'recent_notes': recent_notes}
    return render(request, 'yabbyapp/home.html', context)

@login_required
def practice(request):
    return render(request, 'yabbyapp/practice.html')

@login_required
def backpack(request):
    return render(request, 'yabbyapp/backpack.html')

@login_required
def profile(request):
    return render(request, 'yabbyapp/profile.html')

@login_required
def notifications(request):
    return render(request, 'yabbyapp/notifications.html')

@login_required
def quicklinks(request):
    return render(request, 'yabbyapp/quicklinks.html')

@login_required
def settings(request):
    return render(request, 'yabbyapp/settings.html')

@login_required
def manuals(request):
    return render(request, 'yabbyapp/manuals.html')

@login_required
def books(request):
    return render(request, 'yabbyapp/books.html')

@login_required
def teacherslounge(request):
    return render(request, 'yabbyapp/teachers-lounge.html')

@login_required
def notes(request):
    return render(request, 'yabbyapp/notes.html')

@login_required
def notes_list(request):
    selected_subject = request.GET.get('subject')
    selected_grade_level = request.GET.get('grade_level')

    notes = Note.objects.all()

    if selected_grade_level:
        notes = notes.filter(section=selected_grade_level)
    if selected_subject:
        notes = notes.filter(subject=selected_subject)

    context = {
        'notes': notes
    }

    # Check if the request is AJAX (for partial updates)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'yabbyapp/notes_partial.html', context)
    
    return render(request, 'yabbyapp/notes.html', context)

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'yabbyapp/note_detail.html', {'note': note})

@login_required
def load_notes(request, grade, subject):
    # Filter notes by grade and subject
    notes = Note.objects.filter(section=grade, subject=subject)
    
    # Prepare the data to return
    notes_data = [{
        'pk': note.pk,
        'title': note.title,
        'preview_image': note.preview_image.url if note.preview_image else None,
    } for note in notes]

    return JsonResponse({'notes': notes_data})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'yabbyapp/create_note.html', {'form': form})

@login_required
def add_to_library(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    user = request.user

    if note in user.library.all():
        messages.info(request, "This note is already in your library.")
    else:
        user.library.add(note)
        messages.success(request, "Note added to your library.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect back to the referring page or home if not available
