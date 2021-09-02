from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('blog/<slug:slug>/comment/', views.CommentNew.as_view(),
         name='comment'),
    path('blog/<slug:slug>/status/', views.PostStatus.as_view(),
         name='status'),
    path('blog/<slug:slug>/edit', views.PostEdit.as_view(), name='edit'),
    path('blog/new', views.PostNew.as_view(), name='post_new'),
    path('blog/<slug:slug>/delete', views.PostDelete.as_view(), name='delete')
]
