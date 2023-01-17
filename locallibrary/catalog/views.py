from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
import datetime
from catalog.forms import RenewBookModelForm
from django.contrib.auth.decorators import login_required, permission_required


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
    paginate_by = 10  

class AuthorDetailView(generic.DetailView):
    model =Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/mybooks.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/borrowedbooks.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:books-borrowed'))
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
  
    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    #initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books')


