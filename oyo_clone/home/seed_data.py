from accounts.models import *
from accounts.utils import generateSlug
from django.contrib.auth.models import User
from faker import Faker
fake = Faker()
import random


def createUser():
    for i in range(100):
        email = fake.email()
        HotelVendor.objects.create(
            email = email,
            business_name = fake.name(),
            username = email,
            first_name = fake.name(),
            phone_number = random.randint(1111111111, 9999999999),
        )

from random import choice
def createHotel():
    for i in range(100):
        hotel_vendor = choice(HotelVendor.objects.all())
        amenities = list(Amenities.objects.all())
        hotel_name = fake.company()
        hotel_price = round(fake.random_number(digits=4) / 100.0, 2)
        
        hotel = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = fake.text()[:50],
            hotel_slug = generateSlug(hotel_name),
            hotel_owner = hotel_vendor,
            hotel_price = hotel_price,
            hotel_offer_price = round((hotel_price)*0.75, 2),
            hotel_location = fake.address(),
            is_active = fake.boolean(),
        )
        hotel.amenities.set(amenities)