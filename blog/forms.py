from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm (forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'slug', 'featured_image',
                  'content', 'author')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder':
                                            'Input your title'}),
            'excerpt': forms.TextInput(attrs={'placeholder':
                                              'Write it here'}),
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'value': '',
                       'id': 'user', 'type': 'hidden'}),
        }
