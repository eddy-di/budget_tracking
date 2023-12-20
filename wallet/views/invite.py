import secrets
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone

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