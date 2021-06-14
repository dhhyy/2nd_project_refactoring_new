import os
import django
import csv
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.chdir("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wagrano.settings')
django.setup()

from products.models import *
from users.models    import *
#CSV_PATH_PRODUCTS = './Product.csv'

with open('./db_upload/categories.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        Category.objects.create(
                name           = data['name'],
                image_url      = data['image_url'],
                )

with open('./db_upload/destinations.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        Destination.objects.create(
                name      = data['name'],
                image_url = data['image_url']
                )

with open('./db_upload/category_destinations.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        CategoryDestination.objects.create(
                category_id    = data['category_id'],
                destination_id = data['destination_id']
                )

with open('./db_upload/cities.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        City.objects.create(
                name = data['name']
                )
        
with open('./db_upload/districts.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        District.objects.create(
                name = data['name'],
                city_id = data['city_id']
                )

with open('./db_upload/room_types.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        RoomType.objects.create(
                name = data['name']
                )

with open('./db_upload/rooms.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        Room.objects.create(
                star_rating    = data['star_rating'],
                room_type_id   = data['room_type_id'],
                )

with open('./db_upload/service_types.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        ServiceType.objects.create(
                name = data['name']
                )

with open('./db_upload/conveniences.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        Convenience.objects.create(
                name            = data['name'],
                service_type_id = data['service_type_id']
                )

with open('./db_upload/room_conveniences.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        RoomConvenience.objects.create(
                room_id = data['room_id'],
                convenience_id  = data['convenience_id'],
                service_type_id = data['service_type_id']
                )

with open('./db_upload/dinning_types.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        DinningType.objects.create(
                name = data['name']
                )

with open('./db_upload/food_types.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        FoodType.objects.create(
                name = data['name']
                )

with open('./db_upload/dinnings.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        Dinning.objects.create(
                dinning_type_id = data['dinning_type_id'],
                food_type_id = data['food_type_id']
                )

with open('./db_upload/dinning_options.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        DinningOption.objects.create(
                name        = data['name'],
                price       = data['price'],
                description = data['description'],
                dinning_id  = data['dinning_id']
                )
print(1)
with open('./db_upload/products.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
            Product.objects.create(
                    name           = data['name'],
                    rating         = data['rating'],
                    description    = data['description'],
                    address        = data['address'],
                    latitude       = data['latitude'],
                    longitude      = data['longitude'],
                    category_id    = data['category_id'],
                    destination_id = data['destination_id'],
                    district_id    = data['district_id'],
                    city_id        = data['city_id'],
                    price          = data['price'],
                    is_room        = data['is_room'],
                    room_id        = data['room_id'],
                    is_dinning     = data['is_dinning'],
                    dinning_id     = data['dinning_id'],
                    is_activity    = data['is_activity'],
                    is_popular     = data['is_popular']
                    )
print(2)

with open('./db_upload/product_images.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        ProductImage.objects.create(
            image_url = data['image_url'],
            product_id = data['product_id']
        )

with open('./db_upload/reviews.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        Review.objects.create(
            dinning_id  = data['dinning_id'],
            user_id     = data['user_id'],
            comment     = data['comment'],
            star_rating = data['star_rating']
        )

with open('./db_upload/coupons.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        Coupon.objects.create(
                name = data['name'],
                code = data['code'],
                discount_rate = data['discount_rate'],
                expire_date = data['expire_date'],
                product_id = data['product_id']
                )

with open('./db_upload/users.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        User.objects.create(
                email = data['email'],
                password = data['password'],
                name = data['name'],
                last_name = data['last_name'],
                first_name = data['first_name'],
                phone_number = data['phone_number'],
        )
with open('./db_upload/user_coupons.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for data in csv_reader:
        UserCoupon.objects.create(
                user_id = data['user_id'],
                coupon_id = data['coupon_id']
                )
