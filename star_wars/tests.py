import pytz
from datetime import datetime, timedelta

from django.urls import resolve, reverse
from rest_framework.test import APITestCase, APIClient

from .models import Character, CharacterRate
from .serializers import CharacterSerializer
from coderio.settings import CACHE_LIFETIME


# Create your tests here.

class TestCharacterAPI(APITestCase):
    def test_post_character_rating(self):
        client = APIClient()

        client.post(
            reverse('character-rating', args={1}),
            {'rating': 3},
        )

        self.assertEqual(
            Character.objects.get(api_id=1).max_rating(),
            3
        )

    def test_post_character_rating_wrong_value(self):
        client = APIClient()

        response = client.post(
            reverse('character-rating', args={1}),
            {'rating': 6},
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_get_uncached_character(self):
        client = APIClient()

        response = client.get(
            reverse('character', args={1}),
        )

        character = Character.objects.get(api_id=1)

        self.assertEqual(
            CharacterSerializer(Character.objects.get(api_id=1)).data,
            response.json()
        )

        self.assertEqual(
            character.cached_recently(),
            True
        )

        self.assertEqual(
            character.last_update.date(),
            datetime.utcnow().date()
        )

    def test_get_recached_character(self):
        character = Character.get_by_api_id(api_id=1)
        character.last_update = datetime.utcnow().replace(
            tzinfo=pytz.utc
        ) - timedelta(
            days=CACHE_LIFETIME+1
        )
        
        character.save()

        self.assertEqual(
            character.cached_recently(),
            False
        )

        client = APIClient()

        response = client.get(
            reverse('character', args={1}),
        )

        self.assertEqual(
            CharacterSerializer(Character.objects.get(api_id=1)).data,
            response.json()
        )

        self.assertNotEqual(
            character.last_update.date(),
            datetime.utcnow().date()
        )

    def test_get_character_specie_unknown(self):
        client = APIClient()

        response = client.get(
            reverse('character', args={1}),
        )

        self.assertEqual(
            "",
            response.json()['species_name']
        )

    def test_get_character_raitings(self):
        character_rating_url = reverse('character-rating', args={1})

        client = APIClient()

        client.post(
            character_rating_url,
            {'rating': 1},
        )

        client.post(
            character_rating_url,
            {'rating': 3},
        )

        client.post(
            character_rating_url,
            {'rating': 5},
        )

        character_response = client.get(
            reverse('character', args={1}),
        )

        self.assertEqual(
            3,
            character_response.json()['average_rating']
        )

        self.assertEqual(
            5,
            character_response.json()['max_rating']
        )
