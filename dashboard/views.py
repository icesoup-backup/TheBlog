from blog.models import Post
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class Dashboard(ListView):
    template_name = 'dashboard/dashboard_home.html'
    model = User

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('home')
        return super(Dashboard, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class DashboardNew(CreateView):
    template_name = 'dashboard/dashboard_new.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')


    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('home')
        return super(DashboardNew, self).dispatch(
            request, *args, **kwargs)


class DashboardEdit(UpdateView):
    template_name = 'dashboard/dashboard_update.html'
    model = User
    form_class = UserChangeForm
    success_url = reverse_lazy('dashboard')

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('home')
        return super(DashboardEdit, self).dispatch(
            request, *args, **kwargs)


class DashboardDelete(DeleteView):
    template_name = 'dashboard/dashboard_delete.html'
    model = User
    success_url = reverse_lazy('dashboard')

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('home')
        return super(DashboardDelete, self).dispatch(
            request, *args, **kwargs)


class DashboardViewPost(DetailView):
    template_name = 'dashboard/dashboard_viewposts.html'
    model = User

    def user_passes_test(self, request):
        if request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('home')
        return super(DashboardViewPost, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        print(obj)
        context['posts'] = Post.objects.filter(author = obj)
        print(context)
        return context