from . import views
from django.urls import path

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('new', views.DashboardNew.as_view(), name='dashboard_new'),
    path('<int:pk>/edit', views.DashboardEdit.as_view(), name='dashboard_edit'),
    path('<int:pk>/delete', views.DashboardDelete.as_view(), name='dashboard_delete'),
    path('<int:pk>/view', views.DashboardViewPost.as_view(), name='dashboard_view'),
]