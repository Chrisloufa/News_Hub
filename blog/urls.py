from django.urls import path
from . import views
from .views import AddPost, UpdatePostView, DeletePostView
from .views import DeleteComment, UpdateComment

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path('<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('delete_comment/<slug:slug>/<int:pk>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
    path('add/', AddPost.as_view(), name='add_post'),
    path('edit/<slug:slug>/', UpdatePostView.as_view(), name='update_post'),
    path('<slug:slug>/delete/', DeletePostView.as_view(), name='delete'),
    path('delete_comment/<int:pk>', views.DeleteComment.as_view(),
         name='delete_comment'),
    path('update_comment/<int:pk>', views.UpdateComment.as_view(),
         name='update_comment')
]
