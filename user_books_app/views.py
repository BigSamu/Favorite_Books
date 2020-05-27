from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')

def userDetails(request):
    if 'name' in request.session:
        
        currentUser = User.objects.get(id=request.session['id'])
        context = {
            'all_books': Book.objects.all(),
            'books_liked_by_current_user': currentUser.liked_books.all() 
        }
        return render(request,'user_details.html', context)
    return redirect('/')

def register(request):
    print(request.POST)
    
    errors = User.objects.validator(request.POST)
    

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

def login(request):
    # login for current User
    
    try:
        loggedUser = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), loggedUser.password.encode()):
            print(loggedUser.first_name, "logged user was signed in!")
            request.session['name'] = loggedUser.first_name
            request.session['id'] = loggedUser.id
            return redirect('/books')

    except loggedUser.DoesNotExist:
        loggedUser = None

    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def addBooktoList(request):

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

def addBookToFavorites(request, book_id):

    currentUser = User.objects.get(id=request.session['id'])
    bookSelected = Book.objects.get(id=book_id)

    bookSelected.users_who_like.add(currentUser)
    print(request.path)

    return redirect('/books')

def addBookToFavoritesFunctionTwo(request, book_id):

    currentUser = User.objects.get(id=request.session['id'])
    bookSelected = Book.objects.get(id=book_id)

    bookSelected.users_who_like.add(currentUser)

    return redirect(f'/books/{str(book_id)}')

def removeBookFromFavorites(request, book_id):

    currentUser = User.objects.get(id=request.session['id'])
    bookSelected = Book.objects.get(id=book_id)

    bookSelected.users_who_like.remove(currentUser)

    return redirect(f'/books/{str(book_id)}')

def booksDetails(request, book_id):
    
    if 'name' in request.session:
        
        currentUser = User.objects.get(id=request.session['id'])
        context = {
            'book_selected': Book.objects.get(id=book_id),
            'books_liked_by_current_user': currentUser.liked_books.all()
        }
        return render(request,'book_details.html', context)
    return redirect('/books')

def updateBook(request):
   
    errors = Book.objects.validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{str(book_id)}')

    currentUser = User.objects.get(id=request.session['id'])
    bookToUpdate = Book.objects.get(id = book_id)

    bookToUpdate

    newBook.users_who_like.add(currentUser)

    return redirect(f'/books/{str(book_id)}')
   

def deleteBook(request):
    pass