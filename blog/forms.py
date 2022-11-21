from .models import Comment, Post, User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
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

class EditProfileForm(UserChangeForm):
    password = None
    username = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=100, label="Old Password", widget=forms.PasswordInput())
    new_password1 = forms.CharField(
        max_length=100, label="New Password", widget=forms.PasswordInput())
    new_password2 = forms.CharField(
        max_length=100, label="Confirm Password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]