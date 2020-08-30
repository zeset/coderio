from .models import Character, Homeworld

from rest_framework import serializers


class HomeworldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homeworld
        exclude = ('api_id', 'last_update', 'id')
        depth = 1


class CharacterSerializer(serializers.ModelSerializer):
    average_rating = serializers.IntegerField(source='avg_rating')
    max_rating = serializers.IntegerField()
    homeworld = HomeworldSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Character
        exclude = ('api_id', 'last_update', 'id')
