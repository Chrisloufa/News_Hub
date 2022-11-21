from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm, PostForm, EditProfileForm, PasswordChangingForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class AddPost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add.html'
    success_url = reverse_lazy('home')


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'postupdate.html'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('home')


# Class based view to delete user comments
class DeleteComment(DeleteView):

    model = Comment
# After deletion of the user comment user returns to same blog post

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.post.slug])


# Class based view to update/edit user comments
class UpdateComment(UpdateView):

    model = Comment
    fields = ('body',)
# After update of the user comment user returns to same blog post

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.post.slug])


class UserEditView(UpdateView):
    form_class = EditProfileForm
    template_name = 'editprofile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    model = Post
    template_name = 'change_password.html'
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'successpassword.html', {})
