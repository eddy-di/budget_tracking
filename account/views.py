from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from wallet.models.invite import Invite
from wallet.models.wallet import Wallet

def user_login(request, invite_token=None):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    # Check if there's an invite token in the URL
                    if invite_token:
                        # Retrieve the associated wallet and redirect the user
                        invite = get_object_or_404(Invite, token=invite_token)
                        wallet = invite.wallet
                        destination_wallet = Wallet.objects.get(id=wallet.id)
                        destination_wallet.users.add(user)
                        return redirect('wallet:wallet_info', wallet_id=wallet.id)
                    
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    
    return render(request, 'account/login_with_token.html', {'form': form})


@login_required
def wallet(request):
    return render(request, 
                  'wallet/wallet_index.html', 
                  {'section': 'wallet'})


def register(request, invite_token=None):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False) # create new user obj but not commit to db
            new_user.set_password(user_form.cleaned_data['password']) # set password to user obj
            new_user.save() # save user obj in db
            Profile.objects.create(user=new_user) # create profile of new user
            
            # Log in the newly created user
            user = authenticate(request, username=new_user.username, password=user_form.cleaned_data['password'])
            if user is not None:
                login(request, user)

            if invite_token is None:
                return render(request, 'account/register_done.html', {'new_user': new_user})
            
            else:
                invite = get_object_or_404(Invite, token=invite_token)
                wallet = invite.wallet
                destination_wallet = Wallet.objects.get(id=wallet.id)
                destination_wallet.users.add(new_user)

                # Redirect the newly created and logged-in user to the wallet page
                return redirect('wallet:wallet_info', wallet_id=wallet.id)
        
    else:
        user_form = UserRegistrationForm()

        if invite_token:
            invite = get_object_or_404(
                Invite,
                token=invite_token
            )

            user_form.fields['email'].initial = invite.email
            wallet = invite.wallet.id                

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
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user) # profile
    
    return render(request, 
                  'account/edit.html', 
                  {'user_form': user_form, 
                   'profile_form': profile_form})


def redirect_to_login(request):
        return render(request, 'account/redirect_to_login.html')


def successful_login(request):
    return render(request, 'account/successful_login.html')