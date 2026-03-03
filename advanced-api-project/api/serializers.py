from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization of the Book model.
    Includes custom validation to ensure publication_year is not in the future.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        
    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization of the Author model.
    Includes nested BookSerializer to serialize related books dynamically.
    This demonstrates how to handle one-to-many relationships in DRF.
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        
    def to_representation(self, instance):
        """
        Customize the representation to include the count of books.
        This shows how to extend serializer functionality.
        """
        representation = super().to_representation(instance)
        representation['books_count'] = instance.books.count()
        return representation
