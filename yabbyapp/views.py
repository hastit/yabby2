from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                auth_login(request, user)
            return redirect('home')  # Redirect to the home page after signup
    else:
        form = UserCreationForm()
    
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

# Navigation Bar Pages
@login_required
def home(request):
    return render(request, 'yabbyapp/home.html')

@login_required
def practice(request):
    return render(request, 'yabbyapp/practice.html')

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
def notes(request):
    return render(request, 'yabbyapp/notes.html')

@login_required
def teacherslounge(request):
    return render(request, 'yabbyapp/teachers-lounge.html')

@login_required
def notes_list(request):
    # Retrieve the subject from the GET parameters
    selected_subject = request.GET.get('subject')

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('notes_list')  # Redirect after form submission
    else:
        form = NoteForm()

    # Filter notes by the selected subject if provided
    if selected_subject:
        notes = Note.objects.filter(subject=selected_subject)
    else:
        notes = Note.objects.all()  # Show all notes if no subject is selected

    # Pass the selected subject to the template to highlight the active filter
    return render(request, 'yabbyapp/notes.html', {'notes': notes, 'form': form, 'selected_subject': selected_subject})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'yabbyapp/note_detail.html', {'note': note})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('notes_list')  # Ensure 'notes_list' URL name exists
    else:
        form = NoteForm()
    return render(request, 'yabbyapp/create_note.html', {'form': form})
