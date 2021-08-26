from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        registerForm = UserCreationForm(request.POST)
        if registerForm.is_valid:
            registerForm.save()
            username = registerForm.cleaned_data['username']
            password = registerForm.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        registerForm = UserCreationForm()

    context = {'form': registerForm}

    return render(request, 'registration/register.html', context)
