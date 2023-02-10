from django.urls import path
from . import views

app_name = 'user_books_app'

urlpatterns = [
    path("", views.index, name="auth"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("books", views.home, name="home"),
    path("books/<int:book_id>", views.books_details, name="book_details"),
    path("books/new", views.add_book, name="add_book"),
    path("books/<int:book_id>/edit", views.edit_book, name="edit_book"),
    path("books/<int:book_id>/delete", views.remove_book, name="remove_book"),
    path(
        "books/<int:book_id>/add_to_favorites",
        views.add_book_to_favorites,
        name="add_book_to_favorites",
    ),
    path(
        "books/<int:book_id>/remove_from_favorites",
        views.remove_book_from_favorites,
        name="remove_book_from_favorites",
    ),
    
]
