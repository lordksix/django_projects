from django.contrib import admin


from .models import Author, Genre, Book, BookInstance,Language
# Register your models here

def display_genre(self):
    """Create a string for the Genre. This is required to display genre in Admin."""
    return ', '.join(genre.name for genre in self.genre.all()[:3])

display_genre.short_description = 'Genre'

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0

class BooksInline(admin.StackedInline):
    model = Book
    extra=0

class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines=[BooksInline]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', display_genre)
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)    
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)


