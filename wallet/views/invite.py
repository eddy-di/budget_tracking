import secrets
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from wallet.models.wallet import Wallet

from wallet.forms import InviteForm
from wallet.models.invite import Invite


def send_invitation_email(link, email, wallet):
    subject = f'Invitation to join {wallet}'
    message = render_to_string('wallet/invitation_email_template.html', {'link': link})
    send_mail(subject, message, 'eddy.di.fint@gmail.com', [email])


def invite_view(request):
    if request.method == 'POST':
        form = InviteForm(user=request.user, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            wallet = form.cleaned_data['wallet']
            print(wallet)
            token = secrets.token_hex(16)
            expiration_date = timezone.now() + timezone.timedelta(days=1)
            user = request.user
            invite = Invite.objects.create(
                token=token,
                expiration_date=expiration_date,
                user=user,
                wallet=wallet,
                email=email
            )
            invite_link = invite.generate_link

            send_invitation_email(link=invite_link, email=email, wallet=wallet)

            messages.success(request, 'Invitation sent successfully!')
            return redirect('wallet:successful_invite') # need to make this page

    else:
        form = InviteForm(user=request.user)
    
    return render(request, 'wallet/invite.html', {
        'form': form
    })


def successful_invite(request):
    return render(request, 'wallet/successful_invite.html')


def invite_confirmation(request, invite_token):
    print('start')
    invite = get_object_or_404(
        Invite,
        token=invite_token
    )
    print(invite)
    email = invite.email
    print(email)

    wallet_users = Wallet.objects.filter(name=invite.wallet).values_list(
        'users__email',
        )
    print(wallet_users)
    all_users = User.objects.values_list('email')
    # user = request.user

    if email not in wallet_users:
        if email not in all_users:
            print('Not here')
            return redirect ('account:register', invite_token=invite_token)
        else:
            print('not in wallet but in system')
            return redirect('account:redirect_with_token', invite_token=invite_token)


    return HttpResponse('done')