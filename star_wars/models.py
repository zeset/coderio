import pytz
import requests
from datetime import datetime

from django.db import models
from django.db.models import Avg

from coderio.settings import CACHE_LIFETIME
from .utils import (
    RequestError,
    parse_homeworld_data,
    parse_species_name,
    parse_homeworld_id
)


class Homeworld(models.Model):
    ENDPOINT = "https://swapi.dev/api/planets/"

    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    population = models.CharField(max_length=100)
    known_residents_count = models.IntegerField(null=True)
    last_update = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_by_api_id(self, api_id):
        homeworld, created = Homeworld.objects.get_or_create(
            api_id=api_id
        )

        if created or homeworld.cached_recently():
            homeworld.update_from_api()

        return homeworld

    def mark_as_cached(self):
        self.last_update = datetime.utcnow().replace(
            tzinfo=pytz.utc
        )
        self.save()

    def cached_recently(self):
        has_cache = self.last_update is None

        return has_cache or (datetime.utcnow().replace(
            tzinfo=pytz.utc
        ) - self.last_update.replace(
            tzinfo=pytz.utc
        )).days <= CACHE_LIFETIME

    def update_from_api(self):
        homeworld_response = requests.get(f"{self.ENDPOINT}{self.api_id}/")

        if 400 <= homeworld_response.status_code < 600:
            raise RequestError

        Homeworld.objects.filter(pk=self.id).update(
            **parse_homeworld_data(homeworld_response.json()),
        )

        self.mark_as_cached()

        self.refresh_from_db()


class Character(models.Model):
    ENDPOINT = "https://swapi.dev/api/people/"
    API_DESIRED_ATTRIBUTES = [
        'name',
        'height',
        'mass',
        'hair_color',
        'skin_color',
        'eye_color',
        'birth_year',
        'gender'
    ]

    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=100, null=True, blank=True)
    mass = models.CharField(max_length=100, null=True, blank=True)
    hair_color = models.CharField(max_length=100, null=True, blank=True)
    skin_color = models.CharField(max_length=100, null=True, blank=True)
    eye_color = models.CharField(max_length=100, null=True, blank=True)
    birth_year = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    species_name = models.CharField(max_length=100, null=True, blank=True)
    homeworld = models.ForeignKey(
        Homeworld, related_name='characters',
        on_delete=models.CASCADE, null=True, blank=True
    )
    last_update = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_by_api_id(self, api_id):
        character, created = Character.objects.get_or_create(
            api_id=api_id
        )

        if created or not character.cached_recently():
            character.update_from_api()

        return character

    def mark_as_cached(self):
        self.last_update = datetime.utcnow().replace(
            tzinfo=pytz.utc
        )
        self.save()

    def max_rating(self):
        max_rating = self.ratings.order_by('-rating').first()
        if max_rating is None:
            return 0

        return max_rating.rating

    def avg_rating(self):
        return self.ratings.aggregate(
            average_rating=Avg('rating')
        )['average_rating'] or 0

    def cached_recently(self):
        has_cache = self.last_update is None

        return has_cache or (datetime.utcnow().replace(
            tzinfo=pytz.utc
        ) - self.last_update.replace(
            tzinfo=pytz.utc
        )).days <= CACHE_LIFETIME

    def update_from_api(self):
        character_response = requests.get(f"{self.ENDPOINT}{self.api_id}/")

        if 400 <= character_response.status_code < 600:
            raise RequestError

        response_data = character_response.json()

        Character.objects.filter(pk=self.id).update(
            **{key: response_data[key] for key in self.API_DESIRED_ATTRIBUTES},
            species_name=parse_species_name(response_data),
            homeworld=Homeworld.get_by_api_id(
                api_id=parse_homeworld_id(
                    response_data
                )
            ),
        )

        self.mark_as_cached()

        self.refresh_from_db()


class CharacterRate(models.Model):
    rating = models.IntegerField()
    character = models.ForeignKey(
        Character, related_name='ratings', on_delete=models.CASCADE
    )
