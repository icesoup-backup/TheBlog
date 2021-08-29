from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    model = UserModel

    def get_success_url(self):
        form = self.request.POST
        username = form.get('username')
        password = form.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return reverse_lazy('home')
