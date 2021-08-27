from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/comment/', views.CommentNew.as_view(), name='comment'),
    path('<slug:slug>/edit', views.PostEdit.as_view(), name='edit'),
    path('new', views.PostNew.as_view(), name='post_new'),
    path('<slug:slug>/delete', views.PostDelete.as_view(), name='delete')
]