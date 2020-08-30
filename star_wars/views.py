from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .models import Character, CharacterRate
from .serializers import CharacterSerializer


@api_view(['GET'])
def get_character(request, pk):
    return Response(
        CharacterSerializer(
            Character.get_by_api_id(api_id=pk)
        ).data
    )


@api_view(['POST'])
def rate_character(request, pk):
    if 1 <= int(request.data['rating']) <= 5:
        CharacterRate.objects.create(
            character=Character.get_by_api_id(api_id=pk),
            rating=request.data['rating']
        )
        return Response(
            'OK',
            status=200
        )
    else:
        return Response(
            'Rating must be an int between 1 and 5',
            status=400
        )
