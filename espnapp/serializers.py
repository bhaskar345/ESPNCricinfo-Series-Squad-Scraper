from rest_framework import serializers
from espnapp.models import Players, Squads


class PlayersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ['name', 'role', 'age']


class SquadSerializer(serializers.ModelSerializer):
    squad = PlayersSerializers(many=True)

    class Meta:
        model = Squads
        fields = ['name', 'squad', 'series']
