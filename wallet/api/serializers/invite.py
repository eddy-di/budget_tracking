from rest_framework import serializers
from wallet.models.invite import Invite


class InviteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Invite
        fields = ['id', 'token', 'wallet', 'expiration_date', 'user', 'is_deleted']