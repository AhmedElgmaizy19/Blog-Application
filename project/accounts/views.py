from django.shortcuts import render , redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    form = RegisterForm()
    if request.user.is_authenticated:
        messages.warning(request , 'You are already logged in..!')
        return redirect('home')
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            new_user = authenticate(username = username , password = password)
            login(request , new_user)
            messages.success(request , 'Account created successfully..!')
            return redirect('home')
    return render(request, 'register.html' , {'form':form})


def log_in(request):
    form = LoginForm()
    get_next = request.GET.get('next')
    if request.user.is_authenticated:
        messages.warning(request , f'You are already logged in..! ')
        return redirect('home')
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username , password = password)
            
            if user:
                login(request , user)
                messages.info(request , f'You are logged in sucssufuly ')
                return redirect('home')
            else:
                messages.warning(request , 'user not found')
                return redirect('login')
        else:
            form = LoginForm()
    return render(request , 'login.html' , {'form':form , 'next':get_next})



def log_out(request):
    logout(request)
    return redirect('home')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasssForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request , user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasssForm(request.user)
    return render(request, 'password_change.html', {'form': form})


@login_required
def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', pk=profile.id)
        else:
            messages.warning(request, f'{form.errors}')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})