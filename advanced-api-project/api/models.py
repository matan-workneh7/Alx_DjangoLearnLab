from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model represents a book author with a name field.
    This model has a one-to-many relationship with the Book model.
    """
    name = models.CharField(max_length=100, help_text="The name of the author")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a book with title, publication year, and author.
    This model has a foreign key relationship to the Author model,
    establishing a many-to-one relationship (many books can have one author).
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(
        help_text="The year the book was published"
    )
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="The author of this book"
    )
    
    class Meta:
        ordering = ['-publication_year', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
