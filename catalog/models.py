from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200,
                    help_text=_('Enter a book genre (e.g. Science Fiction)'))

    def __str__(self):
        return self.name

class Book(models.Model):
    # Add book's title
    title = models.CharField(max_length=200)

    # Create foreign key, 1-n between author-book
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    
    # Add language for book
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    # Add book's summary
    summary = models.TextField(max_length=1500,
                    help_text=_('Enter the description of the book'))
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                    help_text=_('13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'))

    # Create m-n relationship between book-genre
    genre = models.ManyToManyField(Genre, help_text=_('Select a genre for this book'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                    help_text=_('Unique ID for this particular book across whole library'))
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book availability'),
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    language_name = models.CharField(max_length=50,
                    help_text=_('Enter the book\'s language'))
    def __str__(self):
        return self.language_name
