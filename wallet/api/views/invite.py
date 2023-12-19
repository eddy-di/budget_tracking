import secrets
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from wallet.models.invite import Invite
from wallet.api.serializers.invite import InviteSerializer
from wallet.models.wallet import Wallet


class InviteCreateView(generics.ListCreateAPIView):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def generate_unique_token():
        return secrets.token_hex(16)

    # @classmethod
    # def create_invite_link(cls, wallet):
        # token = cls.generate_unique_token()
        # expiration_date = timezone.now() + timezone.timedelta(days=1)
        # invite_link = cls.objects.create(token=token, wallet=wallet, expiration_date=expiration_date)
        # return invite_link

    # def create(self, request, *args, **kwargs):
        # # Get the wallet from the request or however you have it available
        # wallet = Wallet.objects.get(id=request.data.get('wallet'))

        # # Generate the token
        # token = self.generate_unique_token()

        # # Add the token to the request data
        # request.data['token'] = token

        # # Call the base class create method
        # return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Get the wallet from the request or however you have it available
        wallet = Wallet.objects.get(id=self.request.data.get('wallet'))
        # Create the invite link for the given wallet using the class method
        # invite_link = self.create_invite_link(wallet)
        token = self.generate_unique_token()
        # Create the invite link
        serializer.save(
            token=token, 
            wallet=wallet, 
            user=self.request.user
            )



@api_view(['GET'])
@login_required
def join_wallet(request, token):
    invite_link = Invite.objects.get(token=token, expiration_date__gte=timezone.now())
    wallet = invite_link.wallet

    # Check if the user is already in the wallet
    if request.user not in wallet.users.all():
        # Add the user to the wallet
        wallet.users.add(request.user)

    # Your logic to handle the redirection or response after joining the wallet
    # ...

    # Delete the invite link after it's used
    invite_link.delete()

    return redirect('success_page')  # Redirect to a success page or return a success response