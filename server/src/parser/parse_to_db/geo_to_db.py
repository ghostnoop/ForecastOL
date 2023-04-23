from typing import List, Optional

from vkbottle_types.codegen.objects import BaseCountry, BaseCity

from main.models import Country, City
from parser.parse_to_db.utils import create_only_new_objects


def countries_to_db(countries: List[Optional[BaseCountry]]):
    countries_to_create = {}
    for country in countries:
        if country is not None:
            countries_to_create[country.id] = Country(
                id=country.id,
                name=country.title
            )
    create_only_new_objects(Country, countries_to_create)


def cities_to_db(cities: List[Optional[BaseCity]]):
    cities_to_create = {}
    for city in cities:
        if city is not None:
            cities_to_create[city.id] = City(
                id=city.id,
                name=city.title
            )
    create_only_new_objects(City, cities_to_create)
