from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                username=cd['username'], 
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authernticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    
    return render(request, 
                  'account/login.html', 
                  {'form': form})


@login_required
def wallet(request):
    return render(request, 
                  'wallet/wallet_index.html', 
                  {'section': 'wallet'})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False) # create new user obj but not commit to db
            new_user.set_password(user_form.cleaned_data['password']) # set password to user obj
            new_user.save() # save user obj in db
            Profile.objects.create(user=new_user) # create profile of new user
            return render(request, 
                          'account/register_done.html', 
                          {'new_user': new_user})
        
    else:
        user_form = UserRegistrationForm()
    return render(request, 
                  'account/register.html', 
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, 
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                       data=request.POST, 
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 
                  'account/edit.html', 
                  {'user_form': user_form, 
                   'profile_form': profile_form})