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


    def perform_create(self, serializer):
        # Get the wallet from the request or however you have it available
        wallet = Wallet.objects.get(id=self.request.data.get('wallet'))
        # Create token to the link
        token = self.generate_unique_token()
        # Create the invite link
        serializer.save(
            token=token, 
            wallet=wallet, 
            user=self.request.user
            )
        
    
    def return_link(self):
        return Response({"link":self.generate_link})



@api_view(['GET'])
@login_required
def join_wallet(request, token):
    invite = Invite.objects.get(token=token, expiration_date__gte=timezone.now())
    wallet = invite.wallet

    # Check if the user is already in the wallet
    if request.user not in wallet.users.all():
        # Add the user to the wallet
        wallet.users.add(request.user)

    # Your logic to handle the redirection or response after joining the wallet
    # ...

    # Delete the invite link after it's used
    invite_link.delete()

    return redirect('success_page')  # Redirect to a success page or return a success response