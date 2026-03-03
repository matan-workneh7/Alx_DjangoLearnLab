from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form with email field
    """
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        # Check if email is already used by another user
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email is already in use by another account.')
        
        return email


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select tags for your post (optional)'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Write your post content here...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all().order_by('name')


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }


class TagForm(forms.ModelForm):
    """
    Form for creating and editing tags
    """
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag name'
            })
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = name.strip().lower()
        
        # Check if tag already exists
        if Tag.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('A tag with this name already exists.')
        
        return name


class SearchForm(forms.Form):
    """
    Form for searching posts
    """
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts...'
        })
    )
