from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'catalog/index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )



class BookListView(generic.ListView):
    """View class for web page of all the books."""
    model = Book
    paginate_by = 2
"""     context_object_name = 'book_list'   # your own name for the list as a template variable
    def get_queryset(self):
        return Book.objects.all() """
    #template_name = 'catalog/book_list.html'  # Specify your own template name/location    

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    """View class for web page of all the books."""
    model = Author
    paginate_by = 2  

class AuthorDetailView(generic.DetailView):
    model =Author