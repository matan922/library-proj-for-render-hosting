from flask import render_template, redirect, Blueprint, request
from project import db
from project.books.models import Books

books = Blueprint('books', __name__, template_folder='templates', url_prefix = '/books')

'''Function that shows books based on index given in the url's endpoint
or shows all books if no index was given.
Default is set to show all books.'''
@books.route("/", methods=["GET"])
@books.route("/<ind>")
def show_book_list(ind=-1):
    if int(ind)==-1:
        return render_template('all_books.html', books = Books.query.all())
    if int(ind) > -1:
        single_book=Books.query.get(int(ind))
        return render_template('books.html', single_book=single_book)

'''Function made to search a specific book based 
on the index given in the url's endpoint from the function above.'''
@books.route("/book_search", methods=['POST'])
def books_name():
    name = request.form['bookname']
    # If the book's name from the html <input> tag matches a name from the database it redirects you to said database id in the url's endpoint.
    book = Books.query.filter(Books.bookname==name).first()
    # If book does not exist you get redirected to the same page that shows all books.
    if book is None:
        return redirect('/books')
    return redirect(f"{book.id}") 

# Function made to render a page where a user can add a new book to the library.
@books.route("/add_book")
def new_book_page():
    return render_template('add_book.html')

# Function made to add a new book from the page created by previous function.
@books.route("/", methods=['POST'])
def add_books():
    # Making a form that connects to the <form> html tag for user input.
    request_data = request.form
    bookname= request_data["bookname"]
    author = request_data["author"]
    publishdate = request_data["publishdate"]
    # Type of loan connects to the return date of a book.
    typeofloan = request_data["typeofloan"]
    new_book = Books(bookname,author,publishdate,typeofloan)
    db.session.add(new_book)
    db.session.commit()
    return redirect('/books')

# Function made to delete a book from the databse based on the index (id) of the book.
@books.route("/books_del", methods=['GET'])
@books.route("/books_del/<ind>")
def delete_book(ind):
    book = Books.query.get(ind)
    # If the book does not exist return to the endpoint that shows all books.
    if book is None:
        return render_template('all_books.html', books=Books.query.all())
    try:
        db.session.delete(book)
        db.session.commit()
    except:
        return render_template('all_books.html', books=Books.query.all())
    return render_template('all_books.html', books=Books.query.all())
    # After function is done running it will render the page that shows all books.




