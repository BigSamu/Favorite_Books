from urllib.parse import urlparse
from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request):
    if 'name' in request.session:
        return redirect('/books')
    return render(request,'index.html')


# Register new user
def register(request):
  
    errors = User.objects.validatorSignUp(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_password
    )
    
    request.session['name'] = newUser.first_name
    request.session['id'] = newUser.id
    return redirect('/books')

# Login for current user
def login(request):
    # login for current User
    
    if request.method == 'POST':
        errors = User.objects.validatorSignIn(request.POST)
        
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        loggedUser = User.objects.get(email=request.POST['email'])
        print(loggedUser)
        request.session['name'] = loggedUser.first_name
        request.session['id'] = loggedUser.id
        return redirect('/books')

    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    if 'name' in request.session:
        
        currentUser = User.objects.get(id=request.session['id'])
        context = {
            'all_books': Book.objects.all(),
            'books_liked_by_current_user': currentUser.liked_books.all() 
        }
    
        return render(request,'home.html', context)
    return redirect('/')



def add_book(request):

    errors = Book.objects.validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')

    currentUser = User.objects.get(id=request.session['id'])
    newBook = Book.objects.create(
        title = request.POST['book_title'],
        description = request.POST['book_description'],
        uploaded_by = currentUser,
    )

    newBook.users_who_like.add(currentUser)

    return redirect('/books')

def add_book_to_favorites(request, book_id):

    currentUser = User.objects.get(id=request.session['id'])
    bookSelected = Book.objects.get(id=book_id)

    bookSelected.users_who_like.add(currentUser)
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        prev_path = urlparse(referer).path
    else:
        prev_path = '/'
  
    if (prev_path == reverse('user_books_app:home')):
        return redirect('/books')
    else:
        return redirect(f'/books/{str(book_id)}')

def remove_book_from_favorites(request, book_id):

    currentUser = User.objects.get(id=request.session['id'])
    bookSelected = Book.objects.get(id=book_id)

    bookSelected.users_who_like.remove(currentUser)

    return redirect(f'/books/{str(book_id)}')

def books_details(request, book_id):
    
    if 'name' in request.session:
        
        currentUser = User.objects.get(id=request.session['id'])
        context = {
            'book_selected': Book.objects.get(id=book_id),
            'books_liked_by_current_user': currentUser.liked_books.all()
        }
        return render(request,'book_details.html', context)
    return redirect('/books')

def edit_book(request, book_id):
   
    errors = Book.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{str(book_id)}')

    
    bookToUpdate = Book.objects.get(id = book_id)

    bookToUpdate.title = request.POST['book_title']
    bookToUpdate.description = request.POST['book_description']
    bookToUpdate.save()
    
    return redirect(f'/books')
   

def remove_book(request, book_id):
    bookToRemove = Book.objects.get(id=book_id)
    bookToRemove.delete()
    return redirect('/books')