from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter book title'}))
    author = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter author name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter book description'}), required=False)
    publish_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'publish_date']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("The title must be at least 5 characters long.")
        return title

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if len(author) < 3:
            raise forms.ValidationError("The author name must be at least 3 characters long.")
        return author
